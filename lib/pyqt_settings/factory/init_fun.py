from typing import Callable

from pyqt_settings.gui_widget.base import FieldWidget


class InitFunc:
    """Container for constructor function (class) and its arguments"""

    def __init__(self, init: Callable[..., FieldWidget], *args, **kwargs):
        self.init = init
        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> FieldWidget:
        return self.init(*self.args, **self.kwargs)
