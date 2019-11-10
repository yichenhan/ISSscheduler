# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'defaultEvent.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DefaultEvent(object):
    def setupUi(self, DefaultEvent):
        DefaultEvent.setObjectName("DefaultEvent")
        DefaultEvent.resize(443, 640)
        DefaultEvent.setMinimumSize(QtCore.QSize(200, 300))
        self.verticalLayoutWidget = QtWidgets.QWidget(DefaultEvent)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 401, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName("mainLayout")
        self.timeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.timeLabel.setObjectName("timeLabel")
        self.mainLayout.addWidget(self.timeLabel)
        self.titleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.titleLabel.setObjectName("titleLabel")
        self.mainLayout.addWidget(self.titleLabel)
        self.summaryLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.summaryLabel.setObjectName("summaryLabel")
        self.mainLayout.addWidget(self.summaryLabel)
        self.descriptionLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.mainLayout.addWidget(self.descriptionLabel)

        self.retranslateUi(DefaultEvent)
        QtCore.QMetaObject.connectSlotsByName(DefaultEvent)

    def retranslateUi(self, DefaultEvent):
        _translate = QtCore.QCoreApplication.translate
        DefaultEvent.setWindowTitle(_translate("DefaultEvent", "Form"))
        self.timeLabel.setText(_translate("DefaultEvent", "Time - Time"))
        self.titleLabel.setText(_translate("DefaultEvent", "Title"))
        self.summaryLabel.setText(_translate("DefaultEvent", "Summary"))
        self.descriptionLabel.setText(_translate("DefaultEvent", "Description"))

