"""
Module with tests for templateexporter.py
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os

from traitlets.config import Config
from jinja2 import DictLoader, TemplateNotFound
from nbformat import v4

from .base import ExportersTestsBase
from .cheese import CheesePreprocessor
from ..templateexporter import TemplateExporter
from testpath import tempdir

import pytest

class TestExporter(ExportersTestsBase):
    """Contains test functions for exporter.py"""


    def test_constructor(self):
        """
        Can a TemplateExporter be constructed?
        """
        TemplateExporter()


    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        exporter = self._make_exporter()
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert len(output) > 0


    def test_extract_outputs(self):
        """
        If the ExtractOutputPreprocessor is enabled, are outputs extracted?
        """
        config = Config({'ExtractOutputPreprocessor': {'enabled': True}})
        exporter = self._make_exporter(config=config)
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert resources is not None
        assert isinstance(resources['outputs'], dict)
        assert len(resources['outputs']) > 0


    def test_preprocessor_class(self):
        """
        Can a preprocessor be added to the preprocessors list by class type?
        """
        config = Config({'Exporter': {'preprocessors': [CheesePreprocessor]}})
        exporter = self._make_exporter(config=config)
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert resources is not None
        assert resources['cheese'] == 'real'


    def test_preprocessor_instance(self):
        """
        Can a preprocessor be added to the preprocessors list by instance?
        """
        config = Config({'Exporter': {'preprocessors': [CheesePreprocessor()]}})
        exporter = self._make_exporter(config=config)
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert resources is not None
        assert resources['cheese'] == 'real'


    def test_preprocessor_dottedobjectname(self):
        """
        Can a preprocessor be added to the preprocessors list by dotted object name?
        """
        config = Config({'Exporter': {'preprocessors': ['nbconvert.exporters.tests.cheese.CheesePreprocessor']}})
        exporter = self._make_exporter(config=config)
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert resources is not None
        assert resources['cheese'] == 'real'


    def test_preprocessor_via_method(self):
        """
        Can a preprocessor be added via the Exporter convenience method?
        """
        exporter = self._make_exporter()
        exporter.register_preprocessor(CheesePreprocessor, enabled=True)
        (output, resources) = exporter.from_filename(self._get_notebook())
        assert resources is not None
        assert resources['cheese'] == 'real'

    def test_absolute_template_file(self):
        with tempdir.TemporaryDirectory() as td:
            template = os.path.join(td, 'abstemplate.tpl')
            test_output = 'absolute!'
            with open(template, 'w') as f:
                f.write(test_output)
            config = Config()
            config.TemplateExporter.template_file = template
            exporter = self._make_exporter(config=config)
            assert exporter.template.filename == template
            assert os.path.dirname(template) in exporter.template_path

    def test_relative_template_file(self):
        with tempdir.TemporaryWorkingDirectory() as td:
            os.mkdir('relative')
            template = os.path.abspath(os.path.join(td, 'relative', 'relative_template.tpl'))
            test_output = 'relative!'
            with open(template, 'w') as f:
                f.write(test_output)
            config = Config()
            config.TemplateExporter.template_file = template
            exporter = self._make_exporter(config=config)
            assert os.path.abspath(exporter.template.filename) == template
            assert os.path.dirname(template) in [ os.path.abspath(d) for d in exporter.template_path ]
    
    def test_in_memory_template(self):
        # Loads in an in memory template using jinja2.DictLoader
        # creates a class that uses this template with the template_file argument
        # converts an empty notebook using this mechanism
        my_loader = DictLoader({'my_template': "{%- extends 'rst.tpl' -%}"})
        
        class MyExporter(TemplateExporter):
            template_file = 'my_template'
        
        exporter = MyExporter(extra_loaders=[my_loader])
        nb = v4.new_notebook()
        out, resources = exporter.from_notebook_node(nb)


    def test_fail_to_find_template_file(self):
        # Create exporter with invalid template file, check that it doesn't
        # exist in the environment, try to convert empty notebook. Failure is
        # expected due to nonexistant template file.
        
        template = 'does_not_exist.tpl'
        exporter = TemplateExporter(template_file=template)
        assert template not in exporter.environment.list_templates(extensions=['tpl'])
        nb = v4.new_notebook()
        with pytest.raises(TemplateNotFound):
            out, resources = exporter.from_notebook_node(nb)
        
        
        

    def _make_exporter(self, config=None):
        # Create the exporter instance, make sure to set a template name since
        # the base TemplateExporter doesn't have a template associated with it.
        exporter = TemplateExporter(config=config)
        if not exporter.template_file:
            # give it a default if not specified
            exporter.template_file = 'python'
        return exporter
