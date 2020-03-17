import logging
import re
from typing import Dict

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QWidget

from pyqt_settings.field.base import Field
from pyqt_settings.metaclass.geometry_saver import GeometrySaverMeta

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
            self.settings = settings_
            self._settingName2field: Dict[str, Field] = {}

            self.mainLayout = QVBoxLayout(self)
            self.subLayout = QFormLayout()
            self.mainLayout.addLayout(self.subLayout)

            self._createButtons()
            self._createWidgets()
            self.finished.connect(self.onFinished)

        def _createButtons(self):
            self.buttonBox = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
            self.accepted.connect(self.onAccepted)

            self.mainLayout.addWidget(self.buttonBox)

        def _createWidgets(self):
            for settingName, field in type(self.settings).__dict__.items():
                if isinstance(field, Field) and field.widgetFactory is not None:
                    widget = field.widgetFactory()
                    val = getattr(self.settings, settingName)
                    widget.setValue(val)
                    field.widget = widget

                    displayName = re.sub('([A-Z]+)', r'_\1', settingName).replace('__', ' ')
                    displayName = displayName.lower().replace('_', ' ').strip().capitalize()
                    self.subLayout.addRow(displayName, widget)
                    self._settingName2field[settingName] = field

        def onAccepted(self):
            for settingName, field in self._settingName2field.items():
                val = field.widget.getValue()
                ok = field.__set__(self.settings, val)
                if ok is False:
                    continue
                logger.debug(f"Set {settingName} = {val}")

            self.settings.sync()

        def onFinished(self):
            for settingName, field in self._settingName2field.items():
                field.widget = None

            self._settingName2field.clear()

    return SettingDialog
