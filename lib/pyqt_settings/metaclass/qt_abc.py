from abc import ABCMeta

from PyQt5.QtCore import QObject

from pyqt_settings.metaclass.base import BaseMeta


class QtAbcMeta(BaseMeta, ABCMeta, type(QObject)):
    pass
