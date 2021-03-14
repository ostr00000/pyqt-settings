class ConfigFunc:
    """Container for unbound function and its arguments"""

    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self, widget):
        self.fun(widget, *self.args, **self.kwargs)
