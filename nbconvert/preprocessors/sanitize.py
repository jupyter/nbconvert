"""
NBConvert Preprocessor for sanitizing HTML rendering of notebooks.
"""

from collections.abc import Mapping
from html import escape
from html.parser import HTMLParser
from importlib import import_module
from typing import Any as TypingAny

from traitlets import Any, Bool, List, Set, Unicode

from .base import Preprocessor

nh3: TypingAny = None
try:  # pragma: no cover - the fallback is only possible in partial tooling environments
    nh3 = import_module("nh3")
except ModuleNotFoundError:
    pass

# Keep the public defaults compatible with Bleach while using nh3 for the
# actual sanitization.  nh3's defaults are intentionally broader than
# Bleach's, so relying on them would silently change the HTML allowlist.
ALLOWED_TAGS = {
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "strong",
    "ul",
}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "abbr": ["title"],
    "acronym": ["title"],
}
ALLOWED_STYLES = {
    "azimuth",
    "background-color",
    "border-bottom-color",
    "border-collapse",
    "border-color",
    "border-left-color",
    "border-right-color",
    "border-top-color",
    "clear",
    "color",
    "cursor",
    "direction",
    "display",
    "elevation",
    "float",
    "font",
    "font-family",
    "font-size",
    "font-style",
    "font-variant",
    "font-weight",
    "height",
    "letter-spacing",
    "line-height",
    "overflow",
    "pause",
    "pause-after",
    "pause-before",
    "pitch",
    "pitch-range",
    "richness",
    "speak",
    "speak-header",
    "speak-numeral",
    "speak-punctuation",
    "speech-rate",
    "stress",
    "text-align",
    "text-decoration",
    "text-indent",
    "vertical-align",
    "voice-family",
    "volume",
    "white-space",
    "width",
    "unicode-bidi",
}


__all__ = ["SanitizeHTML"]


class _TagEscaper(HTMLParser):
    """Escape disallowed tags so nh3 can reproduce Bleach's strip=False mode."""

    def __init__(self, allowed_tags):
        super().__init__(convert_charrefs=False)
        self.allowed_tags = {tag.lower() for tag in allowed_tags}
        self.parts = []

    def handle_starttag(self, tag, attrs):
        source = self.get_starttag_text() or f"<{tag}>"
        self.parts.append(source if tag.lower() in self.allowed_tags else escape(source))

    def handle_startendtag(self, tag, attrs):
        source = self.get_starttag_text() or f"<{tag} />"
        self.parts.append(source if tag.lower() in self.allowed_tags else escape(source))

    def handle_endtag(self, tag):
        source = f"</{tag}>"
        self.parts.append(source if tag.lower() in self.allowed_tags else escape(source))

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.parts.append(escape(f"<!{decl}>"))

    def unknown_decl(self, data):
        self.parts.append(escape(f"<![{data}]>"))

    def handle_pi(self, data):
        self.parts.append(escape(f"<?{data}>"))

    def result(self):
        return "".join(self.parts)


def _escape_disallowed_tags(html_str, tags):
    parser = _TagEscaper(tags)
    parser.feed(html_str)
    parser.close()
    return parser.result()


def _attribute_configuration(attributes):
    """Convert Bleach's flexible attribute config to nh3's callback API."""

    if callable(attributes):
        return None, lambda tag, attr, value: value if attributes(tag, attr, value) else None

    if isinstance(attributes, Mapping):
        normalized = {}
        for tag, allowed in attributes.items():
            if callable(allowed):
                # nh3 needs a candidate allowlist before it invokes the
                # callback.  Its default set covers the standard HTML attrs.
                normalized[tag] = set(ALLOWED_ATTRIBUTES.get(tag, ()))
            elif isinstance(allowed, str):
                normalized[tag] = {allowed}
            else:
                normalized[tag] = set(allowed or ())
    else:
        normalized = {"*": set(attributes or ())}

    def filter_mapping(tag, attr, value):
        if isinstance(attributes, Mapping):
            candidates = []
            if "*" in attributes:
                candidates.append(attributes["*"])
            if tag in attributes:
                candidates.append(attributes[tag])
            for allowed_value in candidates:
                if callable(allowed_value):
                    if allowed_value(tag, attr, value):
                        return value
                else:
                    allowed_attrs = (
                        {allowed_value} if isinstance(allowed_value, str) else allowed_value
                    )
                    if attr in (allowed_attrs or ()):
                        return value
            return None

        return value if attr in normalized["*"] else None

    return normalized, filter_mapping


