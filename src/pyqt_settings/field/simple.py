import logging
from typing import Self, overload

from PyQt5.QtCore import QByteArray, QSettings, QVariant

from pyqt_settings.factory.base import WidgetFactory
from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit
from pyqt_settings.gui_widget.simple import (
    CheckBoxFieldWidget,
    LineEditFieldWidget,
    SpinBoxFieldWidget,
)

logger = logging.getLogger(__name__)


class QVariantField(Field[QVariant]):
    """Field save QVariant without conversion."""

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.value(self.key, self.default)


class StrField(Field[str]):
    """Field represent python string."""

    def __init__(self, key, default=""):
        super().__init__(key, default, str)
        self.widgetFactory = WidgetFactory(LineEditFieldWidget)


class PathField(StrField):
    """Field represent file path in system."""

    def __init__(self, key, default=""):
        super().__init__(key, default)
        self.widgetFactory = WidgetFactory(PathLineEdit)


class IntField(Field[int]):
    """Field represent python integer."""

    def __init__(self, key, default=0):
        super().__init__(key, default, int)
        self.widgetFactory = WidgetFactory(SpinBoxFieldWidget)


# future update:
#  class BytesField(Field[bytes, QByteArray | bytes | bytearray]):
class BytesField(Field[bytes]):
    """Field represent python bytes."""

    def __init__(self, key, default=b""):
        super().__init__(key, default, bytes)

    @overload
    def __get__(self, instance: None, owner: type[QSettings]) -> Self: ...

    @overload
    def __get__(self, instance: QSettings, owner: type[QSettings]) -> bytes: ...

    def __get__(
        self, instance: QSettings | None, owner: type[QSettings]
    ) -> bytes | Self:
        if instance is None:
            return self

        try:
            bytesObj = instance.value(self.key, self.default, self.typeAsClass)
        except TypeError:
            try:
                bytesObj = instance.value(self.key, self.default, QByteArray)
            except TypeError:
                logger.exception("Cannot get value - fallback to default")
                bytesObj = self.default

        match bytesObj:
            case QByteArray() as bA:
                return bA.data()
            case bytes(rawBytes):
                return rawBytes
            case _:
                msg = f"Unexpected type for {self.key}: {type(bytesObj)}"
                raise TypeError(msg)

    def __set__(self, instance: QSettings, value: QByteArray | bytes | bytearray):
        super().__set__(
            instance,
            QByteArray(value),  # type: ignore[reportArgumentType]
        )


class BoolField(Field[bool]):
    """Field represent python bool."""

    def __init__(self, key, *, default=False):
        super().__init__(key, default, bool)
        self.widgetFactory = WidgetFactory(CheckBoxFieldWidget)
