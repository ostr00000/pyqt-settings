import logging
from typing import Dict

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QWidget

from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.base import FieldWidget
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
            self._settingName2widget: Dict[str, FieldWidget] = {}

            self.mainLayout = QVBoxLayout(self)
            self.layout = QFormLayout()
            self.mainLayout.addLayout(self.layout)

            self._createButtons()
            self._createWidgets()

        def _createButtons(self):
            self.buttonBox = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
            self.accepted.connect(self.onAccepted)

            self.mainLayout.addWidget(self.buttonBox)

        def _createWidgets(self):
            for settingName, field in type(self.settings).__dict__.items():
                if isinstance(field, Field) and getattr(field, 'widgetClass', False):
                    widget = field.widgetClass(*field.widgetArgs)
                    widget.setValue(getattr(self.settings, settingName))
                    displayName = settingName.lower().replace('_', ' ').capitalize()
                    self.layout.addRow(displayName, widget)
                    self._settingName2widget[settingName] = widget

        def onAccepted(self):
            for settingName, widget in self._settingName2widget.items():
                val = widget.getValue()
                logger.debug(f"Set {settingName} = {val}")
                setattr(self.settings, settingName, val)

            self.settings.sync()

    return SettingDialog
