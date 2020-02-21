import logging
from typing import Dict

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QWidget

from pyqt_settings.field.base import Field
from pyqt_settings.util.geometry_saver_meta import GeometrySaverMeta

logger = logging.getLogger(__name__)


def createSettingDialogClass(settings: QSettings = None, saveName: str = None):
    """
    :param settings: where save dialog position
    :param saveName: dialog key in setting in section 'geometry'
    :return: dialog that create representation of field in setting
    """

    class SettingDialog(QDialog,
                        metaclass=GeometrySaverMeta.wrap(QDialog),
                        settings=settings, saveName=saveName):

        def __init__(self, settings_: QSettings, parent: QWidget = None):
            super().__init__(parent)
            self.settings = settings_
            self._settingName2field: Dict[str, Field] = {}

            self.mainLayout = QVBoxLayout(self)
            self.layout = QFormLayout()
            self.mainLayout.addLayout(self.layout)

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

                    displayName = settingName.lower().replace('_', ' ').capitalize()
                    self.layout.addRow(displayName, widget)
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
