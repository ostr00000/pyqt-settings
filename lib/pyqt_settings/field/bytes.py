from pyqt_settings.field.base import Field


class BytesField(Field):
    def __init__(self, key, default=b''):
        super().__init__(key, default, bytes)
