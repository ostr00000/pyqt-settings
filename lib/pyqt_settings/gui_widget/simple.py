import logging

from PyQt5.QtWidgets import QCheckBox, QSpinBox, QLineEdit, QComboBox

from pyqt_settings.gui_widget.base import FieldWidget
from pyqt_utils.widgets.space_line_edit import SpaceLineEdit

logger = logging.getLogger(__name__)


class CheckBoxFieldWidget(QCheckBox, FieldWidget[bool]):
    def getValue(self):
        return self.isChecked()

    def setValue(self, value):
        self.setChecked(value)


class SpinBoxFieldWidget(QSpinBox, FieldWidget[int]):
    def __init__(self):
        super().__init__()
        self.setMaximum(1_000_000)
        self.setAccelerated(True)

    def getValue(self):
        return self.value()


class LineEditFieldWidget(QLineEdit, FieldWidget[str]):
    def getValue(self):
        return self.text()

    def setValue(self, value):
        self.setText(str(value))


class SpaceLineFieldWidget(SpaceLineEdit, FieldWidget[list]):
    def getValue(self) -> list:
        values = self.getValues()
        return values

    def setValue(self, value: list):
        self.setValues(value)


class ComboBoxFieldWidget(QComboBox, FieldWidget[str]):
    def __init__(self, *items: str):
        super().__init__()
        self.items = items
        self.addItems(items)

    def getValue(self):
        return self.currentText()

    def setValue(self, value: str | int):
        if isinstance(value, str):
            try:
                index = self.items.index(value)
            except ValueError:
                logger.error(f'Unexpected string value "{value}"')
                index = 0
        elif isinstance(value, int):
            index = value
        else:
            raise ValueError
        self.setCurrentIndex(index)
