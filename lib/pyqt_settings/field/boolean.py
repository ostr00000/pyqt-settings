from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.check_box import CheckBoxFieldWidget
from pyqt_settings.factory.base import WidgetFactory


class BoolField(Field):

    def __init__(self, key, default=False):
        super().__init__(key, default, bool)
        self.widgetFactory = WidgetFactory(CheckBoxFieldWidget)
