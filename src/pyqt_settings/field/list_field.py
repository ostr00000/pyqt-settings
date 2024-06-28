from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Self, overload

from pyqt_settings.factory.base import WidgetFactory
from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.simple import SpaceLineFieldWidget

if TYPE_CHECKING:
    from collections.abc import Callable

    from PyQt5.QtCore import QSettings

logger = logging.getLogger(__name__)


class ListField[S](Field[list[S]]):
    """Field represent python list with values of type castType."""

    def __init__(
        self,
        key: str,
        default: list[S] | None = None,
        castType: Callable[[Any], S] = str,
    ):
        if default is None:
            default = []
        super().__init__(key, default, list)
        self.castType = castType
        self.widgetFactory = WidgetFactory(SpaceLineFieldWidget)

    @overload
    def __get__(self, instance: None, owner: type[QSettings]) -> Self: ...

    @overload
    def __get__(self, instance: QSettings, owner: type[QSettings]) -> list[S]: ...

    def __get__(
        self, instance: QSettings | None, owner: type[QSettings]
    ) -> Self | list[S]:
        if instance is None:
            return self
        try:
            val = instance.value(self.key, self.default, self.typeAsClass)
            return [self.castType(v) for v in val]
        except (TypeError, ValueError):
            logger.exception(f"Cannot convert `{self.key}`")
            return self.default

    def __set__(self, instance: QSettings, value):
        instance.setValue(self.key, value)
