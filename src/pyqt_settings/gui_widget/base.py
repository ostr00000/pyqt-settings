from abc import ABC, abstractmethod

from PyQt5.QtCore import QSettings
from pyqt_utils.widgets.base_ui_widget import BaseWidget

from pyqt_settings.field.base import Field


class FieldWidgetInit[T]:
    def __init__(
        self,
        *,
        settings: QSettings,
        field: Field[T],
        **factoryKwargs,
    ):
        self.settings = settings
        self.field = field
        super().__init__(**factoryKwargs)


class FieldWidget[T](BaseWidget, ABC):
    """This should be a first class in inheritance chain.

    PyQt stubs are missing `kwargs` argument for `__init__` functions,
    so putting this class in front solve typing problem.
    Example:
    >>> from PyQt5.QtWidgets import QLineEdit
    >>> class SomeWidgetField(
    ...     QLineEdit,
    ...     FieldWidget[str],
    ...     ABC,
    ... ): ...
    """

    @abstractmethod
    def getValue(self) -> T:
        """Return current settings value."""
        raise NotImplementedError

    @abstractmethod
    def setValue(self, value: T):
        """Set a new value to settings."""
        raise NotImplementedError
