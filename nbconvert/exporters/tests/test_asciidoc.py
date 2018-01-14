"""Tests for ASCIIDocExporter`"""

#-----------------------------------------------------------------------------
# Copyright (c) 2016, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import re

from traitlets.config import Config
from ipython_genutils.testing import decorators as dec

from .base import ExportersTestsBase
from ..asciidoc import ASCIIDocExporter

#-----------------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------------

class TestASCIIDocExporter(ExportersTestsBase):
    """Tests for ASCIIDocExporter"""

    exporter_class = ASCIIDocExporter

    def test_constructor(self):
        """
        Can a ASCIIDocExporter be constructed?
        """
        ASCIIDocExporter()


    @dec.onlyif_cmds_exist('pandoc')
    def test_export(self):
        """
        Can a ASCIIDocExporter export something?
        """
        (output, resources) = ASCIIDocExporter().from_filename(self._get_notebook())
        assert len(output) > 0
        
    @dec.onlyif_cmds_exist('pandoc')
    def test_export(self):
        """
        Can a ASCIIDocExporter export something?
        """
        no_prompt = {
            "TemplateExporter":{
                "exclude_input_prompt": True,
                "exclude_output_prompt": True,
            }
        }
        c_no_prompt = Config(no_prompt)
        exporter = ASCIIDocExporter(config=c_no_prompt)
        (output, resources) = exporter.from_filename(
            self._get_notebook(nb_name="prompt_numbers.ipynb"))
            
        in_regex = r"In&nbsp;\[(.*)\]:"
        out_regex = r"Out\[(.*)\]:"

        assert not re.findall(in_regex, output)
        assert not re.findall(out_regex, output)
