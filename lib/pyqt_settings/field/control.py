from typing import Type, TypeVar, Union

from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.factory.control import ControlWidgetFactory

Field_T = TypeVar('Field_T', bound=Field)


class ControlledField(Field[Field_T]):
    def __init__(self, supervisor: BoolField, controlled: Field[Field_T]):
        super().__init__('')
        self.supervisor = supervisor
        self.controlled = controlled
        self.widgetFactory = ControlWidgetFactory(supervisor, controlled)

    def isControlled(self, instance, owner=QSettings):
        return self.supervisor.__get__(instance, owner)

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> Union[Field_T]:
        if instance is None:
            return self
        if self.isControlled(instance, owner):
            return self.controlled.__get__(instance, owner)
        else:
            return self.controlled.default

    def __set__(self, instance: QSettings, value: Field_T):
        if self.isControlled(instance):
            self.controlled.__set__(instance, value)
            return True
        return False
