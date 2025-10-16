"""Tests for the qtpng preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os

import pytest

from nbconvert.exporters.qt_screenshot import QT_INSTALLED
from nbconvert.exporters.qtpng import QtPNGExporter

from .base import ExportersTestsBase


@pytest.mark.skipif(not QT_INSTALLED, reason="PyQtWebEngine not installed")
class TestQtPNGExporter(ExportersTestsBase):
    """Contains test functions for qtpng.py"""

    exporter_class = QtPNGExporter  # type:ignore

    @pytest.mark.flaky
    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        if os.name == "nt":
            # currently not supported
            with pytest.raises(RuntimeError):
                (output, _resources) = QtPNGExporter().from_filename(self._get_notebook())
        else:
            (output, _resources) = QtPNGExporter().from_filename(self._get_notebook())
            assert len(output) > 0
