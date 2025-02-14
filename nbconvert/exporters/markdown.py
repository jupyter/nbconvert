"""Markdown Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import default
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

    @default("raw_mimetypes")
    def _raw_mimetypes_default(self):
        return ["text/markdown", "text/html", ""]

    @property
    def default_config(self):
        c = Config(
            {
                "ExtractAttachmentsPreprocessor": {"enabled": True},
                "ExtractOutputPreprocessor": {
                    "enabled": True,
                    "extract_output_prefix": "{unique_key}_output_"
                },
                "Base64ImageExtractor": {"enabled": True},
                "Exporter": {
                    "preprocessors": [
                        "nbconvert.preprocessors.Base64ImageExtractor",
                        "nbconvert.preprocessors.TagRemovePreprocessor",
                        "nbconvert.preprocessors.RegexRemovePreprocessor",
                        "nbconvert.preprocessors.ExtractAttachmentsPreprocessor",
                        "nbconvert.preprocessors.ExtractOutputPreprocessor",
                    ]
                },
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
