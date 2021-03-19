import logging
from typing import Iterable

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QCompleter, QFileDialog, QWidget, QFileSystemModel

from pyqt_settings.factory.base import ConfigFunc
from pyqt_settings.gui_widget.base import FieldWidget
from pyqt_settings.ui.ui_path_widget import Ui_PathWidget
from pyqt_utils.ui_base_widget import BaseWidget

logger = logging.getLogger(__name__)


class PathLineEdit(Ui_PathWidget, BaseWidget, FieldWidget[str], QWidget):
    """Use kwargs 'configFunctions' to pass iterable with ConfigFunc for path dialog."""

    def __pre_init__(self, *args, configFunctions: Iterable[ConfigFunc] = (), **kwargs):
        super().__pre_init__(*args, **kwargs)
        self.configFunctions = configFunctions

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.fileSystemModel = QFileSystemModel(parent=self)
        self.fileSystemModel.setRootPath('/')
        self.fileSystemModel.setFilter(self.fileSystemModel.filter() | QDir.Hidden)
        self.completer = QCompleter(self.fileSystemModel, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.lineEdit.setCompleter(self.completer)

        self.toolButton.clicked.connect(self.onToolButtonClicked)

    def getValue(self) -> str:
        return self.lineEdit.text()

    def setValue(self, value: str):
        self.lineEdit.setText(value)
        self.fileSystemModel.index(value)

    def onToolButtonClicked(self):
        curPath = self.getValue()
        dialog = QFileDialog(self, "Select path", curPath)

        for confFunc in self.configFunctions:
            confFunc(dialog)

        if dialog.exec():
            fileName, *_ = dialog.selectedFiles()
            self.setValue(fileName)
