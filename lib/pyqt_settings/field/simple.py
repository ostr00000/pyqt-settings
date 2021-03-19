from PyQt5.QtCore import QVariant

from pyqt_settings.factory.base import WidgetFactory
from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit
from pyqt_settings.gui_widget.simple import CheckBoxFieldWidget, SpinBoxFieldWidget, \
    LineEditFieldWidget


class QVariantField(Field[QVariant]):
    """Field save QVariant without conversion."""

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.value(self.key, self.default)


class StrField(Field[str]):
    """Field represent python string."""

    def __init__(self, key, default=''):
        super().__init__(key, default, str)
        self.widgetFactory = WidgetFactory(LineEditFieldWidget)


class PathField(StrField):
    """Field represent file path in system."""

    def __init__(self, key, default=''):
        super().__init__(key, default)
        self.widgetFactory = WidgetFactory(PathLineEdit)


class IntField(Field):
    """Field represent python integer."""

    def __init__(self, key, default=0):
        super().__init__(key, default, int)
        self.widgetFactory = WidgetFactory(SpinBoxFieldWidget)


class BytesField(Field):
    """Field represent python bytes."""

    def __init__(self, key, default=b''):
        super().__init__(key, default, bytes)


class BoolField(Field):
    """Field represent python bool."""

    def __init__(self, key, default=False):
        super().__init__(key, default, bool)
        self.widgetFactory = WidgetFactory(CheckBoxFieldWidget)
