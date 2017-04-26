"""
Module with tests for the RemoveEmptyPreprocessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from nbformat import v4 as nbformat

from .base import PreprocessorTestsBase
from ..removeempty import RemoveEmptyPreprocessor


class TestRemoveEmpty(PreprocessorTestsBase):
    """Contains test functions for removeempty.py"""

    def build_notebook(self):
        notebook = super(TestRemoveEmpty, self).build_notebook()
        # Add a few empty cells
        notebook.cells.extend([
            nbformat.new_code_cell(''),
            nbformat.new_markdown_cell(' '),
            nbformat.new_raw_cell('\n')
        ])

        return notebook

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = RemoveEmptyPreprocessor()
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a RemoveEmptyPreprocessor be constructed?"""
        self.build_preprocessor()

    def test_output(self):
        """Test the output of the RemoveEmptyPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()

        # Run one test that removes only strictly empty cells and
        # one test that also removes cells containing whitespace
        for keep_whitespace in [True, False]:
            preprocessor = self.build_preprocessor()
            # Keep only strictly empty cells
            if keep_whitespace:
                preprocessor.empty_pattern = r""
            nb, res = preprocessor(nb, res)

            if keep_whitespace:
                self.assertEqual(len(nb.cells), 4)
            else:
                self.assertEqual(len(nb.cells), 2)

            # Make sure none of the cells match the empty pattern
            pattern = re.compile(preprocessor.empty_pattern)
            for cell in nb.cells:
                self.assertFalse(pattern.fullmatch(cell.source))
