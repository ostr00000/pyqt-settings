from pyqt_settings.field.base import Field


class RawField(Field):
    def __get__(self, instance, owner):
        return instance.value(self.key, self.default)
