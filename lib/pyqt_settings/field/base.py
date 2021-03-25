from __future__ import annotations

import logging
import re
from functools import cached_property
from typing import TypeVar, Generic, Type, Union, Optional, Callable

from PyQt5.QtCore import QSettings, pyqtProperty, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)
T = TypeVar('T')
WidgetFactory_t = Union[
    Callable[[QSettings, 'Field'], FieldWidget],
    Type[FieldWidget],
]


class DirtyController:
    def __init__(self, widget: FieldWidget, field: Field):
        self.widget = widget
        self.startValue = widget.getValue()
        try:
            widget.valueChanged.connect(self._setDirty)
        except AttributeError:
            pass
        field.valueChanged.connect(self.resetStartValue)

    def resetStartValue(self, newStartValue):
        self.startValue = newStartValue
        self._setDirty()

    def _setDirty(self):
        curValue = self.widget.getValue()
        if curValue == self.startValue:
            toolTip, style = '', ''
        else:
            style = 'border: 2px solid orange;'
            toolTip = 'Unsaved changes'
        self.widget.setStyleSheet(style)
        self.widget.setToolTip(toolTip)


class FieldWidgetWithLabel(QWidget):
    def __init__(self, fieldWidget: FieldWidget, label: str,
                 layoutType=QHBoxLayout, field: Field = None,
                 settings: QSettings = None, connectSaveButton=True,
                 parent=None):
        super().__init__(parent)
        self.fieldWidget = fieldWidget
        self.field = field
        self.dirty = DirtyController(fieldWidget, field)
        self.settings = settings
        self.button = QPushButton('Save')

        if field and connectSaveButton:
            self.button.clicked.connect(self.onButtonClicked)

        layout = layoutType(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(QLabel(label + ':'))
        layout.addWidget(fieldWidget)
        layout.addWidget(self.button)

    def onButtonClicked(self):
        value = self.fieldWidget.getValue()
        self.field.__set__(self.settings, value)

    def replaceWidget(self, placeHolder: QWidget):
        layout = placeHolder.parentWidget().layout()
        layout.replaceWidget(placeHolder, self)
        placeHolder.deleteLater()


class SigWrapper(QObject):
    valueChanged = pyqtSignal(object)

    def connect(self, fun):
        self.valueChanged.connect(fun)

    def disconnect(self, fun=None):
        self.valueChanged.disconnect(fun)

    def emit(self, value):
        self.valueChanged.emit(value)


class Field(pyqtProperty, Generic[T]):
    @cached_property
    def valueChanged(self):
        return SigWrapper()

    def __init__(self, key: str, default: T = None, type_: Type[T] = None):
        super().__init__(object if type_ is None else type_)
        if type_ is not None:
            default = type_(default)
        self.key = key
        self.default = default
        self.widgetFactory: Optional[WidgetFactory_t] = None
        self.name = None

    def __set_name__(self, owner: QSettings, name: str):
        self.name = name

    def createWidget(self, instance: QSettings) -> Optional[FieldWidget]:
        if self.widgetFactory is None:
            return None

        widget = self.widgetFactory(instance, self)
        widget.setValue(self.__get__(instance, type(instance)))
        self.valueChanged.connect(widget.setValue)
        return widget

    def createWidgetWithLabel(
            self, instance: QSettings, parent=None, **kwargs
    ) -> FieldWidgetWithLabel:
        widget = self.createWidget(instance)
        widgetWithLabel = FieldWidgetWithLabel(
            widget, self.displayName, field=self,
            settings=instance, parent=parent, **kwargs)
        return widgetWithLabel

    @cached_property
    def displayName(self):
        """To square bracket ([]) use _LL and JJ.
        All underscores (_) become spaces ( )."""
        dn = self.name.replace('_LL', '_[').replace('JJ', ']')
        dn = re.sub('([A-Z]+)', r'_\1', dn).replace('__', ' ')
        dn = dn.lower().replace('_', ' ').strip().capitalize()
        return dn

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
        self.valueChanged.emit(value)
