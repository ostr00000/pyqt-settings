from pyqt_settings.field.base import Field
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.gui_widget.base import FieldWidget


class ControlWidgetFactory:
    def __init__(self, supervisor: BoolField, controlled: Field):
        self.supervisor = supervisor
        self.controlled = controlled
        self.factory = controlled.widgetFactory
        controlled.widgetFactory = None

    def __call__(self) -> FieldWidget:
        controlledWidget = self.factory()
        supervisorWidget = self.supervisor.getWidget(None)

        try:
            controlledWidget.setEnabled(supervisorWidget.isChecked())
        except AttributeError:
            pass
        try:
            supervisorWidget.stateChanged.connect(controlledWidget.setEnabled)
        except AttributeError:
            pass

        return controlledWidget
