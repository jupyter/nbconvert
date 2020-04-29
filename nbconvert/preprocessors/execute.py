"""Module containing a preprocessor that executes the code cells
and updates outputs"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.
from nbclient import NotebookClient
from textwrap import dedent
from traitlets import Bool

from .base import Preprocessor


# We inherit from both classes to allow for traitlets to resolve as they did
# pre-6.0.  This unfortunatley makes for some ugliness around initialization as
# NotebookClient assumes it's a constructed class with a nb object that we have
# to hack around.
class ExecutePreprocessor(Preprocessor):
    """
    Executes all the cells in a notebook
    """

    allow_errors = Bool(
        False,
        help=dedent(
            """
            If `False` (default), when a cell raises an error the
            execution is stopped and a `CellExecutionError`
            is raised.
            If `True`, execution errors are ignored and the execution
            is continued until the end of the notebook. Output from
            exceptions is included in the cell output in both cases.
            """
        ),
    ).tag(config=True)

    def preprocess(self, nb, resources=None, km=None, timeout=600, **kw):
        """
        Preprocess notebook executing each code cell.

        The input argument `nb` is modified in-place.

        Parameters
        ----------
        nb : NotebookNode
            Notebook being executed.
        resources : dictionary (optional)
            Additional resources used in the conversion process. For example,
            passing ``{'metadata': {'path': run_path}}`` sets the
            execution path to ``run_path``.
        km: KernelManager (optional)
            Optional kernel manager. If none is provided, a kernel manager will
            be created.

        Returns
        -------
        nb : NotebookNode
            The executed notebook.
        resources : dictionary
            Additional resources used in the conversion process.
        """
        if resources is None:
            resources = {}

        nb_client = NotebookClient(
            nb,
            timeout=timeout,
            resources=resources,
            allow_errors=self.allow_errors,
            **kw
        )

        nb_client.reset_execution_trackers()
        nb_client.execute()
        return nb, resources
