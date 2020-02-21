from typing import Type

from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field
from pyqt_settings.factory.base import WidgetFactory
from pyqt_settings.gui_widget.line_edit import LineEditFieldWidget


class StrField(Field[str]):
    def __init__(self, key, default=''):
        super().__init__(key, default, str)
        self.widgetFactory = WidgetFactory(LineEditFieldWidget)

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> str:
        return super().__get__(instance, owner)
