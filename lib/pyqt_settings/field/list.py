from __future__ import annotations

import logging
from typing import Type, List, Generic, TypeVar, Union, Callable

from PyQt5.QtCore import QSettings

from pyqt_settings.factory.base import WidgetFactory
from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.simple import SpaceLineFieldWidget

logger = logging.getLogger(__name__)
S = TypeVar('S')


class ListField(Field[List], Generic[S]):
    """Field represent python list with values of type castType."""
    def __init__(self, key, default=None, castType: Callable[[str], S] = str):
        if default is None:
            default = []
        super().__init__(key, default, list)
        self.castType = castType
        self.widgetFactory = WidgetFactory(SpaceLineFieldWidget)

    def __get__(self, instance: QSettings, owner: Type[QSettings]) -> Union[ListField, List[S]]:
        if instance is None:
            return self
        try:
            val = instance.value(self.key, self.default, self.type)
            return [self.castType(v) for v in val]
        except (TypeError, ValueError) as error:
            logger.error(error)
            return self.default

    def __set__(self, instance: QSettings, value):
        instance.setValue(self.key, value)
