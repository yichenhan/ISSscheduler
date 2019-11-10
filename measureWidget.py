# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'measureWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_measureWidget(object):
    def setupUi(self, measureWidget):
        measureWidget.setObjectName("measureWidget")
        measureWidget.resize(307, 640)
        self.gridLayoutWidget = QtWidgets.QWidget(measureWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(24, 24, 261, 581))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.mainLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.mainLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mainLayout_2.setObjectName("mainLayout_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.textEdit_2.setMaximumSize(QtCore.QSize(150, 50))
        self.textEdit_2.setObjectName("textEdit_2")
        self.mainLayout_2.addWidget(self.textEdit_2, 3, 1, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QtCore.QSize(150, 50))
        self.textEdit.setObjectName("textEdit")
        self.mainLayout_2.addWidget(self.textEdit, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.mainLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.mainLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.summaryLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.summaryLabel.setObjectName("summaryLabel")
        self.mainLayout_2.addWidget(self.summaryLabel, 4, 0, 1, 2)
        self.descriptionLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.mainLayout_2.addWidget(self.descriptionLabel, 5, 0, 1, 2)
        self.timeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.timeLabel.setObjectName("timeLabel")
        self.mainLayout_2.addWidget(self.timeLabel, 1, 0, 1, 2)
        self.titleLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.titleLabel.setObjectName("titleLabel")
        self.mainLayout_2.addWidget(self.titleLabel, 0, 0, 1, 2)

        self.retranslateUi(measureWidget)
        QtCore.QMetaObject.connectSlotsByName(measureWidget)

    def retranslateUi(self, measureWidget):
        _translate = QtCore.QCoreApplication.translate
        measureWidget.setWindowTitle(_translate("measureWidget", "Form"))
        self.label.setText(_translate("measureWidget", "Measurement 1"))
        self.label_2.setText(_translate("measureWidget", "Measurement 2"))
        self.summaryLabel.setText(_translate("measureWidget", "Summary"))
        self.descriptionLabel.setText(_translate("measureWidget", "Description"))
        self.timeLabel.setText(_translate("measureWidget", "Time - Time"))
        self.titleLabel.setText(_translate("measureWidget", "Title"))

