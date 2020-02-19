from typing import Dict, Callable, Tuple

from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QLineEdit, QWidget, QToolButton, \
    QFileDialog, QHBoxLayout

from pyqt_settings.gui_widget.base import FieldWidget


class FileDialogFieldWidget(QWidget, FieldWidget[str]):

    def __init__(self, function2args: Dict[Callable, Tuple] = None):
        """
        function - Unbound method for QFileDialog (self will be provided)
        args - arguments for this function
        """
        super().__init__()
        self.function2args = dict(function2args or {})

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
        for function, args in self.function2args.items():
            function(dialog, *args)

        if dialog.exec():
            fileName, *_ = dialog.selectedFiles()
            self.lineEdit.setText(fileName)

    def getValue(self):
        return self.lineEdit.text()

    def setValue(self, value):
        self.lineEdit.setText(value)
