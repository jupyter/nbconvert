
def deprecation_warn(old_name, new_name):
    from warnings import warn
    warn(f"This class/method call '{old_name}' is deprecated since version 6.0.0 and has been replaced by '{new_name}'",
        DeprecationWarning)

def deprecated_caller(old_name, new_name, new_target, *args, **kwargs):
    def wrapped(*args, **kwargs):
        deprecation_warn(old_name, new_name)
        return new_target(*args, **kwargs)
    return wrapped


class DeprecationHelper(object):
    def __init__(self, old_name, new_name, new_target):
        self.old_name = old_name
        self.new_name = new_name
        self.new_target = new_target

    def __call__(self, *args, **kwargs):
        deprecation_warn(self.old_name, self.new_name)
        return self.new_target(*args, **kwargs)


# Class base Preprocessors
from ..processors.base import Processor
processor = DeprecationHelper(
    'preprocessors.base.processor',
    'processors.base.Processor',
    Processor
)
from ..processors.convertfigures import ConvertFiguresProcessor
ConvertFiguresPreprocessor = DeprecationHelper(
    'preprocessors.convertfigures.ConvertFiguresPreprocessor',
    'processors.convertfigures.ConvertFiguresProcessor',
    ConvertFiguresProcessor)
from ..processors.svg2pdf import SVG2PDFProcessor
SVG2PDFPreprocessor = DeprecationHelper(
    'preprocessors.svg2pdf.SVG2PDFPreprocessor',
    'processors.svg2pdf.SVG2PDFProcessor',
    SVG2PDFProcessor)
from ..processors.extractoutput import ExtractOutputProcessor
ExtractOutputPreprocessor = DeprecationHelper(
    'preprocessors.extractoutput.ExtractOutputPreprocessor',
    'processors.extractoutput.ExtractOutputProcessor',
    ExtractOutputProcessor)
from ..processors.latex import LatexProcessor
LatexPreprocessor = DeprecationHelper(
    'preprocessors.latex.LatexPreprocessor',
    'processors.latex.LatexProcessor',
    LatexProcessor)
from ..processors.csshtmlheader import CSSHTMLHeaderProcessor
CSSHTMLHeaderPreprocessor = DeprecationHelper(
    'preprocessors.csshtmlheader.CSSHTMLHeaderPreprocessor',
    'processors.csshtmlheader.CSSHTMLHeaderProcessor',
    CSSHTMLHeaderProcessor)
from ..processors.highlightmagics import HighlightMagicsProcessor
HighlightMagicsPreprocessor = DeprecationHelper(
    'preprocessors.highlightmagics.HighlightMagicsPreprocessor',
    'processors.highlightmagics.HighlightMagicsProcessor',
    HighlightMagicsProcessor)
from ..processors.clearoutput import ClearOutputProcessor
ClearOutputPreprocessor = DeprecationHelper(
    'preprocessors.clearoutput.ClearOutputPreprocessor',
    'processors.clearoutput.ClearOutputProcessor',
    ClearOutputProcessor)
from ..processors.execute import ExecuteProcessor
ExecutePreprocessor = DeprecationHelper(
    'preprocessors.execute.ExecutePreprocessor',
    'processors.execute.ExecuteProcessor',
    ExecuteProcessor)
from ..processors.regexremove import RegexRemoveProcessor
RegexRemovePreprocessor = DeprecationHelper(
    'preprocessors.regexremove.RegexRemovePreprocessor',
    'processors.regexremove.RegexRemoveProcessor',
    RegexRemoveProcessor)
from ..processors.tagremove import TagRemoveProcessor
TagRemovePreprocessor = DeprecationHelper(
    'preprocessors.tagremove.TagRemovePreprocessor',
    'processors.tagremove.TagRemoveProcessor',
    TagRemoveProcessor)
from ..processors.clearmetadata import ClearMetadataProcessor
ClearMetadataPreprocessor = DeprecationHelper(
    'preprocessors.clearmetadata.ClearMetadataPreprocessor',
    'processors.clearmetadata.ClearMetadataProcessor',
    ClearMetadataProcessor)

# decorated function Preprocessors
from ..processors.coalescestreams import coalesce_streams as coalesce_streams_new
coalesce_streams = deprecated_caller(
    'preprocessors.coalescestreams.coalesce_streams',
    'processors.coalescestreams.coalesce_streams',
    coalesce_streams_new
)

# Backwards compatability for imported name
from nbclient.exceptions import CellExecutionError
ClearMetadataPreprocessor = DeprecationHelper(
    'preprocessors.CellExecutionError',
    'nbclient.exceptions.CellExecutionError',
    CellExecutionError)
