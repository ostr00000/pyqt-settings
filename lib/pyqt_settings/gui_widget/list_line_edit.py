from typing import List

from pyqt_settings.gui_widget.base import FieldWidget
from pyqt_settings.widgets.space_line_edit import SpaceLineEdit


class SpaceLineFieldWidget(SpaceLineEdit, FieldWidget[List]):
    def getValue(self) -> List:
        values = self.getValues()
        return values

    def setValue(self, value: List):
        self.setValues(value)
