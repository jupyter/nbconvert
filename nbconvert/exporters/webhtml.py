"""Export to HTML after loading in a headless browser"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import asyncio
import concurrent.futures
import os
import subprocess
import sys
import tempfile
from importlib import util as importlib_util

from traitlets import Bool, Int, List, Unicode, default

from .html import HTMLExporter

PLAYWRIGHT_INSTALLED = importlib_util.find_spec("playwright") is not None

__all__ = ("WebHTMLExporter",)


class WebHTMLExporter(HTMLExporter):
    """Writer designed to write to HTML files after rendering in a browser.

    This inherits from :class:`HTMLExporter`. It creates the HTML using the
    template machinery, and then run playwright to load in a browser, saving
    the resulting page.
    """

    export_from_notebook = "HTML via Browser"
    _media_type = "screen"
    _output_format = "HTML"

    allow_chromium_download = Bool(
        False,
        help="Whether to allow downloading Chromium if no suitable version is found on the system.",
    ).tag(config=True)

    @default("file_extension")
    def _file_extension_default(self):
        return ".html"

    @default("template_name")
    def _template_name_default(self):
        return "webhtml"

    page_render_timeout = Int(
        100,
        help="""
        Time to wait for the page to render before serializing the output, in milliseconds.
        Increase this value if your notebook has complex JavaScript output that needs
        more time to load.
        """,
    ).tag(config=True)

    disable_sandbox = Bool(
        False,
        help="""
        Disable chromium security sandbox during browser-based conversion.

        WARNING: This could cause arbitrary code execution in specific circumstances,
        where JS in your notebook can execute serverside code! Please use with
        caution.

        ``https://github.com/puppeteer/puppeteer/blob/main@%7B2020-12-14T17:22:24Z%7D/docs/troubleshooting.md#setting-up-chrome-linux-sandbox``
        has more information.

        This is required for webhtml to work inside most container environments.
        """,
    ).tag(config=True)

    browser_args = List(
        Unicode(),
        help="""
        Additional arguments to pass to the browser.

        These arguments will be passed directly to the browser launch method
        and can be used to customize browser behavior beyond the default settings.
        """,
    ).tag(config=True)

    def run_playwright(self, html, _postprocess=None):
        """Run playwright."""

        async def main(temp_file):
            """Run main playwright script."""

            try:
                from playwright.async_api import (  # type: ignore[import-not-found] # noqa: PLC0415,
                    async_playwright,
                )
            except ModuleNotFoundError as e:
                msg = (
                    "Playwright is not installed to support browser-based conversion. "
                    "Please install `nbconvert[webhtml]` or `nbconvert[webpdf]` to enable it."
                )
                raise RuntimeError(msg) from e

            playwright = await async_playwright().start()
            chromium = playwright.chromium

            args = list(self.browser_args)
            if self.disable_sandbox:
                args.append("--no-sandbox")

            try:
                browser = await chromium.launch(
                    handle_sigint=False, handle_sigterm=False, handle_sighup=False, args=args
                )
            except Exception as e:
                msg = (
                    "No suitable chromium executable found on the system. "
                    "Please use '--allow-chromium-download' to allow downloading one,"
                    "or install it using `playwright install chromium`."
                )
                await playwright.stop()
                raise RuntimeError(msg) from e

            try:
                page = await browser.new_page()
                await page.emulate_media(media=self._media_type)
                await page.wait_for_timeout(100)
                await page.goto(f"file://{temp_file.name}", wait_until="networkidle")
                await page.wait_for_timeout(self.page_render_timeout)

                if _postprocess:
                    return await _postprocess(page)
                return await page.content()
            finally:
                try:
                    await browser.close()
                finally:
                    await playwright.stop()

        if self.allow_chromium_download:
            cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
            subprocess.check_call(cmd)  # noqa: S603

        # Create a temporary file to pass the HTML code to Chromium:
        # Unfortunately, tempfile on Windows does not allow for an already open
        # file to be opened by a separate process. So we must close it first
        # before calling Chromium. We also specify delete=False to ensure the
        # file is not deleted after closing (the default behavior).
        temp_file = tempfile.NamedTemporaryFile(  # noqa: SIM115
            suffix=".html", delete=False
        )
        with temp_file:
            if isinstance(html, str):
                temp_file.write(html.encode("utf-8"))
            else:
                temp_file.write(html)
        try:
            with concurrent.futures.ThreadPoolExecutor() as pool:
                html_data = pool.submit(asyncio.run, main(temp_file)).result()
        finally:
            # Ensure the file is deleted even if playwright raises an exception
            os.unlink(temp_file.name)
        return html_data

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert from a notebook node."""
        html, resources = super().from_notebook_node(nb, resources=resources, **kw)

        self.log.info("Building %s", self._output_format)
        html_data = self.run_playwright(html)
        self.log.info("%s successfully created", self._output_format)

        return html_data, resources
