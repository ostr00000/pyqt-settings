from __future__ import annotations

import logging
from typing import TypeVar, Generic, Type, Union, Optional, Callable

from PyQt5.QtCore import QSettings

from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)
T = TypeVar('T')


class Field(Generic[T]):

    def __init__(self, key: str, default: T = None, type_: Type[T] = None):
        self.key = key
        if type_ is not None:
            default = type_(default)
        self.default = default
        self.type = type_
        self.widgetFactory: Optional[Callable[[], FieldWidget]] = None
        self.widget = None

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> Union[T, Field]:
        if instance is None:
            return self
        try:
            return instance.value(self.key, self.default, self.type)
        except TypeError as err:
            logger.error(err)
            return self.default

    def __set__(self, instance: QSettings, value: T):
        instance.setValue(self.key, value)
