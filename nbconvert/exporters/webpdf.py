"""Export to PDF via a headless browser"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import tempfile

from traitlets import Bool, default

from .html import HTMLExporter


class WebPDFExporter(HTMLExporter):
    """Writer designed to write to PDF files.

    This inherits from :class:`HTMLExporter`. It creates the HTML using the
    template machinery, and then run playwright to create a pdf.
    """

    export_from_notebook = "PDF via HTML"

    paginate = Bool(
        True,
        help="""
        Split generated notebook into multiple pages.

        If False, a PDF with one long page will be generated.

        Set to True to match behavior of LaTeX based PDF generator
        """,
    ).tag(config=True)

    @default("file_extension")
    def _file_extension_default(self):
        return ".html"

    @default("template_name")
    def _template_name_default(self):
        return "webpdf"

    disable_sandbox = Bool(
        False,
        help="""
        Disable chromium security sandbox when converting to PDF.

        WARNING: This could cause arbitrary code execution in specific circumstances,
        where JS in your notebook can execute serverside code! Please use with
        caution.

        ``https://github.com/puppeteer/puppeteer/blob/main@%7B2020-12-14T17:22:24Z%7D/docs/troubleshooting.md#setting-up-chrome-linux-sandbox``
        has more information.

        This is required for webpdf to work inside most container environments.
        """,
    ).tag(config=True)

    def _check_launch_reqs(self):
        try:
            from playwright.sync_api import sync_playwright
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "playwright is not installed to support Web PDF conversion. "
                "Please install `nbconvert[webpdf]` to enable."
            ) from e

        return sync_playwright

    def run_browser(self, html):
        """Run headless browser."""
        with self._check_launch_reqs()() as p:
            args = ["--no-sandbox"] if self.disable_sandbox else []
            browser = p.chromium.launch(args=args)
            page = browser.new_page()
            page.emulate_media(media='print')
            page.wait_for_timeout(100)

            # Create a temporary file to pass the HTML code to Chromium:
            # Unfortunately, tempfile on Windows does not allow for an already open
            # file to be opened by a separate process. So we must close it first
            # before calling Chromium. We also specify delete=False to ensure the
            # file is not deleted after closing (the default behavior).
            temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            with temp_file:
                temp_file.write(html.encode("utf-8"))

            page.goto(f"file://{temp_file.name}", wait_until="networkidle")
            page.wait_for_timeout(100)

            pdf_params = {"print_background": True}
            if not self.paginate:
                # Floating point precision errors cause the printed
                # PDF from spilling over a new page by a pixel fraction.
                dimensions = page.evaluate(
                    """() => {
                    const rect = document.body.getBoundingClientRect();
                    return {
                    width: Math.ceil(rect.width) + 1,
                    height: Math.ceil(rect.height) + 1,
                    }
                }"""
                )
                width = dimensions["width"]
                height = dimensions["height"]
                # 200 inches is the maximum size for Adobe Acrobat Reader.
                pdf_params.update(
                    {
                        "width": min(width, 200 * 72),
                        "height": min(height, 200 * 72),
                    }
                )
            pdf_data = page.pdf(**pdf_params)

            browser.close()
            return pdf_data

    def from_notebook_node(self, nb, resources=None, **kw):
        html, resources = super().from_notebook_node(nb, resources=resources, **kw)

        self.log.info("Building PDF")
        pdf_data = self.run_browser(html)
        self.log.info("PDF successfully created")

        # convert output extension to pdf
        # the writer above required it to be html
        resources["output_extension"] = ".pdf"

        return pdf_data, resources
