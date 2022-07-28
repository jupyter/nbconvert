"""Tests for the qtpng preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os

import pytest

from ..qtpng import QtPNGExporter
from .base import ExportersTestsBase


class TestQtPNGExporter(ExportersTestsBase):
    """Contains test functions for qtpng.py"""

    exporter_class = QtPNGExporter

    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        if os.name == "nt":
            # currently not supported
            with pytest.raises(RuntimeError) as exc_info:
                (output, resources) = QtPNGExporter().from_filename(self._get_notebook())
        else:
            (output, resources) = QtPNGExporter().from_filename(self._get_notebook())
            assert len(output) > 0
