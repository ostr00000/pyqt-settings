from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QCheckBox

from pyqt_settings.field.base import Field
from pyqt_settings.field.simple import BoolField
from pyqt_settings.gui_widget.base import FieldWidget


class ControlWidgetFactory[T]:
    def __init__(self, supervisor: BoolField, controlled: Field[T]):
        if (cwf := controlled.widgetFactory) is None:
            raise TypeError

        self.controlled = controlled
        self.controlledFactory = cwf
        self.controlledWidget: FieldWidget[T] | None = None
        controlled.widgetFactory = None

        if (swf := supervisor.widgetFactory) is None:
            raise TypeError

        self.supervisor = supervisor
        self.supervisorFactory = swf
        self.supervisorWidget: FieldWidget[bool] | None = None
        supervisor.widgetFactory = self.supervisorFactoryWrapper

    def supervisorFactoryWrapper(
        self, *, settings: QSettings, field: Field[bool], **factoryKwargs
    ) -> FieldWidget[bool]:
        sw = self.supervisorFactory(settings=settings, field=field, **factoryKwargs)
        self.supervisorWidget = sw
        self._connect()
        return sw

    def _connect(self):
        if self.supervisorWidget is None:
            return
        if self.controlledWidget is None:
            return

        if isinstance(self.supervisorWidget, QCheckBox):
            self.controlledWidget.setEnabled(self.supervisorWidget.isChecked())
            self.supervisorWidget.stateChanged.connect(self.controlledWidget.setEnabled)

        self.controlledWidget = None
        self.supervisorWidget = None

    def __call__(
        self, *, settings: QSettings, field: Field[T], **factoryKwargs
    ) -> FieldWidget[T]:
        cw = self.controlledFactory(settings=settings, field=field, **factoryKwargs)
        self.controlledWidget = cw
        self._connect()
        return cw
