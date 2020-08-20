import logging
import re

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QWidget

from pyqt_settings.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_settings.setting_creator import SettingCreator

logger = logging.getLogger(__name__)


def createSettingDialogClass(settings: QSettings = None):
    """
    :param settings: where save dialog position
    :return: dialog that create representation of field in setting
    """
    saveName = '_'.join((
        settings.organizationName(),
        settings.applicationName(),
        settings.objectName(),
        'SettingDialog',
    ))

    class SettingDialog(
        QDialog,
        metaclass=GeometrySaverMeta.wrap(QDialog),
        settings=settings,
        saveName=saveName
    ):

        def __init__(self, settings_: QSettings, parent: QWidget = None):
            super().__init__(parent)
            self.settingsCreator = SettingCreator(settings_)

            self.subLayout = QFormLayout()
            self._createWidgets()

            self.mainLayout = QVBoxLayout(self)
            self.mainLayout.addLayout(self.subLayout)
            self._createButtons()

            self.accepted.connect(self.settingsCreator.save)
            self.finished.connect(self.settingsCreator.clear)

        def _createWidgets(self):
            for settingName, field, fieldWidget in self.settingsCreator:
                displayName = settingName.replace('LL', '[').replace('JJ', ']')
                displayName = re.sub('([A-Z]+)', r'_\1', displayName).replace('__', ' ')
                displayName = displayName.lower().replace('_', ' ').strip().capitalize()
                self.subLayout.addRow(displayName, fieldWidget)

        def _createButtons(self):
            self.buttonBox = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            self.mainLayout.addWidget(self.buttonBox)

    return SettingDialog
