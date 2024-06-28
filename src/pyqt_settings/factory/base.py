from PyQt5.QtCore import QSettings

from pyqt_settings.field.base import Field, WidgetFactoryType
from pyqt_settings.gui_widget.base import FieldWidget


class ConfigFunc:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.fun(*self.args, *args, **self.kwargs, **kwargs)

    def configureWidget(self, widget: FieldWidget):
        return self.fun(widget, *self.args, **self.kwargs)


class WidgetFactory[T]:
    def __init__(self, initFunc: WidgetFactoryType[T], *args, **kwargs):
        """Save `initFunc` and other parameters.

        When create object is called a Qt widget is created.

        :param initFunc: function that create widget, may be class.
        """
        self.initFunc = ConfigFunc(initFunc, *args, **kwargs)
        self.configFunctions: list[ConfigFunc] = []

    def addConfig(self, configFunction, *args, **kwargs):
        """Save additional configuration functions and their argument.

        These values will be used when constructing the widget.
        """
        self.configFunctions.append(ConfigFunc(configFunction, *args, **kwargs))

    def __call__(
        self, *, settings: QSettings, field: Field, **factoryKwargs
    ) -> FieldWidget[T]:
        widget = self.initFunc(settings=settings, field=field, **factoryKwargs)
        for configFunc in self.configFunctions:
            configFunc.configureWidget(widget)
        return widget
