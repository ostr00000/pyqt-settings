from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from boltons.cacheutils import cachedproperty

# noinspection PyUnresolvedReferences
import pyqt_settings.ui
from pyqt_settings.dialog import createSettingDialogClass
from pyqt_settings.display_widget_action import DisplayWidgetAction


class SettingDialogAction(DisplayWidgetAction):
    def __init__(self, settings, icon=QIcon(':/icons/settings.svg'),
                 text="&Settings", parent=None):
        super().__init__(icon=icon, text=text, parent=parent)
        self.settings = settings

    def createWidget(self) -> QWidget:
        return self.settingDialogClass(self.settings, self.parent())

    @cachedproperty
    def settingDialogClass(self):
        return createSettingDialogClass(self.settings)
