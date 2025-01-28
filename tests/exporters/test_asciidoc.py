"""Tests for ASCIIDocExporter`"""

# -----------------------------------------------------------------------------
# Copyright (c) 2016, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import re

from traitlets.config import Config

from nbconvert.exporters.asciidoc import ASCIIDocExporter
from tests.testutils import onlyif_cmds_exist

from .base import ExportersTestsBase

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
in_regex = r"In\[(.*)\]:"
out_regex = r"Out\[(.*)\]:"


class TestASCIIDocExporter(ExportersTestsBase):
    """Tests for ASCIIDocExporter"""

    exporter_class = ASCIIDocExporter  # type:ignore

    def test_constructor(self):
        """
        Can a ASCIIDocExporter be constructed?
        """
        ASCIIDocExporter()

    @onlyif_cmds_exist("pandoc")
    def test_export(self):
        """
        Can a ASCIIDocExporter export something?
        """
        (output, resources) = ASCIIDocExporter().from_filename(self._get_notebook())
        assert len(output) > 0

        assert re.findall(in_regex, output)
        assert re.findall(out_regex, output)

        # Assert that the Markdown header from our test notebook made it into the output.
        # This can fail when nbconvert invokes pandoc incorrectly, as in issue #2017.
        assert "== NumPy and Matplotlib examples" in output

    @onlyif_cmds_exist("pandoc")
    def test_export_no_prompt(self):
        """
        Can a ASCIIDocExporter export something without prompts?
        """
        no_prompt = {
            "TemplateExporter": {
                "exclude_input_prompt": True,
                "exclude_output_prompt": True,
            }
        }
        c_no_prompt = Config(no_prompt)
        exporter = ASCIIDocExporter(config=c_no_prompt)
        (output, resources) = exporter.from_filename(
            self._get_notebook(nb_name="prompt_numbers.ipynb")
        )

        assert not re.findall(in_regex, output)
        assert not re.findall(out_regex, output)
