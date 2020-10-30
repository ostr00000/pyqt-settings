from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QDialogButtonBox

from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta


def main():
    settings = QSettings()
    app = QApplication([])

    class MyMainWindow(QMainWindow, metaclass=GeometrySaverMeta.wrap(QMainWindow),
                       settings=settings):
        pass

    class MyWidget(QDialog, metaclass=GeometrySaverMeta.wrap(QDialog),
                   settings=settings):
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


if __name__ == '__main__':
    main()
