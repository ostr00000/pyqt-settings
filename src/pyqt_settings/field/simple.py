import contextlib
import logging

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


class BytesField(Field[bytes | QByteArray]):
    """Field represent python bytes."""

    def __init__(self, key, default=b""):
        super().__init__(key, default, bytes)

    def __get__(
        self, instance: QSettings, owner: type[QSettings]
    ) -> bytes | QByteArray | Field:
        if instance is None:
            return self

        with contextlib.suppress(TypeError):
            return instance.value(self.key, self.default, self.typeAsClass)

        try:
            return instance.value(self.key, self.default, QByteArray)
        except TypeError:
            logger.exception("Cannot get value - fallback to default")
            return self.default


class BoolField(Field[bool]):
    """Field represent python bool."""

    def __init__(self, key, *, default=False):
        super().__init__(key, default, bool)
        self.widgetFactory = WidgetFactory(CheckBoxFieldWidget)
