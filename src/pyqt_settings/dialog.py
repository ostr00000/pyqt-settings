import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta

from pyqt_settings.field.base import Field

logger = logging.getLogger(__name__)


class SettingDialogBase(QDialog):

    def __init__(self, settings: QSettings, parent: QWidget | None = None):
        super().__init__(parent)
        self._settings = settings

        self.mainLayout = QVBoxLayout(self)
        self.scrollArea = QScrollArea(self)
        self.mainLayout.addWidget(self.scrollArea)
        self._createButtons()

        self.contentWidget = QWidget(self.scrollArea)
        self.contentLayout = QFormLayout(self.contentWidget)
        self.contentLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.widgetToField = dict(self._createWidgets())
        self.scrollArea.setWidget(self.contentWidget)

        self.accepted.connect(self.save)

    def _createWidgets(self):
        for field in self._genSettingFields():
            if widget := field.createWidget(self._settings):
                self.contentLayout.addRow(field.displayName, widget)
                yield widget, field

    def _genSettingFields(self):
        for field in type(self._settings).__dict__.values():
            if not isinstance(field, Field):
                continue
            yield field

    def _createButtons(self):
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )

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


def createSettingDialogClass(settings: QSettings) -> type[SettingDialogBase]:
    """
    Create setting dialog using provides `settings`.

    :param settings: where save dialog position
    :return: dialog that create representation of field in setting
    """
    saveName = (
        f"{settings.organizationName()}"
        f"_{settings.applicationName()}"
        f"_{settings.objectName()}"
        f"_SettingDialog"
    )

    class SettingDialog(
        SettingDialogBase,
        metaclass=GeometrySaverMeta,
        settings=settings,
        saveName=saveName,
    ):
        pass

    return SettingDialog
