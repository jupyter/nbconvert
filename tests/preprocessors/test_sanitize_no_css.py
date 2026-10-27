"""Tests for importing the HTML sanitizer when no CSS sanitizer is available."""

import subprocess
import sys
import textwrap

from .base import PreprocessorTestsBase

_CHECK = textwrap.dedent(
    """
    import sys
    import warnings

    # Hide both ways of obtaining a CSS allowlist from bleach: the bleach[css]
    # extra (bleach >=5) and the module level constant of bleach <5.
    sys.modules["bleach.css_sanitizer"] = None
    import bleach

    if hasattr(bleach, "ALLOWED_STYLES"):
        del bleach.ALLOWED_STYLES

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        import nbconvert.preprocessors.sanitize as sanitize

    assert sanitize.ALLOWED_STYLES == frozenset(), sanitize.ALLOWED_STYLES
    assert sanitize._USE_BLEACH_CSS_SANITIZER is False
    assert sanitize._USE_BLEACH_STYLES is False
    assert list(sanitize.SanitizeHTML().styles) == []
    assert any(issubclass(w.category, UserWarning) for w in caught)

    sanitize.SanitizeHTML().sanitize_html_tags("_A_ <script>tags</script>")
    print("ok")
    """
)


class TestSanitizerWithoutCss(PreprocessorTestsBase):
    """The sanitizer must stay importable when bleach has no CSS sanitization (#2209)."""

    def test_import_without_css_sanitizer(self):
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-c", _CHECK], capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)
