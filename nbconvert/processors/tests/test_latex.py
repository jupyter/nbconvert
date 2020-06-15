"""Tests for the latex Processor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import ProcessorTestsBase
from ..latex import LatexProcessor


class TestLatex(ProcessorTestsBase):
    """Contains test functions for latex.py"""


    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = LatexProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a LatexProcessor be constructed?"""
        self.build_processor()
        

    def test_output(self):
        """Test the output of the LatexProcessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        nb, res = Processor(nb, res)

        # Make sure the code cell wasn't modified.
        self.assertEqual(nb.cells[0].source, '$ e $')

        # Verify that the markdown cell wasn't processed.
        self.assertEqual(nb.cells[1].source, '$ e $')
    
    def test_highlight(self):
        """Check that highlighting style can be changed"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()

        # Set the style to a known builtin that's not the default
        Processor.style='colorful'
        nb, res = Processor(nb, res)
        style_defs = res['latex']['pygments_definitions']

        # Get the default
        from pygments.formatters import LatexFormatter
        default_defs = LatexFormatter(style='default').get_style_defs()

        # Verify that the style was in fact changed
        assert style_defs != default_defs
