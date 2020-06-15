# Class base Processor
from .base import Processor
from .convertfigures import ConvertFiguresProcessor
from .svg2pdf import SVG2PDFProcessor
from .extractoutput import ExtractOutputProcessor
from .latex import LatexProcessor
from .csshtmlheader import CSSHTMLHeaderProcessor
from .highlightmagics import HighlightMagicsProcessor
from .clearoutput import ClearOutputProcessor
from .execute import ExecuteProcessor
from .regexremove import RegexRemoveProcessor
from .tagremove import TagRemoveProcessor
from .clearmetadata import ClearMetadataProcessor

# decorated function Processor
from .coalescestreams import coalesce_streams

# Backwards compatability for imported name
from nbclient.exceptions import CellExecutionError
