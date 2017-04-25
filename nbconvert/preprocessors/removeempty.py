"""Module containing a preprocessor that removes empty cells"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import Set
from .base import Preprocessor

class RemoveEmptyPreprocessor(Preprocessor):
    """
    Removes blank cells from a notebook.
    """

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        nb.cells = [cell for cell in nb.cells if cell.source.strip()]
        return nb, resources
