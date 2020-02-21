from PyQt5.QtWidgets import QLineEdit

from pyqt_settings.gui_widget.base import FieldWidget


class LineEditFieldWidget(QLineEdit, FieldWidget[str]):
    def getValue(self):
        return self.text()

    def setValue(self, value):
        self.setText(str(value))
