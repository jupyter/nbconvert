"""
Module that define a custom exporter just to test the ability to invoke
nbconvert with full qualified name
"""

from traitlets import default

from nbconvert.exporters.html import HTMLExporter
from nbconvert.exporters.notebook import NotebookExporter


class MyExporter(HTMLExporter):
    """
    My custom exporter
    """

    @default("file_extension")
    def _file_extension_default(self):
        """
        The new file extension is `.test_ext`
        """
        return ".test_ext"

    @default("template_extension")
    def _template_extension_default(self):
        return ".html.j2"


class MyNotebookExporter(NotebookExporter):
    """A notebook exporter that marks output to verify exporter selection."""

    def from_notebook_node(self, nb, resources=None, **kw):
        nb.metadata["custom_exporter"] = True
        return super().from_notebook_node(nb, resources, **kw)
