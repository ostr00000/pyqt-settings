from __future__ import annotations

import logging
import re
from functools import cached_property
from typing import TYPE_CHECKING, Protocol, Self, overload

from PyQt5.QtCore import QObject, QSettings, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QPushButton, QWidget

if TYPE_CHECKING:
    from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)


class WidgetFactoryType[T](Protocol):
    def __call__(
        self, *, settings: QSettings, field: Field[T], **factoryKwargs
    ) -> FieldWidget[T]: ...


class DirtyController[T]:
    def __init__(self, widget: FieldWidget[T], field: Field[T]):
        self.widget = widget
        self.startValue = widget.getValue()

        if (sig := getattr(widget, 'valueChanged', None)) is not None:
            sig.connect(self._setDirty)

        field.valueChanged.connect(self.resetStartValue)

    def resetStartValue(self, newStartValue):
        self.startValue = newStartValue
        self._setDirty()

    def _setDirty(self):
        curValue = self.widget.getValue()
        if curValue == self.startValue:
            toolTip, style = "", ""
        else:
            style = "border: 2px solid orange;"
            toolTip = "Unsaved changes"
        self.widget.setStyleSheet(style)
        self.widget.setToolTip(toolTip)


class FieldWidgetWithLabel[T](QWidget):
    def __init__(
        self,
        fieldWidget: FieldWidget[T],
        label: str,
        layoutType: type[QLayout] = QHBoxLayout,
        *,
        field: Field[T],
        settings: QSettings,
        connectSaveButton: bool = True,
        parent: QWidget | None = None,
        **kwargs,
    ):
        super().__init__(parent=parent, **kwargs)
        self.fieldWidget = fieldWidget
        self.field = field
        self.dirty = DirtyController(fieldWidget, field)
        self.settings = settings
        self.button = QPushButton("Save")

        if field and connectSaveButton:
            self.button.clicked.connect(self.onButtonClicked)

        layout = layoutType(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(QLabel(label + ":"))
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
        if fun is None:
            self.valueChanged.disconnect()
        else:
            self.valueChanged.disconnect(fun)

    def emit(self, value):
        self.valueChanged.emit(value)


class Field[T](pyqtProperty):
    @cached_property
    def valueChanged(self):
        return SigWrapper()

    def __init__(self, key: str, default: T, type_: type[T | object] = object):
        super().__init__(type_)
        self.key = key
        self.default = default
        self.widgetFactory: WidgetFactoryType[T] | None = None
        self._name: str | None = None

    def __set_name__(self, owner: QSettings, name: str):
        self._name = name

    @property
    def name(self):
        if self._name is None:
            msg = (
                "`Field` class must be defined in class scope "
                "before accessing `name` property"
            )
            raise TypeError(msg)
        return self._name

    @property
    def typeAsClass(self) -> type:
        if isinstance(self.type, str):
            raise TypeError
        return self.type

    def createWidget(self, instance: QSettings) -> FieldWidget | None:
        if self.widgetFactory is None:
            return None

        widget = self.widgetFactory(settings=instance, field=self)
        widget.setValue(self.__get__(instance, type(instance)))
        self.valueChanged.connect(widget.setValue)
        return widget

    def createWidgetWithLabel(
        self, instance: QSettings, parent=None, **kwargs
    ) -> FieldWidgetWithLabel:
        if (widget := self.createWidget(instance)) is None:
            msg = f"There is no widget factory for {self.name}"
            raise TypeError(msg)

        return FieldWidgetWithLabel(
            widget,
            self.displayName,
            field=self,
            settings=instance,
            parent=parent,
            **kwargs,
        )

    @cached_property
    def displayName(self):
        """
        Generate display name based on variable name.

        This function use following mapping:
        - `_LL` -> `[`
        - `JJ` -> `]`
        - `_` -> ` ` (space).
        """
        dn = self.name.replace("_LL", "_[").replace("JJ", "]")
        dn = re.sub("([A-Z]+)", r"_\1", dn).replace("__", " ")
        return dn.lower().replace("_", " ").strip().capitalize()

    @overload
    def __get__(self, instance: None, owner: type[QSettings]) -> Self: ...

    @overload
    def __get__(self, instance: QSettings, owner: type[QSettings]) -> T: ...

    def __get__(self, instance: QSettings | None, owner: type[QSettings]) -> T | Self:
        if instance is None:
            return self
        try:
            return instance.value(self.key, self.default, self.typeAsClass)
        except TypeError:
            logger.exception("Cannot get value - fallback to default")
            return self.default

    def __set__(self, instance: QSettings, value: T):
        instance.setValue(self.key, value)
        self.valueChanged.emit(value)
