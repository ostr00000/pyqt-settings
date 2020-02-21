from __future__ import annotations

import logging
from typing import Type, List, Generic, TypeVar, Union, Callable

from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field

logger = logging.getLogger(__name__)
S = TypeVar('S')


class ListField(Field[List], Generic[S]):

    def __init__(self, key, default=(), castType: Callable[[str], S] = str):
        super().__init__(key, default, list)
        self.castType = castType

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> Union[ListField, List[S]]:
        if instance is None:
            return self
        try:
            val = instance.value(self.key, self.default, self.type)
            return [self.castType(v) for v in val]
        except (TypeError, ValueError) as error:
            logger.error(error)
            return []

    def __set__(self, instance: QSettings, value):
        instance.setValue(self.key, value)
