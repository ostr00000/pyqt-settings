from typing import Callable, Union

from pyqt_settings.factory.config_fun import ConfigFunc
from pyqt_settings.factory.init_fun import InitFunc
from pyqt_settings.gui_widget.base import FieldWidget


class WidgetFactory:
    def __init__(self, initFunc: Union[InitFunc, Callable[[], FieldWidget]] = None,
                 *configFuncs: ConfigFunc):
        """Factory create widget using InitFunc and ConfigFunc
        :param initFunc: function create widget, may be class
        :param configFuncs: functions that set desired properties to widget
        """
        self.initFunc = initFunc
        self.configFuncs = list(configFuncs)

    def __call__(self) -> FieldWidget:
        widget = self.initFunc()
        for configFunc in self.configFuncs:
            configFunc(widget)
        return widget


class InitArgWidgetFactory(WidgetFactory):
    def __init__(self, class_, *args):
        """Convenience factory.
        :param class_: widget class
        :param args: argument for widget __init__
        """
        super().__init__(InitFunc(class_, *args))
