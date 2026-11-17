"""Tests for the webpdf exporter"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import builtins
from unittest.mock import patch

import pytest

from nbconvert.exporters.exporter import Exporter
from nbconvert.exporters.webpdf import PLAYWRIGHT_INSTALLED, WebPDFExporter

from .base import ExportersTestsBase

real_import = builtins.__import__


class FakeBrowser:
    executable_path: str = ""


def monkey_import_notfound(name, globals_ctx=None, locals_ctx=None, fromlist=(), level=0):
    if name == "playwright.async_api":
        msg = "Fake missing"
        raise ModuleNotFoundError(msg)
    return real_import(name, globals=globals_ctx, locals=locals_ctx, fromlist=fromlist, level=level)


class TestWebPDFExporter(ExportersTestsBase):
    """Contains test functions for webpdf.py"""

    exporter_class = WebPDFExporter  # type:ignore

    def test_output_extension_and_single_browser_render(self):
        exporter = WebPDFExporter()
        with patch.object(exporter, "run_playwright", return_value=b"%PDF") as run_playwright:
            output, resources = exporter.from_filename(self._get_notebook())

        assert output == b"%PDF"
        assert resources["output_extension"] == ".pdf"
        run_playwright.assert_called_once()

    @pytest.mark.skipif(not PLAYWRIGHT_INSTALLED, reason="Playwright not installed")
    @pytest.mark.network
    def test_export(self):
        """
        Can a TemplateExporter export something?
        """
        output, _resources = WebPDFExporter(allow_chromium_download=True).from_filename(
            self._get_notebook()
        )
        assert output.startswith(b"%PDF")

    @pytest.mark.skipif(not PLAYWRIGHT_INSTALLED, reason="Playwright not installed")
    def test_webpdf_without_chromium(self):
        """
        Generate PDFs if chromium not present?
        """
        with (
            patch(
                "playwright.async_api._generated.Playwright.chromium", return_value=FakeBrowser()
            ),
            pytest.raises(RuntimeError, match="No suitable chromium executable"),
        ):
            WebPDFExporter(allow_chromium_download=False).from_filename(self._get_notebook())

    def test_webpdf_without_playwright(self):
        """
        Generate PDFs if playwright not installed?
        """
        base_exporter = Exporter()
        exporter = WebPDFExporter()
        with open(self._get_notebook(), encoding="utf-8") as f:
            nb = base_exporter.from_file(f, resources={})[0]
        with (
            patch("builtins.__import__", monkey_import_notfound),
            pytest.raises(RuntimeError, match="Playwright is not installed"),
        ):
            exporter.from_notebook_node(nb)
