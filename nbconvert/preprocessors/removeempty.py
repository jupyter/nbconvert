"""Module containing a preprocessor that removes empty cells"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from traitlets import Unicode
from .base import Preprocessor

class RemoveEmptyPreprocessor(Preprocessor):
    """
    Removes empty cells from a notebook, where "empty" is defined
    by the regular expression traitlet `empty_pattern`.
    """

    empty_pattern = Unicode(r"\s*")

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        empty_pattern = re.compile(self.empty_pattern)
        nb.cells = [cell for cell in nb.cells
                    if not empty_pattern.fullmatch(cell.source)]
        return nb, resources
