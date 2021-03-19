import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, \
    QFileDialog

from pyqt_settings.dialog import createSettingDialogClass
from pyqt_settings.factory.base import WidgetFactory, ConfigFunc
from pyqt_settings.field.control import ControlledField
from pyqt_settings.field.list import ListField
from pyqt_settings.field.simple import StrField, IntField, BoolField
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit
from pyqt_settings.gui_widget.simple import LineEditFieldWidget, ComboBoxFieldWidget


class MySettings(QSettings):
    label = StrField('test/label', default='Empty!')

    TEST_ADVANCED_NAME = BoolField('test/name', default=True)
    NUMBER = IntField('number/test', default=13)
    ControlInt = ControlledField(TEST_ADVANCED_NAME, NUMBER)

    override_Logger = BoolField('log/override', default=False)
    LOGGER = StrField('log/level', default='INFO')
    LOGGER.widgetFactory = WidgetFactory(
        ComboBoxFieldWidget, 'INFO', 'DEBUG')
    ControlLogger = ControlledField(override_Logger, LOGGER)

    textText = IntField('test/text')
    textText.widgetFactory = WidgetFactory(LineEditFieldWidget)

    test_path = StrField('test/path')
    test_path.widgetFactory = WidgetFactory(
        PathLineEdit, configFunctions=[
            ConfigFunc(QFileDialog.setWindowTitle, 'Select any dir'),
            ConfigFunc(QFileDialog.setFileMode, QFileDialog.Directory)]
    )

    List_Text = ListField('test/list')


mySettings = MySettings('ostr00000', 'SettingsTest')
SettingDialog = createSettingDialogClass(mySettings)


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
