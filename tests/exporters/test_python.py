"""Tests for PythonExporter"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbconvert.exporters.python import PythonExporter

from .base import ExportersTestsBase


class TestPythonExporter(ExportersTestsBase):
    """Tests for PythonExporter"""

    exporter_class = PythonExporter  # type:ignore
    should_include_raw = ["python"]  # type:ignore

    def test_constructor(self):
        """Can a PythonExporter be constructed?"""
        self.exporter_class()  # type:ignore

    def test_export(self):
        """Can a PythonExporter export something?"""
        (output, _resources) = self.exporter_class().from_filename(  # type:ignore
            self._get_notebook()
        )
        self.assertIn("coding: utf-8", output)
        self.assertIn("#!/usr/bin/env python", output)
