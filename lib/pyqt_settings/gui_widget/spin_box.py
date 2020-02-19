from PyQt5.QtWidgets import QSpinBox

from pyqt_settings.gui_widget.base import FieldWidget


class SpinBoxFieldWidget(QSpinBox, FieldWidget[int]):
    def getValue(self):
        return self.value()
