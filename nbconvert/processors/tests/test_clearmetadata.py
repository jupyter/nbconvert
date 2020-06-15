"""
Module with tests for the clearmetadata Processor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import ProcessorTestsBase
from ..clearmetadata import ClearMetadataProcessor


class TestClearMetadata(ProcessorTestsBase):
    """Contains test functions for clearmetadata.py"""

    def build_notebook(self):
        notebook = super().build_notebook()
        # Add a test field to the first cell
        if 'metadata' not in notebook.cells[0]:
            notebook.cells[0].metadata = {}
        notebook.cells[0].metadata['test_field'] = 'test_value'
        notebook.cells[0].metadata['executeTime'] = dict([('end_time', '09:31:50'), 
                                                    ('start_time', '09:31:49')])
        return notebook

    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = ClearMetadataProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a ClearMetadataProcessor be constructed?"""
        self.build_processor()

    def test_output(self):
        """Test the output of the ClearMetadataProcessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        nb, res = Processor(nb, res)

        assert not nb.cells[0].metadata 
