# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mw4/gui/widgets/measure.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeasureDialog(object):
    def setupUi(self, MeasureDialog):
        MeasureDialog.setObjectName("MeasureDialog")
        MeasureDialog.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MeasureDialog.sizePolicy().hasHeightForWidth())
        MeasureDialog.setSizePolicy(sizePolicy)
        MeasureDialog.setMinimumSize(QtCore.QSize(800, 600))
        MeasureDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MeasureDialog.setSizeIncrement(QtCore.QSize(10, 10))
        MeasureDialog.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Arial")
        MeasureDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(MeasureDialog)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(4, 6, 4, 6)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.measureGroup = QtWidgets.QGroupBox(MeasureDialog)
        self.measureGroup.setObjectName("measureGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.measureGroup)
        self.gridLayout.setContentsMargins(4, 6, 4, 4)
        self.gridLayout.setObjectName("gridLayout")
        self.measureSet1 = QtWidgets.QComboBox(self.measureGroup)
        self.measureSet1.setMinimumSize(QtCore.QSize(150, 25))
        self.measureSet1.setObjectName("measureSet1")
        self.gridLayout.addWidget(self.measureSet1, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.measureGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.measureGroup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.measureGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.measureSet2 = QtWidgets.QComboBox(self.measureGroup)
        self.measureSet2.setMinimumSize(QtCore.QSize(150, 25))
        self.measureSet2.setObjectName("measureSet2")
        self.gridLayout.addWidget(self.measureSet2, 1, 1, 1, 1)
        self.measureSet3 = QtWidgets.QComboBox(self.measureGroup)
        self.measureSet3.setMinimumSize(QtCore.QSize(150, 25))
        self.measureSet3.setObjectName("measureSet3")
        self.gridLayout.addWidget(self.measureSet3, 1, 2, 1, 1)
        self.horizontalLayout.addWidget(self.measureGroup)
        self.line_2 = QtWidgets.QFrame(MeasureDialog)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setMidLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.timeGroup = QtWidgets.QGroupBox(MeasureDialog)
        self.timeGroup.setObjectName("timeGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.timeGroup)
        self.gridLayout_2.setContentsMargins(4, 6, 4, 4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.timeSet = QtWidgets.QComboBox(self.timeGroup)
        self.timeSet.setMinimumSize(QtCore.QSize(150, 25))
        self.timeSet.setObjectName("timeSet")
        self.gridLayout_2.addWidget(self.timeSet, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.timeGroup)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(MeasureDialog)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.measure = QtWidgets.QWidget(MeasureDialog)
        self.measure.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measure.sizePolicy().hasHeightForWidth())
        self.measure.setSizePolicy(sizePolicy)
        self.measure.setMinimumSize(QtCore.QSize(0, 0))
        self.measure.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.measure.setSizeIncrement(QtCore.QSize(10, 10))
        self.measure.setBaseSize(QtCore.QSize(10, 10))
        self.measure.setAutoFillBackground(True)
        self.measure.setStyleSheet("")
        self.measure.setObjectName("measure")
        self.verticalLayout.addWidget(self.measure)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(MeasureDialog)
        QtCore.QMetaObject.connectSlotsByName(MeasureDialog)

    def retranslateUi(self, MeasureDialog):
        _translate = QtCore.QCoreApplication.translate
        MeasureDialog.setWindowTitle(_translate("MeasureDialog", "Measurements"))
        self.measureGroup.setTitle(_translate("MeasureDialog", "Measurement sets"))
        self.label_2.setText(_translate("MeasureDialog", "Middle chart"))
        self.label.setText(_translate("MeasureDialog", "Upper chart"))
        self.label_3.setText(_translate("MeasureDialog", "Lower chart"))
        self.timeGroup.setTitle(_translate("MeasureDialog", "Measurement windows"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MeasureDialog = QtWidgets.QWidget()
    ui = Ui_MeasureDialog()
    ui.setupUi(MeasureDialog)
    MeasureDialog.show()
    sys.exit(app.exec_())
