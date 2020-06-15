"""
Module with tests for the RegexRemoveProcessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from nbformat import v4 as nbformat, from_dict

from .base import ProcessorTestsBase
from ..regexremove import RegexRemoveProcessor


class TestRegexRemove(ProcessorTestsBase):
    """Contains test functions for regexremove.py"""

    def build_notebook(self):
        notebook = super().build_notebook()
        # Add a few empty cells
        notebook.cells.extend([
            nbformat.new_code_cell(''),
            nbformat.new_markdown_cell(' '),
            nbformat.new_raw_cell('\n'),
            nbformat.new_raw_cell('\t'),
        ])

        return notebook

    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = RegexRemoveProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a RegexRemoveProcessor be constructed?"""
        self.build_processor()

    def test_output(self):
        """Test the output of the RegexRemoveProcessor"""
        pattern_lookup = {
            'disallow_whitespace': [r'\s*\Z'],
            'disallow_tab_newline': [r'\t\Z', r'\n\Z']
        }
        expected_cell_count = {
            'default': 6,  # nothing is removed
            'disallow_whitespace': 2,  # all "empty" cells are removed
            'disallow_tab_newline': 4,  # cells with tab and newline are removed
            'none': 6,
        }
        for method in ['default', 'disallow_whitespace', 'disallow_tab_newline', 'none']:
            nb = self.build_notebook()
            res = self.build_resources()

            # Build the Processor and extend the list of patterns or use an empty list
            Processor = self.build_processor()
            if method == 'none':
                Processor.patterns = []
            else:
                Processor.patterns.extend(pattern_lookup.get(method, []))
            nb, res = Processor(nb, res)

            self.assertEqual(len(nb.cells), expected_cell_count[method])

            # Make sure none of the cells match the pattern
            patterns = list(map(re.compile, Processor.patterns))
            for cell in nb.cells:
                for pattern in patterns:
                    self.assertFalse(pattern.match(cell.source))

