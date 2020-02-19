import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, \
    QFileDialog

from pyqt_settings.dialog import SettingDialog, settingDialogSavePosition
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.field.control import ControlledField
from pyqt_settings.field.integer import IntField
from pyqt_settings.field.string import StrField
from pyqt_settings.gui_widget.file_dialog import FileDialogFieldWidget


class MySettings(QSettings):
    label = StrField('test/label', default='Empty!')

    TEST_ADVANCED_NAME = BoolField('test/name', default=True)
    NUMBER = IntField('number/test', default=13)
    ControlInt = ControlledField(TEST_ADVANCED_NAME, NUMBER)

    path = StrField('test/path')
    path.widgetClass = FileDialogFieldWidget
    path.widgetArgs = (
        {QFileDialog.setWindowTitle: ('Select any dir',),
         QFileDialog.setFileMode: (QFileDialog.Directory,),
         },)


mySettings = MySettings('ostr00000', 'SettingsTest')
settingDialogSavePosition(mySettings)


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalLayout = QVBoxLayout(self)
        self.button = QPushButton("Settings")
        self.button.clicked.connect(self.onSettingButtonClicked)
        self.verticalLayout.addWidget(self.button)

    def onSettingButtonClicked(self):
        SettingDialog(mySettings, parent=self).exec()


def main():
    app = QApplication([])

    mmw = QMainWindow()
    mw = MyWidget(mmw)
    mmw.setCentralWidget(mw)
    mmw.show()

    app.exec()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
