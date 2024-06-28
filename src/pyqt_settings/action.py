from functools import cached_property

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from pyqt_utils.qobjects.display_widget_action import DisplayWidgetAction

from pyqt_settings import packageName
from pyqt_settings.dialog import SettingDialogBase, createSettingDialogClass

_settingsIcon = QIcon(f"{packageName}:settings.svg")


class SettingDialogAction(DisplayWidgetAction[SettingDialogBase]):
    def __init__(
        self,
        settings,
        icon=_settingsIcon,
        text="&Settings",
        parent: QWidget | None = None,
    ):
        super().__init__(icon=icon, text=text, parent=parent)
        self.settings = settings

    def parent(self) -> QWidget | None:
        match super().parent():
            case (QWidget() | None) as p:
                return p
            case _:
                raise TypeError

    def createWidget(self, parent: QWidget | None = None) -> SettingDialogBase:
        return self.settingDialogClass(self.settings, parent)

    @cached_property
    def settingDialogClass(self) -> type[SettingDialogBase]:
        return createSettingDialogClass(self.settings)
