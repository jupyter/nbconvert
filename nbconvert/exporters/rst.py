"""reStructuredText Exporter class"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import default
from traitlets.config import Config

from ..filters import DataTypeFilter
from .templateexporter import TemplateExporter


class RSTExporter(TemplateExporter):
    """
    Exports reStructuredText documents.
    """

    @default("file_extension")
    def _file_extension_default(self):
        return ".rst"

    @default("template_name")
    def _template_name_default(self):
        return "rst"

    output_mimetype = "text/restructuredtext"
    export_from_notebook = "reST"

    def default_filters(self):
        """Override filter_data_type to use native rst outputs"""
        dtf = DataTypeFilter()
        dtf.display_data_priority = [self.output_mimetype, *dtf.display_data_priority]
        filters = dict(super().default_filters())
        filters["filter_data_type"] = dtf
        return filters.items()

    @property
    def default_config(self):
        c = Config(
            {
                "CoalesceStreamsPreprocessor": {"enabled": True},
                "ExtractOutputPreprocessor": {"enabled": True},
                "HighlightMagicsPreprocessor": {"enabled": True},
            }
        )
        if super().default_config:
            c2 = super().default_config.copy()
            c2.merge(c)
            c = c2
        return c
