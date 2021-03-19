from __future__ import annotations

import logging
import re
from functools import cached_property
from typing import TypeVar, Generic, Type, Union, Optional, Callable

from PyQt5.QtCore import QSettings, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFormLayout

from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)
T = TypeVar('T')
WidgetFactory_t = Union[
    Callable[[QSettings, 'Field'], FieldWidget],
    Type[FieldWidget],
]


class Field(pyqtProperty, Generic[T]):
    valueChanged = pyqtSignal(object)

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
        return widget

    def createWidgetWithLabel(self, instance: QSettings, parent=None) -> Optional[QWidget]:
        if not (widget := self.createWidget(instance)):
            return
        aggr = QWidget(parent)
        layout = QFormLayout(aggr)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addRow(self.displayName + ':', widget)
        return aggr

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
