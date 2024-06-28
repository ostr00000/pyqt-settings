import logging

from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QSpinBox
from pyqt_utils.widgets.multi_level_space_line_edit import ScrollSpaceLineEdit

from pyqt_settings.gui_widget.base import FieldWidget, FieldWidgetInit

logger = logging.getLogger(__name__)


class CheckBoxFieldWidget(FieldWidgetInit[bool], QCheckBox, FieldWidget[bool]):
    def getValue(self):
        return self.isChecked()

    def setValue(self, value):
        self.setChecked(value)


class SpinBoxFieldWidget(QSpinBox, FieldWidget[int]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setMaximum(1_000_000)
        self.setAccelerated(True)

    def getValue(self):
        return self.value()


class LineEditFieldWidget(FieldWidgetInit[str], QLineEdit, FieldWidget[str]):
    def getValue(self):
        return self.text()

    def setValue(self, value):
        self.setText(str(value))


class SpaceLineFieldWidget(ScrollSpaceLineEdit, FieldWidget[list]):

    def getValue(self) -> list:
        return self.getValues()

    def setValue(self, value: list):
        self.setValues(value)


class ComboBoxFieldWidget(QComboBox, FieldWidget[str]):
    def __init__(self, items: list[str], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        self.addItems(items)

    def getValue(self):
        return self.currentText()

    def setValue(self, value: str | int):
        match value:
            case str(v):
                try:
                    index = self.items.index(v)
                except ValueError:
                    logger.exception(f"Unexpected string value `{v}`")
                    index = 0
            case int(index):
                pass
            case _:
                raise TypeError(type(value))

        self.setCurrentIndex(index)
