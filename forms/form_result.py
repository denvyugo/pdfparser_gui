from PyQt5.QtWidgets import (QWidget, QTreeWidgetItem)

from forms import form_result_ui


class Result(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = form_result_ui.Ui_Results()
        self.ui.setupUi(self)
        # connect signals

    def fill_results(self, results):
        """fill tree view from results list"""
        tree_widget = self.ui.treeResults
        for file in results:
            file_item = QTreeWidgetItem(tree_widget)
            file_item.setText(0, file['file'])
            for i, part in enumerate(file['parts'], 1):
                part_item = QTreeWidgetItem(file_item)
                part_item.setText(0, f'page {i}')
                for key, val in part.items():
                    QTreeWidgetItem(part_item, [key, val])
