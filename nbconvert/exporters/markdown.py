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
                "Base64ImageExtractor": {
                    "enabled": True,
                    "use_separate_dir": False
                },
                "ExtractOutputPreprocessor": {
                    "enabled": True,
                    "output_filename_template": "{unique_key}_{cell_index}_{index}_{timestamp}{extension}"
                },
                "ExtractAttachmentsPreprocessor": {
                    "enabled": True,
                    "use_separate_dir": False
                },
                "FilesWriter": {
                    "build_directory": "",
                    "files_dir_template": "{unique_key}_files"
                },
                "Exporter": {
                    "preprocessors": [
                        "nbconvert.preprocessors.Base64ImageExtractor",
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