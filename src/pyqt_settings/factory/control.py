from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field
from pyqt_settings.field.simple import BoolField
from pyqt_settings.gui_widget.base import FieldWidget


class ControlWidgetFactory:
    def __init__(self, supervisor: BoolField, controlled: Field):
        self.controlled = controlled
        self.controlledFactory = controlled.widgetFactory
        self.controlledWidget = None
        controlled.widgetFactory = None

        self.supervisor = supervisor
        self.supervisorFactory = supervisor.widgetFactory
        self.supervisorWidget = None
        supervisor.widgetFactory = self.supervisorFactoryWrapper

    def supervisorFactoryWrapper(self, settings: QSettings, field: Field) -> FieldWidget:
        self.supervisorWidget = sw = self.supervisorFactory(settings, field)
        self._connect()
        return sw

    def _connect(self):
        if self.supervisorWidget is None:
            return
        if self.controlledWidget is None:
            return

        try:
            self.controlledWidget.setEnabled(self.supervisorWidget.isChecked())
        except AttributeError:
            pass
        try:
            self.supervisorWidget.stateChanged.connect(self.controlledWidget.setEnabled)
        except AttributeError:
            pass

        self.controlledWidget = None
        self.supervisorWidget = None

    def __call__(self, settings: QSettings, field: Field) -> FieldWidget:
        self.controlledWidget = cw = self.controlledFactory(settings, field)
        self._connect()
        return cw
