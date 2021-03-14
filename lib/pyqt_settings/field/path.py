from pyqt_settings.factory.base import InitArgWidgetFactory
from pyqt_settings.field.string import StrField
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit


class PathField(StrField):
    def __init__(self, key, default=''):
        super().__init__(key, default)
        self.widgetFactory = InitArgWidgetFactory(PathLineEdit)
