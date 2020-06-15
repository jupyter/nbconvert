"""Tests for the HighlightMagics Processor"""

from .base import ProcessorTestsBase
from ..highlightmagics import HighlightMagicsProcessor


class TestHighlightMagics(ProcessorTestsBase):
    """Contains test functions for highlightmagics.py"""


    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = HighlightMagicsProcessor()
        Processor.enabled = True
        return Processor

    def test_constructor(self):
        """Can a HighlightMagicsProcessor be constructed?"""
        self.build_processor()

    def test_tagging(self):
        """Test the HighlightMagicsProcessor tagging"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        nb.cells[0].source = """%%R -i x,y -o XYcoef
            lm.fit <- lm(y~x)
            par(mfrow=c(2,2))
            print(summary(lm.fit))
            plot(lm.fit)
            XYcoef <- coef(lm.fit)"""

        nb, res = Processor(nb, res)

        assert('magics_language' in nb.cells[0]['metadata'])

        self.assertEqual(nb.cells[0]['metadata']['magics_language'], 'r')

    def test_no_false_positive(self):
        """Test that HighlightMagicsProcessor does not tag false positives"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        nb.cells[0].source = """# this should not be detected
                print(\"""
                %%R -i x, y
                \""")"""
        nb, res = Processor(nb, res)

        assert('magics_language' not in nb.cells[0]['metadata'])