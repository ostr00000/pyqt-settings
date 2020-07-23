from typing import Callable

from pyqt_settings.field.base import Field
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.gui_widget.base import FieldWidget
from pyqt_settings.setting_creator import SettingCreator


class ControlWidgetFactory:
    def __init__(self, supervisor: BoolField, controlled: Field):
        self.supervisor = supervisor
        self.factory = controlled.widgetFactory
        controlled.widgetFactory = None

        self.controlledWidget: FieldWidget
        self.oldSetCreator: Callable[[SettingCreator], None]

    def __call__(self) -> FieldWidget:
        controlledWidget = self.factory()
        oldSetCreator = controlledWidget.setCreator

        def setCreator(creator: SettingCreator):
            oldSetCreator(creator)
            supervisorWidget = creator.getWidgetFromField(self.supervisor)
            supervisorWidget.stateChanged.connect(controlledWidget.setEnabled)
            controlledWidget.setEnabled(supervisorWidget.isChecked())

        controlledWidget.setCreator = setCreator
        return controlledWidget
