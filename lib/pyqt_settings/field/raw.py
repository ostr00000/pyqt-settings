from pyqt_settings.field.base import Field


class RawField(Field):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.value(self.key, self.default)
