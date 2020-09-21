import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMdiSubWindow, qApp, QApplication)

from forms import form_main_ui, form_sample


class Parser(QMainWindow):
    """class for main window of PDFParser"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = form_main_ui.Ui_PDFparser()
        self.ui.setupUi(self)
        # connect signals
        self.ui.actionOpen_sample.triggered.connect(self.open_sample)
        self.ui.actionExit.triggered.connect(qApp.exit)
        # self properties
        self.sample_pdf = ''
        self._sub = []
        self._sub_forms = {'sample': form_sample}

    def open_sample(self):
        """open sample pdf document to parse text"""
        if not self.sample_pdf:
            file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open sample PDF file',
                directory=os.getcwd(),
                filter='PDF Files (*.pdf)')
            if file_name:
                if os.path.isfile(file_name[0]):
                    self.sample_pdf = file_name[0]
                    sub_form = form_sample.Sample(self)
                    self.add_sub_form(sub_form)
                    sub_form.get_sample_text(self.sample_pdf)
                    sub_form.main = self

    def add_sub_form(self, form):
        """add sub form to main window"""
        child = self.ui.mdiArea.addSubWindow(form)
        self._sub.append(child)
        child.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Parser()
    win.show()
    sys.exit(app.exec_())
