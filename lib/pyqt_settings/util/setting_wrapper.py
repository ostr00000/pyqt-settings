from dataclasses import dataclass

from PyQt5.QtCore import QSettings


@dataclass
class SettingWrapper:
    setting: QSettings = None

    def value(self, key: str, default=None):
        if self.setting is None:
            return
        return self.setting.value(key, default)

    def setValue(self, key: str, value):
        if self.setting is None:
            return
        return self.setting.setValue(key, value)

    def sync(self):
        if self.setting is None:
            return
        return self.setting.sync()
