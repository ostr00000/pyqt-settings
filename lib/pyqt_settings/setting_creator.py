import logging
from typing import Dict

from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.base import FieldWidget

logger = logging.getLogger(__name__)


class SettingCreator:
    def __init__(self, settings: QSettings):
        self.settings = settings
        self._settingName2Field: Dict[str, Field] = {}
        self._field2Widget: Dict[Field, FieldWidget] = {}

        self._createWidgets()
        self._setCreatorForWidgets()

    def _createWidgets(self):
        for settingName, field in type(self.settings).__dict__.items():
            if isinstance(field, Field) and field.widgetFactory is not None:
                widget = field.widgetFactory()
                val = getattr(self.settings, settingName)
                widget.setValue(val)

                self._settingName2Field[settingName] = field
                self._field2Widget[field] = widget

    def _setCreatorForWidgets(self):
        for widget in self._field2Widget.values():
            widget.setCreator(self)

    def getWidgetFromField(self, field: Field) -> FieldWidget:
        return self._field2Widget[field]

    def __iter__(self):
        return ((settingName, field, self._field2Widget[field])
                for settingName, field in self._settingName2Field.items())

    def save(self):
        for settingName, field in self._settingName2Field.items():
            newVal = self._field2Widget[field].getValue()
            oldVal = getattr(self.settings, settingName)
            if newVal == oldVal:
                continue

            ok = field.__set__(self.settings, newVal)
            if ok is False:
                continue

            logger.debug(f"Set {settingName} = {newVal}")

        self.settings.sync()

    def clear(self):
        self._settingName2Field.clear()
        self._field2Widget.clear()
