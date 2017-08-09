"""
Module with tests for the TagRemoveInputSieve.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbformat import v4 as nbformat

from .base import SieveTestsBase
from .. import TagRemoveInputSieve


class TestTagRemoveInput(SieveTestsBase):
    """Contains test functions for tagremove.py"""

    def build_notebook(self):
        """
        Build a notebook to have metadata tags for input filtering.
        """
        notebook = super(TestTagRemoveInput, self).build_notebook()

        outputs_to_be_kept = [
            nbformat.new_output("stream",
                                name="stdout",
                                text="remove_my_output",
                                ),
        ]

        notebook.cells.extend(
            [nbformat.new_markdown_cell(source="move_my_output')",
                                        metadata={"tags": ["hide_this_input"]},
                                        ),

             nbformat.new_code_cell(source="print('remove this cell')",
                                    execution_count=3,
                                    outputs=outputs_to_be_kept,
                                    metadata={"tags": ["hide_this_input"]},
                                    ),
             ]
            )

        return notebook

    def build_sieve(self):
        """Make an instance of a sieve"""
        sieve = TagRemoveInputSieve()
        sieve.enabled = True
        return sieve

    def test_constructor(self):
        """Can a TagRemoveSieve be constructed?"""
        self.build_sieve()

    def test_output(self):
        """Test the output of the TagRemoveSieve"""
        nb = self.build_notebook()
        res = self.build_resources()
        sieve = self.build_sieve()
        sieve.remove_input_tags.add("hide_this_input")

        nb, res = sieve(nb, res)

        # checks that we can remove source from code cells
        self.assertEqual(nb.cells[-1].transient.get("remove_source", False), True)

        # checks that we can remove source from markdown
        self.assertEqual(nb.cells[-2].transient.get("remove_source", False), True)


