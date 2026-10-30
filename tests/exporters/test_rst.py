"""Tests for RSTExporter"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
import tempfile
from pathlib import Path

import nbformat
from nbformat import v4

from nbconvert.exporters.rst import RSTExporter
from tests.testutils import onlyif_cmds_exist

from .base import ExportersTestsBase


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

    def test_image_paths_use_posix_separators(self):
        """Image paths should use POSIX separators, not URL-encoded ones (GH-765)."""
        nb = v4.new_notebook()
        cell = v4.new_code_cell("print('hello')")
        cell.outputs = [
            v4.new_output(
                "display_data",
                data={
                    "image/png": (
                        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
                        "YAAAAAYAAjCB0C8AAAAASUVORK5CYII="
                    ),
                    "text/plain": "<Figure>",
                },
                metadata={"image/png": {"width": 1, "height": 1}},
            )
        ]
        nb.cells.append(cell)

        with tempfile.TemporaryDirectory() as tmp:
            notebook = Path(tmp) / "image.ipynb"
            nbformat.write(nb, notebook)
            output, _resources = RSTExporter().from_filename(
                notebook, resources={"output_files_dir": "image_files"}
            )

        match = re.search(r"\.\. image:: (.+)", output)
        assert match is not None
        image_path = match.group(1)
        assert image_path.startswith("image_files/")
        assert "%5C" not in image_path
