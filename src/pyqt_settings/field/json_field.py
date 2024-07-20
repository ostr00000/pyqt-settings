import json
import logging
from collections.abc import Callable
from typing import Self, overload

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

    @overload
    def __get__(self, instance: None, owner: type[QSettings]) -> Self: ...

    @overload
    def __get__(self, instance: QSettings, owner: type[QSettings]) -> C: ...

    def __get__(self, instance: QSettings | None, owner: type[QSettings]) -> C | Self:
        if instance is None:
            return self

        val = self.default
        try:
            val = super().__get__(instance, owner)
        except TypeError:
            logger.exception("Cannot extract or cast value - fallback to default")

        return self.castType(val)

    def __set__(self, instance: QSettings, value: C | str):
        if not isinstance(value, str):
            value = self.jsonSerializeFun(value)
        super().__set__(instance, value)
