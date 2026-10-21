"""Tests for PythonExporter"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from nbformat import v4

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

    def test_export_invalid_indentation(self):
        """A cell with inconsistent dedents does not stop the export"""
        nb = v4.new_notebook(
            cells=[
                v4.new_code_cell("for i in range(3):\n        print(i)\n    print(i)"),
                v4.new_code_cell("%time x = 1"),
            ]
        )
        (output, _resources) = self.exporter_class().from_notebook_node(nb)  # type:ignore
        self.assertIn("for i in range(3):\n        print(i)\n    print(i)", output)
        self.assertIn("get_ipython().run_line_magic('time', 'x = 1')", output)
