"""Tests for Kernel-specific templates"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from testpath import modified_env

from .base import ExportersTestsBase
from ..markdown import MarkdownExporter


class TestKernelTemplates(ExportersTestsBase):
    """Tests for Kernel-specific templates"""

    exporter_class = MarkdownExporter
    should_include_raw = ['markdown', 'html']

    def setUp(self):
        super(TestKernelTemplates, self).setUp()
        self.env = modified_env({'JUPYTER_PATH': self._get_files_path()})

    def test_export(self):
        """Will the kernel-specific template be used?"""
        with self.env:
            output, resources = MarkdownExporter().from_filename(self._get_notebook('kernel_template.ipynb'))
        self.assertIn('Test md code: some *markdown*', output)
