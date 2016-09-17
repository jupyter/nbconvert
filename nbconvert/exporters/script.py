"""Generic script exporter class for any kernel language"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from .templateexporter import TemplateExporter

from traitlets import Dict, default
from traitlets.utils.importstring import import_item
from .export import ExporterNameError

class ScriptExporter(TemplateExporter):
    
    _exporters = Dict()
    
    @default('template_file')
    def _template_file_default(self):
        return 'script'

    def from_notebook_node(self, nb, resources=None, **kw):
        langinfo = nb.metadata.get('language_info', {})
        print("I am here") 
        # delegate to custom exporter, if specified
        exporter_name = langinfo.get('nbconvert_exporter')
        if exporter_name and exporter_name != 'script':
            self.log.debug("Loading script exporter: %s", exporter_name)
            from .export import get_exporter
            if exporter_name not in self._exporters:
                try: 
                    Exporter = get_exporter(exporter_name)
                    print("i am here")
                    self._exporters[exporter_name] = Exporter(parent=self)
                except:
                    print("yes you found me")
                    if langinfo.get('nbconvert_exporter_package',""):
                        external_exporter_name = langinfo.get('nbconvert_exporter_package')
                        try: 
                            Exporter = get_exporter(external_exporter_name)
                            self._exporters[external_exporter_name] = Exporter(parent=self)
                        except:
                            raise ExporterNameError("The Exporter named {nbconvert_exporter_package} cannot be found, try pip install {nbconvert_exporter_package}.".format(nbconvert_exporter_package=external_exporter_name))
                    else:
                        raise ExporterNameError("The Exporter named {exporter_name} cannot be found.".format(exporter_name=exporter_name)) 

            exporter = self._exporters[exporter_name]
            return exporter.from_notebook_node(nb, resources, **kw)
        
        self.file_extension = langinfo.get('file_extension', '.txt')
        self.output_mimetype = langinfo.get('mimetype', 'text/plain')
        return super(ScriptExporter, self).from_notebook_node(nb, resources, **kw)
