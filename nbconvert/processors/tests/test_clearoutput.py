"""
Module with tests for the clearoutput Processor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import ProcessorTestsBase
from ..clearoutput import ClearOutputProcessor


class TestClearOutput(ProcessorTestsBase):
    """Contains test functions for clearoutput.py"""

    def build_notebook(self):
        notebook = super().build_notebook()
        # Add a test field to the first cell
        if 'metadata' not in notebook.cells[0]:
            notebook.cells[0].metadata = {}
        notebook.cells[0].metadata['test_field'] = 'test_value'
        return notebook

    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = ClearOutputProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a ClearOutputProcessor be constructed?"""
        self.build_processor()

    def test_output(self):
        """Test the output of the ClearOutputProcessor"""
        for remove_test_field in [False, True]:
            nb = self.build_notebook()
            res = self.build_resources()
            Processor = self.build_processor()
            # Also remove the test field in addition to defaults
            if remove_test_field:
                Processor.remove_metadata_fields.add('test_field')
            nb, res = Processor(nb, res)
            assert nb.cells[0].outputs == []
            assert nb.cells[0].execution_count is None
            if 'metadata' in nb.cells[0]:
                for field in Processor.remove_metadata_fields:
                    assert field not in nb.cells[0].metadata
                # Ensure the test field is only removed when added to the traitlet
                assert remove_test_field or 'test_field' in nb.cells[0].metadata
