from PyQt5 import QtCore
from PyQt5.QtGui import QPageLayout, QPageSize
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView


class QtScreenshot(QWebEngineView):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def capture(self, url, output_file, paginate):
        self.output_file = output_file
        self.paginate = paginate
        self.load(QtCore.QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(QtCore.Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        if output_file.endswith(".pdf"):
            self.export = self.export_pdf
            self.page().pdfPrintingFinished.connect(lambda *args: self.app.exit())
        elif output_file.endswith(".png"):
            self.export = self.export_png
        else:
            raise RuntimeError(f"Export file extension not supported: {output_file}")
        self.show()
        self.app.exec()

    def on_loaded(self):
        self.size = self.page().contentsSize().toSize()
        self.resize(self.size)
        # Wait for resize
        QtCore.QTimer.singleShot(1000, self.export)

    def export_pdf(self):
        if self.paginate:
            page_size = QPageSize(QPageSize.A4)
            page_layout = QPageLayout(page_size, QPageLayout.Portrait, QtCore.QMarginsF())
        else:
            factor = 0.75
            page_size = QPageSize(
                QtCore.QSizeF(self.size.width() * factor, self.size.height() * factor),
                QPageSize.Point,
            )
            page_layout = QPageLayout(page_size, QPageLayout.Portrait, QtCore.QMarginsF())

        self.page().printToPdf(self.output_file, pageLayout=page_layout)

    def export_png(self):
        self.grab().save(self.output_file, b"PNG")
        self.app.quit()