def sanitize_html(html_str, *, tags, attributes, styles, strip, strip_comments):
    """Sanitize HTML with nh3 while retaining nbconvert's Bleach semantics."""
    if nh3 is None:
        msg = "nbconvert's HTML sanitizer requires the nh3 dependency"
        raise ImportError(msg)

    if not strip:
        html_str = _escape_disallowed_tags(html_str, tags)

    attribute_config, attribute_filter = _attribute_configuration(attributes)
    return nh3.clean(
        html_str,
        tags=set(tags),
        # Bleach strips unsafe tags but keeps their contents in both modes.
        clean_content_tags=set(),
        attributes=attribute_config,
        attribute_filter=attribute_filter,
        strip_comments=strip_comments,
        link_rel=None,
        filter_style_properties=set(styles),
    )


class SanitizeHTML(Preprocessor):
    """A preprocessor to sanitize html."""

    # Bleach config.
    attributes = Any(
        config=True,
        default_value=ALLOWED_ATTRIBUTES,
        help="Allowed HTML tag attributes",
    )
    tags = List(
        Unicode(),
        config=True,
        default_value=ALLOWED_TAGS,
        help="List of HTML tags to allow",
    )
    styles = List(
        Unicode(),
        config=True,
        default_value=ALLOWED_STYLES,
        help="Allowed CSS styles if <style> tag is allowed",
    )
    strip = Bool(
        config=True,
        default_value=False,
        help="If True, remove unsafe markup entirely instead of escaping",
    )
    strip_comments = Bool(
        config=True,
        default_value=True,
        help="If True, strip comments from escaped HTML",
    )

    # Display data config.
    safe_output_keys = Set(
        config=True,
        default_value={
            "metadata",  # Not a mimetype per-se, but expected and safe.
            "text/plain",
            "text/latex",
            "application/json",
            "image/png",
            "image/jpeg",
        },
        help="Cell output mimetypes to render without modification",
    )
    sanitized_output_types = Set(
        config=True,
        default_value={
            "text/html",
            "text/markdown",
        },
        help="Cell output types to display after sanitizing with nh3.",
    )

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Sanitize potentially-dangerous contents of the cell.

        Cell Types:
          raw:
            Sanitize literal HTML
          markdown:
            Sanitize literal HTML
          code:
            Sanitize outputs that could result in code execution
        """
        if cell.cell_type == "raw":
            # Sanitize all raw cells anyway.
            # Only ones with the text/html mimetype should be emitted
            # but erring on the side of safety maybe.
            cell.source = self.sanitize_html_tags(cell.source)
            return cell, resources
        if cell.cell_type == "markdown":
            cell.source = self.sanitize_html_tags(cell.source)
            return cell, resources
        if cell.cell_type == "code":
            cell.outputs = self.sanitize_code_outputs(cell.outputs)
            return cell, resources
        return None

    def sanitize_code_outputs(self, outputs):
        """
        Sanitize code cell outputs.

        Removes 'text/javascript' fields from display_data outputs, and
        runs `sanitize_html_tags` over 'text/html'.
        """
        for output in outputs:
            # These are always ascii, so nothing to escape.
            if output["output_type"] in ("stream", "error"):
                continue
            data = output.data
            to_remove = []
            for key in data:
                if key in self.safe_output_keys:
                    continue
                if key in self.sanitized_output_types:
                    self.log.info("Sanitizing %s", key)
                    data[key] = self.sanitize_html_tags(data[key])
                else:
                    # Mark key for removal. (Python doesn't allow deletion of
                    # keys from a dict during iteration)
                    to_remove.append(key)
            for key in to_remove:
                self.log.info("Removing %s", key)
                del data[key]
        return outputs

    def sanitize_html_tags(self, html_str):
        """
        Sanitize a string containing raw HTML tags.
        """
        return sanitize_html(
            html_str,
            tags=self.tags,
            attributes=self.attributes,
            styles=self.styles,
            strip=self.strip,
            strip_comments=self.strip_comments,
        )


def _get_default_css_sanitizer():
    return set(ALLOWED_STYLES)
