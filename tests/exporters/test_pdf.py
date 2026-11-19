"""Tests for PDF export"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import shutil
import textwrap
from tempfile import TemporaryDirectory

from nbformat import v4, write

from nbconvert.exporters.pdf import PDFExporter
from nbconvert.utils import _contextlib_chdir
from tests.testutils import onlyif_cmds_exist

from .base import ExportersTestsBase

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------


class TestPDF(ExportersTestsBase):
    """Test PDF export"""

    exporter_class = PDFExporter  # type:ignore

    def test_constructor(self):
        """Can a PDFExporter be constructed?"""
        self.exporter_class()  # type:ignore

    @onlyif_cmds_exist("xelatex", "pandoc")
    def test_export(self):
        """Smoke test PDFExporter"""
        with TemporaryDirectory() as td:
            file_name = os.path.basename(self._get_notebook())
            newpath = os.path.join(td, file_name)
            shutil.copy(self._get_notebook(), newpath)
            (output, _resources) = self.exporter_class(latex_count=1).from_filename(  # type:ignore
                newpath
            )
            self.assertIsInstance(output, bytes)
            assert len(output) > 0
            # all temporary file should be cleaned up
            assert {file_name} == set(os.listdir(td))

    @onlyif_cmds_exist("xelatex", "pandoc")
    def test_captionless_markdown_table(self):
        """
        Captionless Markdown tables must PDF-build with modern pandoc/longtable.

        Pandoc sets \\LTcaptype to none; without \\newcounter{none} in the
        template, xelatex fails with ``No counter 'none' defined``.
        """
        table = textwrap.dedent(
            """\
            | Name | Value |
            | --- | --- |
            | a | 1 |
            """
        )
        nb = v4.new_notebook(cells=[v4.new_markdown_cell(source=table)])
        with TemporaryDirectory() as td:
            nbfile = os.path.join(td, "captionless_table.ipynb")
            with open(nbfile, "w", encoding="utf-8") as f:
                write(nb, f, 4)
            (output, _resources) = self.exporter_class(latex_count=1).from_filename(  # type:ignore
                nbfile
            )
            self.assertIsInstance(output, bytes)
            assert len(output) > 0

    @onlyif_cmds_exist("xelatex", "pandoc")
    def test_texinputs(self):
        """
        Is TEXINPUTS set properly when we are converting
        - in the same directory, and
        - in a different directory?
        """
        with TemporaryDirectory() as td, _contextlib_chdir.chdir(td):
            os.mkdir("folder")
            file_name = os.path.basename(self._get_notebook())
            nb1 = os.path.join(td, file_name)
            nb2 = os.path.join(td, "folder", file_name)
            ex1 = self.exporter_class(latex_count=1)  # type:ignore
            ex2 = self.exporter_class(latex_count=1)  # type:ignore
            shutil.copy(self._get_notebook(), nb1)
            shutil.copy(self._get_notebook(), nb2)
            _ = ex1.from_filename(nb1)
            _ = ex2.from_filename(nb2)
            assert ex1.texinputs == os.path.abspath(".")
            assert ex2.texinputs == os.path.abspath("./folder")
