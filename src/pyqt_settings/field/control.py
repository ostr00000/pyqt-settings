from PyQt5.QtCore import QSettings

from pyqt_settings.factory.control import ControlWidgetFactory
from pyqt_settings.field.base import Field
from pyqt_settings.field.simple import BoolField


class ControlledField[T](Field[T]):
    def __init__(self, supervisor: BoolField, controlled: Field[T]):
        super().__init__("", controlled.default)
        self.supervisor = supervisor
        self.controlled = controlled
        self.widgetFactory = ControlWidgetFactory(supervisor, controlled)

    def isControlled(self, instance, owner=QSettings):
        return self.supervisor.__get__(instance, owner)

    def __get__(self, instance: QSettings, owner: type[QSettings]) -> T:
        if instance is None:
            return self

        if self.isControlled(instance, owner):
            return self.controlled.__get__(instance, owner)

        return self.controlled.default

    def __set__(self, instance: QSettings, value: T):
        if self.isControlled(instance):
            self.controlled.__set__(instance, value)
            return True
        return False
