# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/path_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_PathWidget(object):
    def setupUi(self, PathWidget):
        PathWidget.setObjectName("PathWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(PathWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(PathWidget)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.toolButton = QtWidgets.QToolButton(PathWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)

        self.retranslateUi(PathWidget)
        QtCore.QMetaObject.connectSlotsByName(PathWidget)

    def retranslateUi(self, PathWidget):
        _translate = QtCore.QCoreApplication.translate
        PathWidget.setWindowTitle(_translate("PathWidget", "Path widget"))
        self.toolButton.setText(_translate("PathWidget", "..."))
