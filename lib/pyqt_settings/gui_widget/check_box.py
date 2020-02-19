from PyQt5.QtWidgets import QCheckBox

from pyqt_settings.gui_widget.base import FieldWidget


class CheckBoxFieldWidget(QCheckBox, FieldWidget[bool]):
    def getValue(self):
        return self.isChecked()

    def setValue(self, value):
        self.setChecked(value)
