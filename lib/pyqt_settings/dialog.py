import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget, QFormLayout

from pyqt_settings.field.base import Field
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta

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
            self._settings = settings_

            self.mainLayout = QVBoxLayout(self)
            self.subLayout = QFormLayout()
            self.mainLayout.addLayout(self.subLayout)

            self.widgetToField = dict(self._createWidgets())
            self._createButtons()
            self.accepted.connect(self.save)

        def _createWidgets(self):
            for field in self._genSettingFields():
                if widget := field.createWidget(self._settings):
                    self.subLayout.addRow(field.displayName, widget)
                    yield widget, field

        def _genSettingFields(self):
            for field in type(self._settings).__dict__.values():
                if not isinstance(field, Field):
                    continue
                yield field

        def _createButtons(self):
            self.buttonBox = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            self.mainLayout.addWidget(self.buttonBox)

        def save(self):
            changed = False
            for widget, field in self.widgetToField.items():
                newValue = widget.getValue()
                oldValue = field.__get__(self._settings, type(self._settings))

                if newValue == oldValue:
                    continue

                if field.__set__(self._settings, newValue) is False:
                    continue

                changed = True
                logger.debug(f"Set {field.name} = {newValue}")

            if changed:
                self._settings.sync()

    return SettingDialog
