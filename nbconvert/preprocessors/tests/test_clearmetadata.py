"""
Module with tests for the clearmetadata preprocessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import PreprocessorTestsBase
from ..clearmetadata import ClearMetadataPreprocessor


class TestClearMetadata(PreprocessorTestsBase):
    """Contains test functions for clearmetadata.py"""

    def build_notebook(self):
        notebook = super().build_notebook()
        notebook.metadata = {'language': 'python'}
        # Add a test field to the first cell
        if 'metadata' not in notebook.cells[0]:
            notebook.cells[0].metadata = {}
        notebook.cells[0].metadata['test_field'] = 'test_value'
        notebook.cells[0].metadata['executeTime'] = dict([('end_time', '09:31:50'), 
                                                    ('start_time', '09:31:49')])
        return notebook

    def build_preprocessor(self, **kwargs):
        """Make an instance of a preprocessor"""
        preprocessor = ClearMetadataPreprocessor(**kwargs)
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a ClearMetadataPreprocessor be constructed?"""
        self.build_preprocessor()

    def test_default_output(self):
        """Test the output of the ClearMetadataPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        assert not nb.cells[0].metadata 
        assert not nb.metadata 

    def test_cell_only(self):
        """Test the output of the ClearMetadataPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor(clear_notebook_metadata=False)
        nb, res = preprocessor(nb, res)

        assert not nb.cells[0].metadata 
        assert nb.metadata

    def test_selective_cell_metadata(self):
        """Test the output of the ClearMetadataPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor(preserve_metadata_keys=['test_field'])
        nb, res = preprocessor(nb, res)

        assert nb.cells[0].metadata == { 'test_field': 'test_value' }
        assert not nb.metadata

    def test_selective_notebook_metadata(self):
        """Test the output of the ClearMetadataPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor(preserve_metadata_keys=['language'])
        nb, res = preprocessor(nb, res)

        assert not nb.cells[0].metadata
        assert nb.metadata == { 'language': 'python' }
