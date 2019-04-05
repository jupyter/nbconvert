# -*- coding: utf-8 -*-
"""HTML Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import copy
import os
import re

from traitlets import default, Unicode
from traitlets.config import Config

from nbconvert.filters.highlight import Highlight2HTML
from nbconvert.filters.markdown_mistune import IPythonRenderer, MarkdownWithMath

from .templateexporter import TemplateExporter


class HTMLExporter(TemplateExporter):
    """
    Exports a basic HTML document.  This exporter assists with the export of
    HTML.  Inherit from it if you are writing your own HTML template and need
    custom preprocessors/filters.  If you don't need custom preprocessors/
    filters, just change the 'template_file' config option.
    """

    anchor_link_text = Unicode(u'¶',
        help="The text used as the text for anchor links.").tag(config=True)

    @default('file_extension')
    def _file_extension_default(self):
        return '.html'

    @default('default_template_path')
    def _default_template_path_default(self):
        return os.path.join("..", "templates", "html")

    @default('template_file')
    def _template_file_default(self):
        return 'full.tpl'

    output_mimetype = 'text/html'

    @property
    def default_config(self):
        c = Config({
            'NbConvertBase': {
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
                },
            'CSSHTMLHeaderPreprocessor':{
                'enabled':True
                },
            'HighlightMagicsPreprocessor': {
                'enabled':True
                }
            })
        c.merge(super(HTMLExporter,self).default_config)
        return c

    def markdown2html(self, source):
        """Markdown to HTML filter respecting the anchor_link_text setting"""
        renderer = IPythonRenderer(escape=False,
                                   anchor_link_text=self.anchor_link_text)
        return MarkdownWithMath(renderer=renderer).render(source)

    def default_filters(self):
        for pair in super(HTMLExporter, self).default_filters():
            yield pair
        yield ('markdown2html', self.markdown2html)

    def process_attachments(self, nb, output):
        for cell in nb.cells:
            if 'attachments' in cell:
                for key, attachment in cell['attachments'].items():
                    for att_type, att in attachment.items():
                        output = output.replace(
                            'attachment:{}'.format(key),
                            'data:' + att_type + ';base64, ' + attachment[att_type])
        return output

    def _make_attachments_globally_unique(self, nb):
        nb = copy.deepcopy(nb)
        for cell_index, cell in enumerate(nb.cells):
            if 'attachments' in cell:
                # attachment with names being unique only within the cell not globally
                local_attachments = cell['attachments'].copy()
                # we will replace them with a globally unique name
                cell['attachments'] = {}
                for key, attachment in local_attachments.items():
                    unique_key = 'globally_unique_%i_%s' % (cell_index, key)
                    cell['attachments'][unique_key] = attachment
                    if 'source' in cell:
                        # the reference to the attachment should also be renamed
                        local_ref = r'](attachment:%s)' % key
                        global_ref = r'](attachment:%s)' % unique_key
                        cell['source'] = re.sub(local_ref, global_ref, cell['source'])
                        cell['source'] = cell['source'].replace(local_ref, global_ref)
        return nb



    def from_notebook_node(self, nb, resources=None, **kw):
        self.nb = nb = self._make_attachments_globally_unique(nb)
        langinfo = nb.metadata.get('language_info', {})
        lexer = langinfo.get('pygments_lexer', langinfo.get('name', None))
        highlight_code = self.filters.get('highlight_code', Highlight2HTML(pygments_lexer=lexer, parent=self))
        self.register_filter('highlight_code', highlight_code)
        
        output, resources = super(HTMLExporter, self).from_notebook_node(nb, resources, **kw)
        att_output = self.process_attachments(nb, output)
        return att_output, resources
