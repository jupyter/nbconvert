"""
Module with tests for the TagRemoveProcessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbformat import v4 as nbformat

from .base import ProcessorTestsBase
from ..tagremove import TagRemoveProcessor


class TestTagRemove(ProcessorTestsBase):
    """Contains test functions for tagremove.py"""

    def build_notebook(self):
        """
        Build a notebook to have metadata tags for cells, output_areas, and
        individual outputs.
        """
        notebook = super().build_notebook()
        # Add a few empty cells
        notebook.cells[0].outputs.extend(
            [nbformat.new_output("display_data",
                                 data={'text/plain': 'i'},
                                 metadata={'tags': ["hide_one_output"]}
                                 ),
             ])
        outputs_to_be_removed = [
            nbformat.new_output("display_data",
                                data={'text/plain': "remove_my_output"}),
        ]
        outputs_to_be_kept = [
            nbformat.new_output("stream",
                                name="stdout",
                                text="remove_my_output",
                                ),
        ]
        notebook.cells.extend(
            [nbformat.new_code_cell(source="display('remove_my_output')",
                                    execution_count=2,
                                    outputs=outputs_to_be_removed,
                                    metadata={"tags": ["hide_all_outputs"]}),

             nbformat.new_code_cell(source="print('remove this cell')",
                                    execution_count=3,
                                    outputs=outputs_to_be_kept,
                                    metadata={"tags": ["hide_this_cell"]}),
             ]
            )

        return notebook

    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = TagRemoveProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a TagRemoveProcessor be constructed?"""
        self.build_processor()

    def test_output(self):
        """Test the output of the TagRemoveProcessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        Processor.remove_cell_tags.add("hide_this_cell")
        Processor.remove_all_outputs_tags.add('hide_all_outputs')
        Processor.remove_single_output_tags.add('hide_one_output')

        nb, res = Processor(nb, res)

        # checks that we can remove entire cells
        self.assertEqual(len(nb.cells), 3)

        # checks that we can remove output areas
        self.assertEqual(len(nb.cells[-1].outputs), 0)

        # checks that we can remove individual outputs
        self.assertEqual(len(nb.cells[0].outputs), 8)
