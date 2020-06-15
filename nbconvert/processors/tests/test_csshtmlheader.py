"""
Module with tests for the csshtmlheader Processor
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from .base import ProcessorTestsBase
from ..csshtmlheader import CSSHTMLHeaderProcessor


#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

class TestCSSHTMLHeader(ProcessorTestsBase):
    """Contains test functions for csshtmlheader.py"""


    def build_processor(self):
        """Make an instance of a Processor"""
        Processor = CSSHTMLHeaderProcessor()
        Processor.enabled = True
        return Processor


    def test_constructor(self):
        """Can a CSSHTMLHeaderProcessor be constructed?"""
        self.build_processor()
    

    def test_output(self):
        """Test the output of the CSSHTMLHeaderProcessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        Processor = self.build_processor()
        nb, res = Processor(nb, res)
        assert 'css' in res['inlining'] 
