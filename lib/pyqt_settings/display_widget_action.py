from abc import abstractmethod
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QDialog, QVBoxLayout

from pyqt_settings.metaclass.qt_abc import QtAbcMeta


class DisplayWidgetAction(QAction, metaclass=QtAbcMeta):  # TODO move
    def __init__(self, icon=QIcon(), text='', parent: QWidget = None):
        super().__init__(icon, text, parent)
        self.dialog = QDialog()
        self.dialog.setLayout(QVBoxLayout())
        self.dialog.finished.connect(self.onFinished)

        self.widget: Optional[QWidget] = None
        self.triggered.connect(self.onTriggered)

    def onTriggered(self):
        if self.widget is None:
            self.widget = self.createWidget()
            self.dialog.layout().addWidget(self.widget)
            self.dialog.show()
        else:
            self.dialog.raise_()

    def onFinished(self):
        self.dialog.layout().removeWidget(self.widget)
        self.widget = None

    @abstractmethod
    def createWidget(self) -> QWidget:
        pass
