"""Tests for RSTExporter"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from base64 import b64encode
from copy import deepcopy
from pathlib import Path

import nbformat
import pytest
from nbformat import v4
from traitlets.config import Config

from nbconvert.exporters.rst import RSTExporter
from nbconvert.writers.files import FilesWriter
from tests.testutils import onlyif_cmds_exist

from .base import ExportersTestsBase


@onlyif_cmds_exist("pandoc")
@pytest.mark.parametrize("output_files_dir", ["", "notebook_files"])
@pytest.mark.parametrize("use_separate_dir", [False, True])
def test_export_attachments(tmp_path, output_files_dir, use_separate_dir):
    """RST image references resolve to files containing the original attachment bytes."""
    images = {
        "red.svg": (
            "image/svg+xml",
            b'<svg xmlns="http://www.w3.org/2000/svg"><circle r="1" fill="red"/></svg>',
        ),
        "image.png": (
            "image/png",
            (Path(__file__).parent.parent / "files" / "testimage.png").read_bytes(),
        ),
    }
    nb = v4.new_notebook(
        cells=[
            v4.new_markdown_cell(
                source=f"![{name}](attachment:{name})",
                attachments={name: {mimetype: b64encode(data).decode("ascii")}},
            )
            for name, (mimetype, data) in images.items()
        ]
    )
    original_nb = deepcopy(nb)
    config = Config({"ExtractAttachmentsPreprocessor": {"use_separate_dir": use_separate_dir}})
    output, resources = RSTExporter(config=config).from_notebook_node(
        nb, resources={"output_files_dir": output_files_dir, "unique_key": "notebook"}
    )
    destination = FilesWriter(build_directory=str(tmp_path)).write(
        output, resources, notebook_name="notebook"
    )

    assert destination.read_text(encoding="utf-8") == output
    assert "attachment:" not in output
    assert nb == original_nb
    directory = "notebook_attachments" if use_separate_dir else output_files_dir
    for name, (_mimetype, data) in images.items():
        relative_path = f"{directory}/{name}" if directory else name
        assert f".. figure:: {relative_path}\n" in output
        assert (tmp_path / relative_path).read_bytes() == data


@onlyif_cmds_exist("pandoc")
def test_export_attachments_disabled():
    """Explicitly disabling attachment extraction keeps the original references."""
    nb = v4.new_notebook(
        cells=[
            v4.new_markdown_cell(
                source="![image](attachment:image.png)",
                attachments={"image.png": {"image/png": b64encode(b"image").decode("ascii")}},
            )
        ]
    )
    config = Config({"ExtractAttachmentsPreprocessor": {"enabled": False}})
    output, resources = RSTExporter(config=config).from_notebook_node(nb)

    assert ".. figure:: attachment:image.png\n" in output
    assert not resources["outputs"]
    assert not resources.get("attachments")


class TestRSTExporter(ExportersTestsBase):
    """Tests for RSTExporter"""

    exporter_class = RSTExporter  # type:ignore
    should_include_raw = ["rst"]  # type:ignore

    def test_constructor(self):
        """
        Can a RSTExporter be constructed?
        """
        RSTExporter()

    @onlyif_cmds_exist("pandoc")
    def test_export(self):
        """
        Can a RSTExporter export something?
        """
        (output, _resources) = RSTExporter().from_filename(self._get_notebook())
        assert len(output) > 0

    @onlyif_cmds_exist("pandoc")
    def test_empty_code_cell(self):
        """No empty code cells in rst"""
        nbname = self._get_notebook()
        with open(nbname, encoding="utf8") as f:
            nb = nbformat.read(f, 4)

        nb = v4.upgrade(nb)
        exporter = self.exporter_class()  # type:ignore

        (output, _resources) = exporter.from_notebook_node(nb)
        # add an empty code cell
        nb.cells.append(v4.new_code_cell(source=""))

        (output2, _resources) = exporter.from_notebook_node(nb)
        # adding an empty code cell shouldn't change output
        self.assertEqual(output.strip(), output2.strip())

    @onlyif_cmds_exist("pandoc")
    def test_png_metadata(self):
        """
        Does RSTExporter treat pngs with width/height metadata correctly?
        """
        (output, _resources) = RSTExporter().from_filename(
            self._get_notebook(nb_name="pngmetadata.ipynb")
        )
        assert len(output) > 0
        check_for_png = re.compile(r".. image::.*?\n\s+(.*?)\n\s*\n", re.DOTALL)
        result = check_for_png.search(output)
        assert result is not None
        attr_string = result.group(1)
        assert ":width:" in attr_string
        assert ":height:" in attr_string
        assert "px" in attr_string

    def test_rst_output(self):
        """
        Is native text/x-rst output included when converting
        """
        (output, _resources) = RSTExporter().from_filename(
            self._get_notebook(nb_name="rst_output.ipynb")
        )
        assert len(output) > 0
        assert "\n.. note::" in output
        assert ".. raw:: html" not in output  # rst should shadow html output
