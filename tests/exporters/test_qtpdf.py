"""Tests for the qtpdf preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import sys

import pytest

from nbconvert.exporters.qt_screenshot import QT_INSTALLED
from nbconvert.exporters.qtpdf import QtPDFExporter

from .base import ExportersTestsBase


@pytest.mark.skipif(not QT_INSTALLED, reason="PyQtWebEngine not installed")
class TestQtPDFExporter(ExportersTestsBase):
    """Contains test functions for qtpdf.py"""

    exporter_class = QtPDFExporter  # type:ignore

    # https://github.com/jupyter/nbconvert/issues/2346
    # Drop this skip when the Qt PDF export works on Windows again.
    @pytest.mark.skipif(sys.platform == "win32", reason="Qt WebEngine hangs on Windows")
    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        (output, _resources) = QtPDFExporter().from_filename(self._get_notebook())
        assert len(output) > 0
