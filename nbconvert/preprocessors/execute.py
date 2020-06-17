"""Module containing a preprocessor that executes the code cells
and updates outputs"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.
from nbclient import NotebookClient, execute as _execute
# Backwards compatability for imported name
from nbclient.exceptions import CellExecutionError

from .base import Preprocessor


def executenb(*args, **kwargs):
    from warnings import warn
    warn("The 'nbconvert.preprocessors.execute.executenb' function was moved to nbclient.execute. "
        "We recommend importing that library directly.",
        FutureWarning)
    return _execute(*args, **kwargs)


# We inherit from both classes to allow for traitlets to resolve as they did pre-6.0.
# This unfortunatley makes for some ugliness around initialization as NotebookClient
# assumes it's a constructed class with a nb object that we have to hack around.
class ExecutePreprocessor(Preprocessor, NotebookClient):
    """
    Executes all the cells in a notebook
    """

    def __init__(self, **kw):
        nb = kw.get('nb')
        Preprocessor.__init__(self, nb=nb, **kw)
        NotebookClient.__init__(self, nb, **kw)

    def preprocess(self, nb, resources=None, km=None):
        """
        Preprocess notebook executing each code cell.

        The input argument *nb* is modified in-place.

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
        # Copied from NotebookClient init :/
        self.nb = nb
        self.km = km
        if resources:
            self.resources = resources
        self.reset_execution_trackers()
        self.execute()
        return nb, resources
