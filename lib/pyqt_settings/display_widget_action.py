from abc import abstractmethod
from typing import Optional

from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget

from pyqt_settings.metaclass.qt_abc import QtAbcMeta


class DisplayWidgetAction(QAction, metaclass=QtAbcMeta):  # TODO move
    def __init__(self, icon=QIcon(), text='', parent: QWidget = None):
        super().__init__(icon, text, parent)
        self.widget: Optional[QWidget] = None
        self.triggered.connect(self.onTriggered)

    def onTriggered(self):
        if self.widget is None:
            self.widget = self.createWidget()
            self.widget.installEventFilter(self)
            self.widget.show()
        else:
            self.widget.raise_()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Close and obj is self.widget:
            obj.event(event)
            obj.setParent(None)
            obj.deleteLater()
            self.widget = None
            return True
        return False

    @abstractmethod
    def createWidget(self) -> QWidget:
        pass
