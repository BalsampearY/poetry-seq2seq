import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide2.QtCore import QObject, QFile, QTranslator, Slot, QStringListModel
from .ui_mainwindow import Ui_MainWindow

# from poetry import predict
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(APP_DIR, 'resources')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.APP_NAME = self.tr('Poetry Generator')

        self.ui = Ui_MainWindow()
        ui = self.ui
        ui.setupUi(self)
        ui.button_generate.clicked.connect(self.generate_poetry)
        ui.lineedit_keyword.returnPressed.connect(self.add_keyword)
        ui.button_delete_keyword.clicked.connect(self.delete_keyword)

        self.keyword_model = QStringListModel(self)
        self.keyword_model.setStringList(['人', '工', '智', '能'])
        ui.listview_keyword.setModel(self.keyword_model)

    @Slot(None, name='add_keyword')
    def add_keyword(self):
        lineedit_keyword = self.ui.lineedit_keyword
        text = lineedit_keyword.text()
        if text is not None or text != '':
            lineedit_keyword.clear()
            self.keyword_model.insertRow(0)
            index = self.keyword_model.index(0)
            self.keyword_model.setData(index, text)

    @Slot(None, name='delete_keyword')
    def delete_keyword(self):
        index = self.ui.listview_keyword.currentIndex()
        row = index.row()
        print(row)
        if row != -1:
            self.keyword_model.removeRow(row)

    @Slot(None, name='generate_poetry')
    def generate_poetry(self):
        if self.keyword_model.rowCount() <= 0:
            QMessageBox.warning(self, self.APP_NAME, self.tr(
                'Please add some keywords first!'))
            return
        poetry = '\n'.join(self.keyword_model.stringList())
        self.ui.label_poetry.setText(poetry)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    translator = QTranslator(app)
    translator.load(os.path.join(RES_DIR, 'main_zhcn'))
    app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
