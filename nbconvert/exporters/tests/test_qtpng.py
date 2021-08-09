"""Tests for the qtpng preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import ExportersTestsBase
from ..qtpng import QtPNGExporter

class TestQtPNGExporter(ExportersTestsBase):
    """Contains test functions for qtpng.py"""

    exporter_class = QtPNGExporter

    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        (output, resources) = QtPNGExporter().from_filename(self._get_notebook())
        assert len(output) > 0
