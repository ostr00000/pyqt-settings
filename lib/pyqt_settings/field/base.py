from typing import TypeVar, Generic, Type

from PyQt5.QtCore import QSettings

from pyqt_settings.gui_widget.base import FieldWidget

T = TypeVar('T')


class Field(Generic[T]):
    widgetClass: Type[FieldWidget]
    widgetArgs = ()

    def __init__(self, key: str, default: T = None, type_: Type[T] = None):
        self.key = key
        self.default = default
        self.type = type_

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> T:
        return instance.value(self.key, self.default, self.type)

    def __set__(self, instance: QSettings, value: T):
        instance.setValue(self.key, value)
