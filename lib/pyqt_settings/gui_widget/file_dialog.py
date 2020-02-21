from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QLineEdit, QToolButton, \
    QFileDialog, QHBoxLayout

from pyqt_settings.factory.config_fun import ConfigFunc
from pyqt_settings.gui_widget.base import FieldWidget


class FileDialogFieldWidget(FieldWidget[str]):

    def __init__(self, *configFunction: ConfigFunc):
        """
        function - Unbound method for QFileDialog (self will be provided)
        args - arguments for this function
        """
        super().__init__()
        self.configFunctions = configFunction

        self.lineEdit = QLineEdit(self)
        self.selectFileButton = QToolButton(self)
        self.selectFileButton.setText('...')
        self.selectFileButton.clicked.connect(self.onSelectFileClicked)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(QMargins())
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.selectFileButton)

    def onSelectFileClicked(self):
        dialog = QFileDialog()
        for configFunc in self.configFunctions:
            configFunc(dialog)

        if dialog.exec():
            fileName, *_ = dialog.selectedFiles()
            self.lineEdit.setText(fileName)

    def getValue(self):
        return self.lineEdit.text()

    def setValue(self, value):
        self.lineEdit.setText(value)
