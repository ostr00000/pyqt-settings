from abc import abstractmethod
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QDialog

from pyqt_settings.metaclass.qt_abc import QtAbcMeta


class DisplayWidgetAction(QAction, metaclass=QtAbcMeta):  # TODO move
    def __init__(self, icon=QIcon(), text='', parent: QWidget = None):
        super().__init__(icon, text, parent)
        self.widget: Optional[QWidget] = None
        self.triggered.connect(self.onTriggered)

    def onTriggered(self):
        if self.widget is None:
            self.widget = self.createWidget()
            if isinstance(self.widget, QDialog):
                self.widget.finished.connect(self.onFinished)

            self.widget.show()
        else:
            self.widget.raise_()

    def onFinished(self):
        if self.widget is not None:
            self.widget.setParent(None)
            self.widget.deleteLater()
            self.widget = None

    @abstractmethod
    def createWidget(self) -> QWidget:
        pass
