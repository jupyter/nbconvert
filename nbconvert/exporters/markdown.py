"""Markdown Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import Bool, default
from traitlets.config import Config

from .templateexporter import TemplateExporter


class MarkdownExporter(TemplateExporter):
    """
    Exports to a markdown document (.md)
    """

    export_from_notebook = "Markdown"

    @default("file_extension")
    def _file_extension_default(self):
        return ".md"

    @default("template_name")
    def _template_name_default(self):
        return "markdown"

    output_mimetype = "text/markdown"

    embed_images = Bool(
        False, help="Whether or not to embed images as base64 in Markdown output."
    ).tag(config=True)

    @default("raw_mimetypes")
    def _raw_mimetypes_default(self):
        return ["text/markdown", "text/html", ""]

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert a notebook, optionally embedding extracted images."""
        if resources is None:
            resources = {}
        resources["embed_images"] = self.embed_images
        return super().from_notebook_node(nb, resources, **kw)

    @property
    def default_config(self):
        c = Config(
            {
                "ExtractAttachmentsPreprocessor": {"enabled": True},
                "ExtractOutputPreprocessor": {"enabled": True},
                "NbConvertBase": {
                    "display_data_priority": [
                        "text/html",
                        "text/markdown",
                        "image/svg+xml",
                        "text/latex",
                        "image/png",
                        "image/jpeg",
                        "text/plain",
                    ]
                },
                "HighlightMagicsPreprocessor": {"enabled": True},
            }
        )
        if super().default_config:
            c2 = super().default_config.copy()
            c2.merge(c)
            c = c2
        return c
