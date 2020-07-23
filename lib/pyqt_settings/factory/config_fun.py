class ConfigFunc:
    """Container for unbound function and its arguments"""

    def __init__(self, fun, *args):
        self.fun = fun
        self.args = args

    def __call__(self, widget):
        self.fun(widget, *self.args)
