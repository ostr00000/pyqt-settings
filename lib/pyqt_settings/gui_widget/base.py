from typing import TypeVar, Generic

from PyQt5.QtWidgets import QWidget

T = TypeVar('T')


class FieldWidget(QWidget, Generic[T]):
    def getValue(self) -> T:
        raise NotImplementedError

    def setValue(self, value: T):
        raise NotImplementedError
