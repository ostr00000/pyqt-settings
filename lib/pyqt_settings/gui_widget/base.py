from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

if TYPE_CHECKING:
    from pyqt_settings.setting_creator import SettingCreator

T = TypeVar('T')


class FieldWidget(QWidget, Generic[T]):
    def setCreator(self, creator: SettingCreator):
        pass

    def getValue(self) -> T:
        raise NotImplementedError

    def setValue(self, value: T):
        raise NotImplementedError
