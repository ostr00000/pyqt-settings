import logging
from typing import Union

from PyQt5.QtWidgets import QComboBox

from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)


class ComboBoxFieldWidget(QComboBox, FieldWidget[str]):
    def __init__(self, *items: str):
        super().__init__()
        self.items = items
        self.addItems(items)

    def getValue(self):
        return self.currentText()

    def setValue(self, value: Union[str, int]):
        if isinstance(value, str):
            try:
                index = self.items.index(value)
            except ValueError:
                logger.error('Unexpected string value "{}"'.format(value))
                index = 0
        elif isinstance(value, int):
            index = value
        else:
            assert False
        self.setCurrentIndex(index)
