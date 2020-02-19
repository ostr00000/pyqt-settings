from pyqt_settings.field.base import Field
from pyqt_settings.gui_widget.spin_box import SpinBoxFieldWidget


class IntField(Field):
    widgetClass = SpinBoxFieldWidget

    def __init__(self, key, default=0):
        super().__init__(key, default, int)
