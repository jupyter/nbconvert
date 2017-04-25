"""
Module with tests for the RemoveEmptyPreprocessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbformat import v4 as nbformat

from .base import PreprocessorTestsBase
from ..removeempty import RemoveEmptyPreprocessor


class TestRemoveEmpty(PreprocessorTestsBase):
    """Contains test functions for removeempty.py"""

    def build_notebook(self):
        notebook = super(TestRemoveEmpty, self).build_notebook()
        # Add a few empty cells
        notebook.cells.extend([
            nbformat.new_code_cell(),
            nbformat.new_markdown_cell(),
            nbformat.new_raw_cell()
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
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        for cell in nb.cells:
            assert cell.source.strip(), "found unexpected empty cell"
