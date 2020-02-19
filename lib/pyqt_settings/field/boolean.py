from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.check_box import CheckBoxFieldWidget


class BoolField(Field):
    widgetClass = CheckBoxFieldWidget

    def __init__(self, key, default=False):
        super().__init__(key, default, bool)
