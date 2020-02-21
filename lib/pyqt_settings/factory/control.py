from pyqt_settings.field.base import Field
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.gui_widget.base import FieldWidget
from pyqt_settings.gui_widget.check_box import CheckBoxFieldWidget


class ControlWidgetFactory:
    def __init__(self, supervisor: BoolField, controlled: Field):
        self.supervisor = supervisor
        self.factory = controlled.widgetFactory
        controlled.widgetFactory = None

    def setControlledWidget(self, controlledWidget: FieldWidget):
        self.factory = controlledWidget

    def __call__(self) -> FieldWidget:
        widget = self.factory()
        w: CheckBoxFieldWidget = self.supervisor.widget
        w.stateChanged.connect(widget.setEnabled)
        widget.setEnabled(w.isChecked())
        return widget
