"""Module containing a preprocessor that removes empty cells"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from traitlets import Unicode
from .base import Preprocessor

class RegexRemovePreprocessor(Preprocessor):
    """
    Removes cells from a notebook that match a regular expression.
    """

    pattern = Unicode(r"\s*\Z", config=True)

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        pattern = re.compile(self.pattern)
        nb.cells = [cell for cell in nb.cells
                    if not pattern.match(cell.source)]
        return nb, resources
