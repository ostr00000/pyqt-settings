import json
import logging
from typing import Type

from PyQt5.QtCore import QSettings

from pyqt_settings.field.string import StrField
from pyqt_utils.python.json_serializable import deepMapSequence, fromJson

logger = logging.getLogger(__name__)


class JsonField(StrField):
    def __init__(self, key, default='', jsonSerializeFun=None,
                 castTypes: deepMapSequence = None):
        super().__init__(key, default)
        self.castTypes = castTypes

        if jsonSerializeFun is not None:
            assert callable(jsonSerializeFun)
            self.jsonSerializeFun = jsonSerializeFun

    def __get__(self, instance: QSettings, owner: Type[QSettings]):
        if instance is None:
            return self

        try:
            val = super().__get__(instance, owner)
            return fromJson(val, self.castTypes)

        except TypeError as error:
            logger.error(error)
            return self.default

    def __set__(self, instance: QSettings, value):
        if not isinstance(value, str):
            value = json.dumps(value, default=self.jsonSerializeFun)
        super().__set__(instance, value)

    @classmethod
    def jsonSerializeFun(cls, x):
        return x.__dict__
