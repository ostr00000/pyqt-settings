from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from boltons.cacheutils import cachedproperty

from pyqt_settings.dialog import createSettingDialogClass
from pyqt_settings.display_widget_action import DisplayWidgetAction


class SettingDialogAction(DisplayWidgetAction):
    def __init__(self, settings, icon=QIcon(':/icons/settings.svg'),
                 text="&Settings", parent=None):
        super().__init__(icon=icon, text=text, parent=parent)
        self.settings = settings

    def createWidget(self) -> QDialog:
        return self.settingDialogClass(self.settings, self.parent())

    @cachedproperty
    def settingDialogClass(self):
        return createSettingDialogClass(self.settings)
