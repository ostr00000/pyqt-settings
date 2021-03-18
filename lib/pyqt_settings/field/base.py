from __future__ import annotations

import logging
import re
from functools import cached_property
from typing import TypeVar, Generic, Type, Union, Optional, Callable

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QFormLayout

from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)
T = TypeVar('T')


class Field(Generic[T]):

    def __init__(self, key: str, default: T = None, type_: Type[T] = None):
        self.key = key
        if type_ is not None:
            default = type_(default)
        self.default = default
        self.type = type_
        self.widgetFactory: Optional[Callable[[], FieldWidget]] = None

        self.name = None
        self.owner = None

    def __set_name__(self, owner: QSettings, name: str):
        self.owner = owner
        self.name = name

    def getWidget(self, instance: Optional[QSettings], init=True) -> Optional[FieldWidget]:
        if self.widgetFactory is None:
            return None
        else:
            try:
                widget = self.widgetFactory()
            except TypeError:  # temporary solution
                widget = self.widgetFactory(instance)  # noqa

        if init and instance is not None:
            widget.setValue(self.__get__(instance, self.owner))
        return widget

    def getWidgetWithLabel(self, instance: QSettings, parent=None) -> Optional[QWidget]:
        if not (widget := self.getWidget(instance)):
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
