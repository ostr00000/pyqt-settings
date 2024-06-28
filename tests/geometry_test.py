from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QMainWindow,
    QVBoxLayout,
)
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta


def main():
    settings = QSettings()
    app = QApplication([])

    class MyMainWindow(QMainWindow, metaclass=GeometrySaverMeta, settings=settings):
        pass

    class MyWidget(
        QDialog,
        metaclass=GeometrySaverMeta,
        settings=settings,
        saveName='geometry_dialog',
    ):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.verticalLayout = QVBoxLayout(self)
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
            self.verticalLayout.addWidget(self.buttonBox)
            self.buttonBox.clicked.connect(self.accept)

    mmw = MyMainWindow()
    mmw.show()

    mw = MyWidget(mmw)
    mw.show()

    app.exec()


if __name__ == "__main__":
    main()
