import re
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from forms import form_sample_ui, form_result
from utils.pdfread import get_text_pdf, make_parse


class Sample(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = form_sample_ui.Ui_Sample()
        self.ui.setupUi(self)
        # connect signals
        self.ui.checkPattern.clicked.connect(self.check_match_pattern)
        self.ui.addField.clicked.connect(self.add_field_pattern)
        self.ui.delField.clicked.connect(self.del_field_pattern)
        self.ui.performParse.clicked.connect(self.perform_parse)
        self.main = None

    def get_sample_text(self, sample_file):
        """parse tex and get it in plain text widget"""
        text = get_text_pdf(sample_file)
        self.ui.plainTextEdit.appendPlainText(text)

    def check_match_pattern(self):
        """check if pattern in text line is match a substring of text"""
        text = self.ui.plainTextEdit.toPlainText()
        pattern = self.ui.textPattern.text()
        result = re.search(pattern, text)
        group = int(self.ui.spinGroup.text())
        if result:
            self.ui.textMatch.setText(result.group(group))

    def add_field_pattern(self):
        """add field pattern to table"""
        table = self.ui.tableFields
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(self.ui.textField.text()))
        table.setItem(row, 1, QTableWidgetItem(self.ui.textPattern.text()))
        table.setItem(row, 2, QTableWidgetItem(self.ui.spinGroup.text()))

    def del_field_pattern(self):
        """delete row from the table of patterns"""
        self.ui.tableFields.removeRow(self.ui.tableFields.currentRow())

    def perform_parse(self):
        """perform parse pdf files with set of patterns from the table"""
        # get folder of pdf files
        folder = QFileDialog.getExistingDirectory(
            parent=self.parent(),
            caption='Get folder with PDF documents to parse'
        )
        if folder:
            # get list of fields and patterns
            field_list = self._get_fields()
            # performing parse
            results = make_parse(folder, field_list)
            self.open_result(results)

    def open_result(self, results):
        """show widget with tree of results of parsing"""
        sub_result = form_result.Result()
        sub_result.resize(300, 400)
        self.main.add_sub_form(sub_result)
        sub_result.fill_results(results)

    def _get_fields(self):
        """get fields and patterns from the table, return list of tuples"""
        table = self.ui.tableFields
        rows = table.rowCount()
        cols = table.columnCount()
        fields = []
        for i in range(rows):
            fields.append(
                tuple(map(lambda x: table.item(i, x).text(), range(cols)))
            )
        return fields

    def _load_table(self, field_list):
        """load table of field from list of patterns"""
        for i, patterns in enumerate(field_list):
            self.ui.tableFields.insertRow(i)
            for j, item in enumerate(patterns):
                self.ui.tableFields.setItem(i, j, QTableWidgetItem(item))
