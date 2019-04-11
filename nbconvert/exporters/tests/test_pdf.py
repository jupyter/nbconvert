"""Tests for PDF export"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import os
import logging
import shutil

from testpath import tempdir

from .base import ExportersTestsBase
from ..pdf import PDFExporter, LatexFailed
from ...utils.io import sensitive_filename_cleanup
from ...tests.utils import onlyif_cmds_exist


class TestPDF(ExportersTestsBase):
    """Test PDF export"""

    exporter_class = PDFExporter

    def test_constructor(self):
        """Can a PDFExporter be constructed?"""
        self.exporter_class()


    @onlyif_cmds_exist('xelatex', 'pandoc')
    def test_export(self):
        """Smoke test PDFExporter"""
        with tempdir.TemporaryDirectory() as td:
            # Add some spaces to names and directories
            file_name = 'space name ' + os.path.basename(self._get_notebook())
            file_basename = os.path.splitext(file_name)[0]
            file_dir = os.path.join(td, 'space dir')
            os.mkdir(file_dir)
            newpath = os.path.join(file_dir, file_name)
            shutil.copy(self._get_notebook(), newpath)
            exporter = self.exporter_class(latex_count=1)
            # Emulate nbconvertapp resource assignments
            resources = {
                'unique_key': file_basename,
                'output_files_dir': os.path.join(
                    file_dir,
                    sensitive_filename_cleanup(file_basename)
                )
            }
            (output, resources) = exporter.from_filename(newpath, resources)
            self.assertIsInstance(output, bytes)
            assert len(output) > 0
            # all temporary file should be cleaned up
            assert {file_name} == set(os.listdir(file_dir))

    @onlyif_cmds_exist('xelatex', 'pandoc')
    def test_bad_export(self):
        with tempdir.TemporaryDirectory() as td:
            # Add some spaces to names and directories
            file_name = os.path.basename(self._get_notebook('bad_latex.ipynb'))
            file_basename = os.path.splitext(file_name)[0]
            newpath = os.path.join(td, file_name)
            shutil.copy(self._get_notebook('bad_latex.ipynb'), newpath)
            exporter = self.exporter_class(latex_count=1)
            with self.assertRaises(LatexFailed):
                exporter.from_filename(newpath)
            # no temporary files should be left over
            assert {file_name} == set(os.listdir(td))
