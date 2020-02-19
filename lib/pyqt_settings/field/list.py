import logging
from typing import Type

from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field

logger = logging.getLogger(__name__)


class ListField(Field):
    def __init__(self, key, default=(), castType=str):
        super().__init__(key, default, list)
        self.castType = castType

    def __get__(self, instance: QSettings, owner: Type[QSettings]):
        try:
            val = instance.value(self.key, self.default, self.type)
            return [self.castType(v) for v in val]
        except (TypeError, ValueError) as error:
            logger.error(error)
            return []

    def __set__(self, instance: QSettings, value):
        instance.setValue(self.key, value)
