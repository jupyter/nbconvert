"""Tests for MarkdownExporter"""

# -----------------------------------------------------------------------------
# Copyright (c) 2013, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from nbformat import v4

from nbconvert.exporters.markdown import MarkdownExporter

from .base import ExportersTestsBase

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------


class TestMarkdownExporter(ExportersTestsBase):
    """Tests for MarkdownExporter"""

    exporter_class = MarkdownExporter  # type:ignore
    should_include_raw = ["markdown", "html"]  # type:ignore

    def test_constructor(self):
        """
        Can a MarkdownExporter be constructed?
        """
        MarkdownExporter()

    def test_export(self):
        """
        Can a MarkdownExporter export something?
        """
        (output, _resources) = MarkdownExporter().from_filename(self._get_notebook())
        assert len(output) > 0

    def test_stream_ansi_is_stripped(self):
        """ANSI escape codes in stream output are not emitted as Markdown."""
        notebook = v4.new_notebook(
            cells=[v4.new_code_cell(outputs=[v4.new_output("stream", text="\x1b[31mred\x1b[0m\n")])]
        )

        output, _resources = MarkdownExporter().from_notebook_node(notebook)

        assert "\x1b[" not in output
        assert "red" in output
