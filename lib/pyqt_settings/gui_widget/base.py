from __future__ import annotations

from typing import TypeVar, Generic

from PyQt5.QtWidgets import QWidget

T = TypeVar('T')


class FieldWidget(QWidget, Generic[T]):
    """Abstract class represent value from settings as widget"""

    def getValue(self) -> T:
        """Return current settings value."""
        raise NotImplementedError

    def setValue(self, value: T):
        """The value may comes from different source than settings."""
        raise NotImplementedError
