"""Module containing a preprocessor that executes the code cells
and updates outputs"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from textwrap import dedent

try:
    from queue import Empty  # Py 3
except ImportError:
    from Queue import Empty  # Py 2

from traitlets import List, Unicode, Bool, Enum, Any, Type

from nbformat.v4 import output_from_msg
from .base import Preprocessor
from ..utils.exceptions import ConversionException
from traitlets import Integer


class CellExecutionError(ConversionException):
    """
    Custom exception to propagate exceptions that are raised during
    notebook execution to the caller. This is mostly useful when
    using nbconvert as a library, since it allows to deal with
    failures gracefully.
    """
    def __init__(self, traceback):
        self.traceback = traceback

    def __str__(self):
        s = self.__unicode__()
        if not isinstance(s, str):
            s = s.encode('utf8', 'replace')
        return s

    def __unicode__(self):
        return self.traceback


class ExecutePreprocessor(Preprocessor):
    """
    Executes all the cells in a notebook
    """

    timeout = Integer(30, allow_none=True,
        help=dedent(
            """
            The time to wait (in seconds) for output from executions.
            If a cell execution takes longer, an exception (TimeoutError
            on python 3+, RuntimeError on python 2) is raised.

            `None` or `-1` will disable the timeout. If `timeout_func` is set,
            it overrides `timeout`.
            """
        )
    ).tag(config=True)

    timeout_func = Any(
        default_value=None,
        allow_none=True,
        help=dedent(
            """
            A callable which, when given the cell source as input,
            returns the time to wait (in seconds) for output from cell
            executions. If a cell execution takes longer, an exception
            (TimeoutError on python 3+, RuntimeError on python 2) is
            raised.

            Returning `None` or `-1` will disable the timeout for the cell.
            Not setting `timeout_func` will cause the preprocessor to
            default to using the `timeout` trait for all cells. The
            `timeout_func` trait overrides `timeout` if it is not `None`.
            """
        )
    ).tag(config=True)

    interrupt_on_timeout = Bool(False,
        help=dedent(
            """
            If execution of a cell times out, interrupt the kernel and
            continue executing other cells rather than throwing an error and
            stopping.
            """
        )
    ).tag(config=True)

    allow_errors = Bool(False,
        help=dedent(
            """
            If `False` (default), when a cell raises an error the
            execution is stopped and a `CellExecutionError`
            is raised.
            If `True`, execution errors are ignored and the execution
            is continued until the end of the notebook. Output from
            exceptions is included in the cell output in both cases.
            """
        )
    ).tag(config=True)

    extra_arguments = List(Unicode())

    kernel_name = Unicode('',
        help=dedent(
            """
            Name of kernel to use to execute the cells.
            If not set, use the kernel_spec embedded in the notebook.
            """
        )
    ).tag(config=True)

    raise_on_iopub_timeout = Bool(False,
        help=dedent(
            """
            If `False` (default), then the kernel will continue waiting for
            iopub messages until it receives a kernel idle message, or until a
            timeout occurs, at which point the currently executing cell will be
            skipped. If `True`, then an error will be raised after the first
            timeout. This option generally does not need to be used, but may be
            useful in contexts where there is the possibility of executing
            notebooks with memory-consuming infinite loops.
            """
            )
    ).tag(config=True)

    iopub_timeout = Integer(4, allow_none=False,
        help=dedent(
            """
            The time to wait (in seconds) for IOPub output. This generally
            doesn't need to be set, but on some slow networks (such as CI
            systems) the default timeout might not be long enough to get all
            messages.
            """
        )
    ).tag(config=True)

    shutdown_kernel = Enum(['graceful', 'immediate'],
        default_value='graceful',
        help=dedent(
            """
            If `graceful` (default), then the kernel is given time to clean
            up after executing all cells, e.g., to execute its `atexit` hooks.
            If `immediate`, then the kernel is signaled to immediately
            terminate.
            """
            )
    ).tag(config=True)

    kernel_manager_class = Type(
        default_value='jupyter_client.manager.KernelManager',
        config=True,
        help='The kernel manager class to use.'
    )

    def preprocess(self, nb, resources):
        """
        Preprocess notebook executing each code cell.

        The input argument `nb` is modified in-place.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being executed.
        resources : dictionary
            Additional resources used in the conversion process. For example,
            passing ``{'metadata': {'path': run_path}}`` sets the
            execution path to ``run_path``.

        Returns
        -------
        nb : NotebookNode
            The executed notebook.
        resources : dictionary
            Additional resources used in the conversion process.
        """
        path = resources.get('metadata', {}).get('path', '')
        if path == '':
            path = None

        # from jupyter_client.manager import start_new_kernel

        def start_new_kernel(startup_timeout=60, kernel_name='python',
                             **kwargs):
            km = self.kernel_manager_class(kernel_name=kernel_name)
            km.start_kernel(**kwargs)
            kc = km.client()
            kc.start_channels()
            try:
                kc.wait_for_ready(timeout=startup_timeout)
            except RuntimeError:
                kc.stop_channels()
                km.shutdown_kernel()
                raise

            return km, kc

        kernel_name = nb.metadata.get('kernelspec', {}).get('name', 'python')
        if self.kernel_name:
            kernel_name = self.kernel_name
        self.log.info("Executing notebook with kernel: %s" % kernel_name)
        self.km, self.kc = start_new_kernel(
            kernel_name=kernel_name,
            extra_arguments=self.extra_arguments,
            cwd=path)
        self.kc.allow_stdin = False

        try:
            nb, resources = super(ExecutePreprocessor, self).preprocess(nb, resources)
        finally:
            self.kc.stop_channels()
            self.km.shutdown_kernel(now=self.shutdown_kernel == 'immediate')

        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Executes a single code cell. See base.py for details.

        To execute all cells see :meth:`preprocess`.
        """
        if cell.cell_type != 'code':
            return cell, resources

        outputs = self.run_cell(cell)
        cell.outputs = outputs

        if not self.allow_errors:
            for out in outputs:
                if out.output_type == 'error':
                    pattern = u"""\
                        An error occurred while executing the following cell:
                        ------------------
                        {cell.source}
                        ------------------

                        {out.ename}: {out.evalue}
                        """
                    msg = dedent(pattern).format(out=out, cell=cell)
                    raise CellExecutionError(msg)
        return cell, resources


    def run_cell(self, cell):
        msg_id = self.kc.execute(cell.source)
        self.log.debug("Executing cell:\n%s", cell.source)
        # wait for finish, with timeout
        while True:
            try:
                if self.timeout_func is not None:
                    timeout = self.timeout_func(cell)
                else:
                    timeout = self.timeout

                if not timeout or timeout < 0:
                    timeout = None
                msg = self.kc.shell_channel.get_msg(timeout=timeout)
            except Empty:
                self.log.error(
                    "Timeout waiting for execute reply (%is)." % self.timeout)
                if self.interrupt_on_timeout:
                    self.log.error("Interrupting kernel")
                    self.km.interrupt_kernel()
                    break
                else:
                    try:
                        exception = TimeoutError
                    except NameError:
                        exception = RuntimeError
                    raise exception("Cell execution timed out")

            if msg['parent_header'].get('msg_id') == msg_id:
                break
            else:
                # not our reply
                continue

        outs = []

        while True:
            try:
                # We've already waited for execute_reply, so all output
                # should already be waiting. However, on slow networks, like
                # in certain CI systems, waiting < 1 second might miss messages.
                # So long as the kernel sends a status:idle message when it
                # finishes, we won't actually have to wait this long, anyway.
                msg = self.kc.iopub_channel.get_msg(timeout=self.iopub_timeout)
            except Empty:
                self.log.warn("Timeout waiting for IOPub output")
                if self.raise_on_iopub_timeout:
                    raise RuntimeError("Timeout waiting for IOPub output")
                else:
                    break
            if msg['parent_header'].get('msg_id') != msg_id:
                # not an output from our execution
                continue

            msg_type = msg['msg_type']
            self.log.debug("output: %s", msg_type)
            content = msg['content']

            # set the prompt number for the input and the output
            if 'execution_count' in content:
                cell['execution_count'] = content['execution_count']

            if msg_type == 'status':
                if content['execution_state'] == 'idle':
                    break
                else:
                    continue
            elif msg_type == 'execute_input':
                continue
            elif msg_type == 'clear_output':
                outs = []
                continue
            elif msg_type.startswith('comm'):
                continue

            try:
                out = output_from_msg(msg)
            except ValueError:
                self.log.error("unhandled iopub msg: " + msg_type)
            else:
                outs.append(out)

        return outs
