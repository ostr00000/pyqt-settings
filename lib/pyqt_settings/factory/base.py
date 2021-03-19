from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import WidgetFactory_t, Field
from pyqt_settings.gui_widget.base import FieldWidget


class ConfigFunc:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self, widget=None):
        if widget is None:
            return self.fun(*self.args, **self.kwargs)
        else:
            self.fun(widget, *self.args, **self.kwargs)


class WidgetFactory:
    def __init__(self, initFunc: WidgetFactory_t, *args, **kwargs):
        """Factory saves initFunc and parameters and
        create widget when this object is called.
        :param initFunc: function that create widget, may be class
        """
        self.initFunc = ConfigFunc(initFunc, *args, **kwargs)
        self.configFunctions: list[ConfigFunc] = []

    def addConfig(self, configFunction, *args, **kwargs):
        """Save additional configuration functions and their argument to
        call when constructing a new object."""
        self.configFunctions.append(ConfigFunc(configFunction, *args, **kwargs))

    def __call__(self, settings: QSettings, field: Field) -> FieldWidget:
        widget = self.initFunc()
        for configFunc in self.configFunctions:
            configFunc(widget)
        return widget
