"""Generic script exporter class for any kernel language"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from .templateexporter import TemplateExporter

from traitlets import Dict, default
from .base import get_exporter, ExporterNotFound

class ScriptExporter(TemplateExporter):
    
    _exporters = Dict()
    
    @default('template_file')
    def _template_file_default(self):
        return 'script'

    def from_notebook_node(self, nb, resources=None, **kw):
        langinfo = nb.metadata.get('language_info', {})
        
        # delegate to custom exporter, if specified
        exporter_name = langinfo.get('nbconvert_exporter')

        if (not exporter_name) or exporter_name == 'script':
            return self._plain_export(nb, resources, langinfo, **kw)


        self.log.debug("Loading script exporter: %s", exporter_name)
        if exporter_name not in self._exporters:
            try:
                Exporter = get_exporter(exporter_name)
                self._exporters[exporter_name] = Exporter(parent=self)
            except ExporterNotFound:
                warn = self.log.warn
                warn("Exporter '%s' not available,"
                     "falling back to plain script export" % exporter_name)
                exporter_dist = langinfo.get('nbconvert_exporter_dist', None)
                if exporter_dist:
                    warn("The notebook's metadata suggests installing the "
                         "'%s' package to provide this exporter" % exporter_dist)
                return self._plain_export(nb, resources, langinfo, **kw)

        exporter = self._exporters[exporter_name]
        return exporter.from_notebook_node(nb, resources, **kw)

    def _plain_export(self, nb, resources, langinfo, **kw):
        self.file_extension = langinfo.get('file_extension', '.txt')
        self.output_mimetype = langinfo.get('mimetype', 'text/plain')
        return super(ScriptExporter, self).from_notebook_node(nb, resources, **kw)
