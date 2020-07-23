from PyQt5.QtWidgets import QSpinBox

from pyqt_settings.gui_widget.base import FieldWidget


class SpinBoxFieldWidget(QSpinBox, FieldWidget[int]):
    def __init__(self):
        super().__init__()
        self.setMaximum(1_000_000)
        self.setAccelerated(True)

    def getValue(self):
        return self.value()
