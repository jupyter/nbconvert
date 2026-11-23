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

import pytest
from nbformat.v4 import new_markdown_cell, new_notebook

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


@pytest.mark.parametrize(
    ("metadata", "frontmatter"),
    [
        ({"lang": "pl"}, '---\nlang: "pl"\n---\n\n'),
        ({"lang": "pt-BR", "language": "python"}, '---\nlang: "pt-BR"\n---\n\n'),
        ({"language": "python"}, ""),
        ({"lang": " "}, ""),
        ({"lang": ["pl"]}, ""),
    ],
)
def test_export_document_language(metadata, frontmatter):
    notebook = new_notebook(metadata=metadata, cells=[new_markdown_cell("# Heading")])

    output, _ = MarkdownExporter().from_notebook_node(notebook)

    assert output == frontmatter + "# Heading\n"


def test_export_document_language_after_pandoc_title():
    notebook = new_notebook(
        metadata={"lang": "pl"},
        cells=[new_markdown_cell("% Title\n% Author\n\n# Heading")],
    )

    output, _ = MarkdownExporter().from_notebook_node(notebook)

    assert output == '% Title\n% Author\n\n---\nlang: "pl"\n---\n\n# Heading\n'
