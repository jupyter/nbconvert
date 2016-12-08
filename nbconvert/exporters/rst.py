"""reStructuredText Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import default
from traitlets.config import Config

from .templateexporter import TemplateExporter


class RSTExporter(TemplateExporter):
    """
    Exports reStructuredText documents.
    """
    
    @default('file_extension')
    def _file_extension_default(self):
        return '.rst'

    @default('template_file')
    def _template_file_default(self):
        return 'rst'

    output_mimetype = 'text/restructuredtext'

    @property
    def default_config(self):
        c = Config({'ExtractOutputPreprocessor':{'enabled':True},
                    'NbConvertBase':{
                        'display_data_priority' : ['application/vnd.jupyter.widget-state+json',
                                                   'application/vnd.jupyter.widget-view+json',
                                                   'application/javascript',
                                                   'text/html',
                                                   'text/markdown',
                                                   'image/svg+xml',
                                                   'text/latex',
                                                   'image/png',
                                                   'image/jpeg',
                                                   'text/plain'
                                                  ]
                        }
                    })
        c.merge(super(RSTExporter,self).default_config)
        return c
