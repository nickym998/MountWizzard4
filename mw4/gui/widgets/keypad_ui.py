# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mw4/gui/widgets/keypad.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeypadDialog(object):
    def setupUi(self, KeypadDialog):
        KeypadDialog.setObjectName("KeypadDialog")
        KeypadDialog.resize(240, 460)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeypadDialog.sizePolicy().hasHeightForWidth())
        KeypadDialog.setSizePolicy(sizePolicy)
        KeypadDialog.setMinimumSize(QtCore.QSize(240, 460))
        KeypadDialog.setMaximumSize(QtCore.QSize(310, 600))
        KeypadDialog.setSizeIncrement(QtCore.QSize(10, 10))
        KeypadDialog.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Arial")
        KeypadDialog.setFont(font)
        self.keypad = QtWidgets.QGridLayout(KeypadDialog)
        self.keypad.setContentsMargins(10, 10, 10, 10)
        self.keypad.setObjectName("keypad")

        self.retranslateUi(KeypadDialog)
        QtCore.QMetaObject.connectSlotsByName(KeypadDialog)

    def retranslateUi(self, KeypadDialog):
        _translate = QtCore.QCoreApplication.translate
        KeypadDialog.setWindowTitle(_translate("KeypadDialog", "Virtual Keypad"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KeypadDialog = QtWidgets.QWidget()
    ui = Ui_KeypadDialog()
    ui.setupUi(KeypadDialog)
    KeypadDialog.show()
    sys.exit(app.exec_())