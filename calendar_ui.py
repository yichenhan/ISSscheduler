# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calendar.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CalendarWindow(object):
    def setupUi(self, CalendarWindow):
        CalendarWindow.setObjectName("CalendarWindow")
        CalendarWindow.resize(480, 640)
        self.centralwidget = QtWidgets.QWidget(CalendarWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 30, 392, 236))
        self.calendarWidget.setObjectName("calendarWidget")
        CalendarWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CalendarWindow)
        QtCore.QMetaObject.connectSlotsByName(CalendarWindow)

    def retranslateUi(self, CalendarWindow):
        _translate = QtCore.QCoreApplication.translate
        CalendarWindow.setWindowTitle(_translate("CalendarWindow", "MainWindow"))

