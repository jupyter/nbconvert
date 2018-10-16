"""PreProcessor for rendering """

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
import copy
import tempfile
import webbrowser
import threading
import tornado.escape
import nbformat

from tornado import web, ioloop, httpserver, log
from tornado.httpclient import AsyncHTTPClient
from traitlets import Bool, Unicode, Int

from .base import Preprocessor
from ..exporters.html import HTMLExporter
from ..writers import FilesWriter


class ProxyHandler(web.RequestHandler):
    """handler the proxies requests from a local prefix to a CDN"""
    @web.asynchronous
    def get(self, prefix, url):
        """proxy a request to a CDN"""
        proxy_url = "/".join([self.settings['cdn'], url])
        client = self.settings['client']
        client.fetch(proxy_url, callback=self.finish_get)
    
    def finish_get(self, response):
        """finish the request"""
        # rethrow errors
        response.rethrow()
        
        for header in ["Content-Type", "Cache-Control", "Date", "Last-Modified", "Expires"]:
            if header in response.headers:
                self.set_header(header, response.headers[header])
        self.finish(response.body)


class SnapshotHandler(web.RequestHandler):
    def initialize(self, snapshot_dict, callback):
        self.snapshot_dict = snapshot_dict
        self.callback = callback

    # @web.asynchronous
    def post(self, view_id=None, image_data=None):
        #, view_id=None, image_data=None
        #view_id = self.get_parameter('view_id')
        data = tornado.escape.json_decode(self.request.body)
        print('hi', data['cell_index'], data['output_index'], data['image_data'])
        i, j = data['cell_index'], data['output_index']
        key = i, j
        # assert MIME_TYPE_PNG not in self.snapshot_dict[key]['data']
        image_data = data['image_data']
        header = 'data:image/png;base64,'
        assert image_data.startswith(header), 'not a png image?'
        self.snapshot_dict[key]['data'][MIME_TYPE_PNG] = image_data[len(header):]
        self.callback()
        # print(data)
        # print(view_id, image_data)
        # print(self.configuration)
        # f

MIME_TYPE_JUPYTER_WIDGET_VIEW = 'application/vnd.jupyter.widget-view+json'
MIME_TYPE_PNG = 'image/png'
MIME_TYPE_HTML = 'text/html'
DIRNAME_STATIC = os.path.join(os.path.dirname(__file__), '../../dist')

