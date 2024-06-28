import json
import logging
from collections.abc import Callable

from PyQt5.QtCore import QSettings

from pyqt_settings.field.simple import StrField

logger = logging.getLogger(__name__)


def dumpToJsonDict(obj):
    return json.dumps(obj, default=lambda x: x.__dict__)


class JsonField[C](StrField):
    def __init__(
        self,
        key: str,
        default: str = "",
        jsonSerializeFun: Callable[[C], str] = dumpToJsonDict,
        castType: Callable[[str], C] = json.loads,
    ):
        super().__init__(key, default)

        if not callable(castType):
            raise TypeError
        self.castType = castType

        if not callable(jsonSerializeFun):
            raise TypeError
        self.jsonSerializeFun = jsonSerializeFun

    def __get__(self, instance: QSettings, owner: type[QSettings]):
        if instance is None:
            return self

        try:
            if not (val := super().__get__(instance, owner)):
                return self.default
            return self.castType(val)

        except TypeError:
            logger.exception("Cannot extract or cast value - fallback to default")
            return self.default

    def __set__(self, instance: QSettings, value):
        if not isinstance(value, str):
            value = self.jsonSerializeFun(value)
        super().__set__(instance, value)
