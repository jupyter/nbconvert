"""
Module containing a preprocessor that removes cells if they match
one or more regular expression.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from traitlets import List, Unicode
from .base import Preprocessor

class RegexRemovePreprocessor(Preprocessor):
    """
    Removes cells from a notebook that match one or more regular expression.

    For each cell, the preprocessor checks whether its contents match
    the regular expressions in the `patterns` traitlet which is a list
    of unicode strings. If the contents match any of the patterns, the cell
    is removed from the notebook.

    By default, `patterns = [r'\Z']` which matches the empty string such that
    strictly empty cells are removed. To modify the list of matched patterns,
    modify the patterns traitlet. For example, execute the following command
    to convert a notebook to html and remove cells containing only whitespace:

    > jupyter nbconvert --RegexRemovePreprocessor.enabled=True \
      --RegexRemovePreprocessor.patterns="['\\s*\\Z']" mynotebook.ipynb

    The first command line argument enables the preprocessor and the second
    sets the list of patterns to '\\s*\\Z' which matches an arbitrary number
    of whitespace characters followed by the end of the string.

    See https://regex101.com/ for an interactive guide to regular expressions
    (make sure to select the python flavor). See
    https://docs.python.org/library/re.html for the official regular expression
    documentation in python.
    """

    patterns = List(Unicode, default_value=[r'\Z']).tag(config=True)

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        # Skip preprocessing if the list of patterns is empty
        if not self.patterns:
            return nb, resources
        # Compile all the patterns into one: each pattern is first wrapped
        # by a non-capturing group to ensure the correct order of precedence
        # and the patterns are joined with a logical or
        pattern = re.compile('|'.join('(?:%s)' % pattern
                             for pattern in self.patterns))
        # Filter out cells that match any of the patterns
        nb.cells = [cell for cell in nb.cells
                    if not pattern.match(cell.source)]
        return nb, resources