class SnapshotPreProcessor(Preprocessor):
    """Pre processor designed to serve files
    
    Proxies reveal.js requests to a CDN if no local reveal.js is present
    """

    open_in_browser = Bool(True,
        help="""Should the browser be opened automatically?"""
    ).tag(config=True)

    browser = Unicode(u'', 
                      help="""Specify what browser should be used to open slides. See
                      https://docs.python.org/3/library/webbrowser.html#webbrowser.register
                      to see how keys are mapped to browser executables. If 
                      not specified, the default browser will be determined 
                      by the `webbrowser` 
                      standard library module, which allows setting of the BROWSER 
                      environment variable to override it.
                      """).tag(config=True)

    reveal_cdn = Unicode("https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.5.0",
                         help="""URL for reveal.js CDN.""").tag(config=True)
    reveal_prefix = Unicode("reveal.js",
                            help="URL prefix for reveal.js").tag(config=True)
    ip = Unicode("127.0.0.1",
                 help="The IP address to listen on.").tag(config=True)
    port = Int(8000, help="port for the server to listen on.").tag(config=True)

    def callback(self):
        done = True
        for key, value in self.snapshot_dict.items():
            if value['data'][MIME_TYPE_PNG] is None:
                done = False
        if done:
            self.main_ioloop.stop()

    def preprocess(self, nb, resources):
        """Serve the build directory with a webserver."""
        self.snapshot_dict = {}
        # self.nb = nbformat.read(input.replace('.html', '.ipynb'), as_version=4)
        self.nb = nb
        for cell_index, cell in enumerate(self.nb.cells):
            if 'outputs' in cell:
                for output_index, output in enumerate(cell.outputs):
                    if 'data' in output:
                        if MIME_TYPE_JUPYTER_WIDGET_VIEW in output['data'] or MIME_TYPE_HTML in output['data']:
                            self.snapshot_dict[(cell_index, output_index)] = output
        if self.snapshot_dict.keys():
            with tempfile.TemporaryDirectory() as dirname:
                html_exporter = HTMLExporter(template_file='snapshot', default_preprocessors=[
                                      # 'nbconvert.preprocessors.TagRemovePreprocessor',
                                      # 'nbconvert.preprocessors.RegexRemovePreprocessor',
                                      # 'nbconvert.preprocessors.ClearOutputPreprocessor',
                                      # 'nbconvert.preprocessors.ExecutePreprocessor',
                                      'nbconvert.preprocessors.coalesce_streams',
                                      'nbconvert.preprocessors.SVG2PDFPreprocessor',
                                      'nbconvert.preprocessors.CSSHTMLHeaderPreprocessor',
                                      # 'nbconvert.preprocessors.LatexPreprocessor',
                                      'nbconvert.preprocessors.HighlightMagicsPreprocessor',
                                      # 'nbconvert.preprocessors.ExtractOutputPreprocessor',
                                      #'nbconvert.preprocessors.SnapshotPreProcessor'
                                  ])
                nbc =  copy.deepcopy(nb)
                resc = copy.deepcopy(resources)
                output, resources_html = html_exporter.from_notebook_node(nbc, resources=resc)
                writer = FilesWriter(build_directory=dirname)
                filename_base = 'index'
                filename = filename_base + '.html'
                writer.write(output, resources_html, notebook_name=filename_base)

                # dirname, filename = os.path.split(input)
                handlers = [
                    (r"/send_snapshot", SnapshotHandler, dict(snapshot_dict=self.snapshot_dict, callback=self.callback)),
                    (r"/dist/(.+)", web.StaticFileHandler, {'path' : DIRNAME_STATIC}),
                    (r"/(.+)", web.StaticFileHandler, {'path' : dirname}),
                    (r"/", web.RedirectHandler, {"url": "/%s" % filename})
                ]
                
                if ('://' in self.reveal_prefix or self.reveal_prefix.startswith("//")):
                    # reveal specifically from CDN, nothing to do
                    pass
                elif os.path.isdir(os.path.join(dirname, self.reveal_prefix)):
                    # reveal prefix exists
                    self.log.info("Serving local %s", self.reveal_prefix)
                else:
                    self.log.info("Redirecting %s requests to %s", self.reveal_prefix, self.reveal_cdn)
                    handlers.insert(0, (r"/(%s)/(.*)" % self.reveal_prefix, ProxyHandler))
                
                app = web.Application(handlers,
                                      cdn=self.reveal_cdn,
                                      client=AsyncHTTPClient(),
                                      )
                
                # hook up tornado logging to our logger
                log.app_log = self.log

                http_server = httpserver.HTTPServer(app)
                http_server.listen(self.port, address=self.ip)
                url = "http://%s:%i/%s" % (self.ip, self.port, filename)
                print("Serving your slides at %s" % url)
                print("Use Control-C to stop this server")
                self.main_ioloop = ioloop.IOLoop.instance()
                if self.open_in_browser:
                    try:
                        # b = lambda: browser.open(url, new=2)
                        # threading.Thread(target=b).start()
                        browser = webbrowser.get(self.browser or None)
                        b = lambda: browser.open(url, new=2)
                        threading.Thread(target=b).start()
                    except webbrowser.Error as e:
                        self.log.warning('No web browser found: %s.' % e)
                        browser = None

                try:
                    self.main_ioloop.start()
                except KeyboardInterrupt:
                    print("\nInterrupted")
                # nbformat.write(self.nb, input.replace('.html', '.ipynb'))
            # import IPython
            # IPython.embed()
            # import pdb
            # pdb.set_trace()
        return nb, resources

def main(path):
    """allow running this module to serve the slides"""
    server = SnapshotPreProcessor()
    server(path)
    
if __name__ == '__main__':
    import sys
    main(sys.argv[1])
