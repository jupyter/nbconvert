"""
Preprocessor that transforms markdown cells: Insert numbering in from of heading
"""

from nbconvert.preprocessors.base import Preprocessor

try:  # for Mistune >= 3.0
    import mistune
    from mistune.core import BlockState
    from mistune.renderers.markdown import MarkdownRenderer

    MISTUNE_V3 = True
except ImportError:  # for Mistune >= 2.0
    MISTUNE_V3 = False

WRONG_MISTUNE_VERSION_ERROR = "Error: NumberedHeadingsPreprocessor requires mistune >= 3"


class NumberedHeadingsPreprocessor(Preprocessor):
    """Pre-processor that will rewrite markdown headings to include numberings."""

    def __init__(self, *args, **kwargs):
        """Init"""
        super().__init__(*args, **kwargs)
        if not MISTUNE_V3:
            raise Exception(WRONG_MISTUNE_VERSION_ERROR)
        self.md_parser = mistune.create_markdown(renderer=None)
        self.md_renderer = MarkdownRenderer()
        self.current_numbering = [0]

    def format_numbering(self):
        """Return a string representation of the current numbering"""
        return ".".join(str(n) for n in self.current_numbering)

    def _inc_current_numbering(self, level):
        """Increase internal counter keeping track of numberings"""
        if level > len(self.current_numbering):
            self.current_numbering = self.current_numbering + [0] * (
                level - len(self.current_numbering)
            )
        elif level < len(self.current_numbering):
            self.current_numbering = self.current_numbering[:level]
        self.current_numbering[level - 1] += 1

    def preprocess_cell(self, cell, resources, index):
        """Rewrites all the headings in the cell if it is markdown"""
        if cell["cell_type"] != "markdown":
            return cell, resources
        try:
            md_ast = self.md_parser(cell["source"])
            assert not isinstance(md_ast, str)  # type guard ; str is not returned by ast parser
            for element in md_ast:
                if element["type"] == "heading":
                    level = element["attrs"]["level"]
                    self._inc_current_numbering(level)
                    if len(element["children"]) > 0:
                        child = element["children"][0]
                        if child["type"] == "text":
                            child["raw"] = self.format_numbering() + " " + child["raw"]
            new_source = self.md_renderer(md_ast, BlockState())
            cell["source"] = new_source
            return cell, resources
        except Exception:
            self.log.warning("Failed processing cell headings", exc_info=True)
            return cell, resources
