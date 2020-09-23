"""Export to PDF via a headless browser"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import asyncio

from traitlets import Bool
import concurrent.futures

from .html import HTMLExporter


class WebPDFExporter(HTMLExporter):
    """Writer designed to write to PDF files.

    This inherits from :class:`HTMLExporter`. It creates the HTML using the
    template machinery, and then run pyppeteer to create a pdf.
    """
    export_from_notebook = "PDF via pyppeteer"

    allow_chromium_download = Bool(False,
        help='Whether to allow downloading Chromium if no suitable version is found on the system.'
    ).tag(config=True)

    def _check_launch_reqs(self):
        try:
            from pyppeteer import launch
            from pyppeteer.util import check_chromium
        except ModuleNotFoundError as e:
            raise RuntimeError("Pyppeteer is not installed to support Web PDF conversion. "
                               "Please install `nbconvert[webpdf]` to enable.") from e
        if not self.allow_chromium_download and not check_chromium():
            raise RuntimeError("No suitable chromium executable found on the system. "
                               "Please use '--allow-chromium-download' to allow downloading one.")
        return launch

    def run_pyppeteer(self, html):
        """Run pyppeteer."""

        async def main():
            browser = await self._check_launch_reqs()(
                handleSIGINT=False,
                handleSIGTERM=False,
                handleSIGHUP=False,
            )
            page = await browser.newPage()
            await page.waitFor(100)
            await page.goto('data:text/html,'+html, waitUntil='networkidle0')
            await page.waitFor(100)

            # Floating point precision errors cause the printed
            # PDF from spilling over a new page by a pixel fraction.
            dimensions = await page.evaluate(
              """() => {
                const rect = document.body.getBoundingClientRect();
                return {
                  width: Math.ceil(rect.width) + 1,
                  height: Math.ceil(rect.height) + 1,
                }
              }"""
            )
            width = dimensions['width']
            height = dimensions['height']
            # 200 inches is the maximum size for Adobe Acrobat Reader.
            pdf_data = await page.pdf(
              {
                'width': min(width, 200 * 72),
                'height': min(height, 200 * 72),
                'printBackground': True,
              }
            )
            await browser.close()
            return pdf_data

        pool = concurrent.futures.ThreadPoolExecutor()
        # TODO: when dropping Python 3.6, use
        # pdf_data = pool.submit(asyncio.run, main()).result()
        def run_coroutine(coro):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        pdf_data = pool.submit(run_coroutine, main()).result()
        return pdf_data

    def from_notebook_node(self, nb, resources=None, **kw):
        self._check_launch_reqs()
        html, resources = super().from_notebook_node(
            nb, resources=resources, **kw
        )

        self.log.info('Building PDF')
        pdf_data = self.run_pyppeteer(html)
        self.log.info('PDF successfully created')

        # convert output extension to pdf
        # the writer above required it to be html
        resources['output_extension'] = '.pdf'

        return pdf_data, resources
