"""Module containing a preprocessor that removes the outputs from code cells"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from textwrap import dedent

try:
    from queue import Empty  # Py 3
except ImportError:
    from Queue import Empty  # Py 2

from traitlets import List, Unicode, Bool

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


class ExecutePreprocessor(Preprocessor):
    """
    Executes all the cells in a notebook
    """

    timeout = Integer(30, config=True,
        help="The time to wait (in seconds) for output from executions."
    )

    interrupt_on_timeout = Bool(
        False, config=True,
        help=dedent(
            """
            If execution of a cell times out, interrupt the kernel and
            continue executing other cells rather than throwing an error and
            stopping.
            """
        )
    )

    allow_errors = Bool(
        False, config=True,
        help=dedent(
            """
            If `True`, a `CellExecutionError` is raised if any of the notebook
            cells raises an exception during execution. Otherwise, execution
            is continued and the output from the exception is included in the
            cell output.
            """
        )
    )

    extra_arguments = List(Unicode())

    def preprocess(self, nb, resources):
        path = resources.get('metadata', {}).get('path', '')
        if path == '':
            path = None

        from jupyter_client.manager import start_new_kernel
        kernel_name = nb.metadata.get('kernelspec', {}).get('name', 'python')
        self.log.info("Executing notebook with kernel: %s" % kernel_name)
        self.km, self.kc = start_new_kernel(
            kernel_name=kernel_name,
            extra_arguments=self.extra_arguments,
            stderr=open(os.devnull, 'w'),
            cwd=path)
        self.kc.allow_stdin = False

        try:
            nb, resources = super(ExecutePreprocessor, self).preprocess(nb, resources)
        finally:
            self.kc.stop_channels()
            self.km.shutdown_kernel(now=True)

        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each code cell. See base.py for details.
        """
        if cell.cell_type != 'code':
            return cell, resources

        outputs = self.run_cell(cell)
        cell.outputs = outputs

        if not self.allow_errors:
            for out in outputs:
                if out.output_type == 'error':
                    pattern = """\
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
                msg = self.kc.shell_channel.get_msg(timeout=self.timeout)
            except Empty:
                self.log.error("""Timeout waiting for execute reply (%is).
                If your cell should take longer than this, you can increase the timeout with:

                    c.ExecutePreprocessor.timeout = SECONDS

                in jupyter_nbconvert_config.py
                """ % self.timeout)
                if self.interrupt_on_timeout:
                    self.log.error("Interrupting kernel")
                    self.km.interrupt_kernel()
                    break
                else:
                    try:
                        exception = TimeoutError
                    except NameError:
                        exception = RuntimeError
                    raise exception("Cell execution timed out, see log"
                                    " for details.")

            if msg['parent_header'].get('msg_id') == msg_id:
                break
            else:
                # not our reply
                continue

        outs = []

        while True:
            try:
                msg = self.kc.iopub_channel.get_msg(timeout=self.timeout)
            except Empty:
                self.log.warn("Timeout waiting for IOPub output")
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
