import sys
from functools import partial
#from googletrans import Translator
#from goslate import Goslate
from translator import trans

from scheduler import Scheduler, TimeTape, Column, Event, SchedulerFolder

from layout import Ui_MainWindow
from defaultEvent import Ui_DefaultEvent

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, \
                            QGraphicsScene, QLabel, QPushButton, QDockWidget
from PyQt5.QtGui import QPen, QBrush

from load_css import MAIN_BUTTONS_CSS, EVENT_LABEL_CSS, CALENDAR_CSS, TIME_TAPE_CSS, MAIN_WINDOW_CSS

from measureWidget import Ui_measureWidget

from sampleSchedule import sampleSchedule

languages = ['en','ru','de','ja','fr','it']


WIDTH_TL = 40 # Timeline width in pixels
Y_SIDE = 120 # Vertical height in pixels of one hour on the timeline

MAX_EVENT_FONT_PT = 14
MIN_EVENT_FONT_PT = 8
DEFAULT_EVENT_FONT = "Times"
FONT_STEP = 2

PEN_WIDTH = 2

W_BUFFER = 4
H_BUFFER = 2
X_BUFFER = 3
Y_BUFFER = 1
STACKED_BUFFER = 1

TT_X_BUFFER = 2
TT_Y_BUFFER = 2

EVENT_POPUP_FLOAT_MAX_Y = 300

GRID_COLOR = Qt.gray

COLUMN_BUTTON_X_BUFFER = 3

RESTORE = {}
for l in languages:
    RESTORE[l] = trans('Restore', l)

MONTH = [-1]
for i in range(1,13):
    MONTH.append({})
    for l in languages:
        MONTH[i][l] = trans(QDate.longMonthName(i),l)

def timeStrToFloat(string):
    hour = float(string.partition(':')[0])
    minute = float(string.partition(':')[2])
    
    return hour + minute / 60

class RectEvent(QGraphicsRectItem):
    
    def setInfo(self, window, eventInfo):
        self.window = window
        self.eventInfo = eventInfo

    def mousePressEvent(self, event):
        window.eventClicked(self.eventInfo)

    def hoverMoveEvent(self, event):
        print('hover')
        pass

class DefaultEvent(QDockWidget, Ui_DefaultEvent):
    def __init__(self, window, parent=None):
        QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.window = window
        self.setMaximumHeight(EVENT_POPUP_FLOAT_MAX_Y)
        self.dockLocationChanged.connect(self.locationChanged)
        self.topLevelChanged.connect(self.locationChanged)
    
    def locationChanged(self):
        if self.isFloating():
            window.draw(w = window.scheduleView.width() + self.width())
        else:
            window.draw()

class MeasureWidget(QDockWidget, Ui_measureWidget):
    def __init__(self, window, parent=None):
        QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.window = window
        self.setMaximumHeight(EVENT_POPUP_FLOAT_MAX_Y)
        self.dockLocationChanged.connect(self.locationChanged)
        self.topLevelChanged.connect(self.locationChanged)
    
    def locationChanged(self):
        if self.isFloating():
            window.draw(w = window.scheduleView.width() + self.width())
        else:
            window.draw()       
            
class SchedulerGUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setStyleSheet(MAIN_WINDOW_CSS)
        self.setupUi(self)
        
        self.scheduleFolder = sampleSchedule()
        self.schedule = self.scheduleFolder.schedulers[self.calendarWidget.selectedDate()]
        
        self.schedule.events[62].customGUI = MeasureWidget
        
        self.activatedColumns = {}
        
        for key in self.scheduleFolder.columns:
            self.activatedColumns[key] = True
        
        self.lang = 'en'
        
        self.restore_buttons = {}
        self.restoreAllButton.clicked.connect(self.restoreAllColumns)
        
        self.translateDict = {}
        for widget in self.centralwidget.findChildren((QPushButton)):
            langDict = {}
            
            for l in languages:
                langDict[l] = trans(widget.text(), l)
            key = widget
            
            self.translateDict[key] = langDict
        
        self.translateWidgets()
        
        self.language0Button.clicked.connect(partial(self.changeLang,'en'))
        self.language1Button.clicked.connect(partial(self.changeLang,'ru'))
        self.language2Button.clicked.connect(partial(self.changeLang,'de'))
        self.language3Button.clicked.connect(partial(self.changeLang,'ja'))
        self.language4Button.clicked.connect(partial(self.changeLang,'fr'))
        self.language5Button.clicked.connect(partial(self.changeLang,'it'))
        
        self.language0Button.setIcon(QtGui.QIcon('flags/United-States.png'))
        self.language1Button.setIcon(QtGui.QIcon('flags/Russia.png'))
        self.language2Button.setIcon(QtGui.QIcon('flags/Germany.png'))
        self.language3Button.setIcon(QtGui.QIcon('flags/Japan.png'))
        self.language4Button.setIcon(QtGui.QIcon('flags/France.png'))
        self.language5Button.setIcon(QtGui.QIcon('flags/Italy.png'))
        
        self.drawAlarm = QTimer()
        self.drawAlarm.timeout.connect(self.drawAlarmFunc)
        self.drawAlarm.start(0.3)
        
        self.calendarWidget.setNavigationBarVisible(False)
        self.calendarWidget.setStyleSheet(CALENDAR_CSS)
        
        self.calendarWidget.clicked.connect(self.updateDisplayedDate)
        self.calendarWidget.currentPageChanged.connect(self.updateNavBarDate)
        self.calendarWidget.selectionChanged.connect(self.updateDisplayedDate)
        self.updateDisplayedDate()
        self.updateNavBarDate()
        
        self.nextMonthButton.clicked.connect(self.calendarWidget.showNextMonth)
        self.prevMonthButton.clicked.connect(self.calendarWidget.showPreviousMonth)
        
        self.nextDayButton.clicked.connect(self.selectNextDate)
        self.prevDayButton.clicked.connect(self.selectPrevDate)
        self.todayButton.clicked.connect(self.selectToday)
        
        navBarWidgets = [self.prevMonthButton,
                              self.displayedCalendarLabel,self.nextMonthButton]
        
        for widget in self.centralwidget.findChildren(QPushButton):
            #if widget not in navBarWidgets:
            widget.setStyleSheet(MAIN_BUTTONS_CSS)
        
        weekendFormat = QTextCharFormat()
        weekendFormat.setForeground(QBrush(Qt.black, Qt.SolidPattern));
        self.calendarWidget.setWeekdayTextFormat(Qt.Saturday, weekendFormat);
        self.calendarWidget.setWeekdayTextFormat(Qt.Sunday, weekendFormat);
        
        self.customGUIs = {}
        
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_A:
            self.selectPrevDate()
        elif event.key() == QtCore.Qt.Key_D:
            self.selectNextDate()
    
    def closeEvent(self, event):
        quit()
    
    def resizeEvent(self, event):
        self.draw()
    
    def eventClicked(self,event):
        '''
        try:
            self.dockWidget.deleteLater()
        except AttributeError:
            pass
        '''
        if event.customGUI != None:
            self.dockWidget = event.customGUI(self)
        else:
            self.dockWidget = DefaultEvent(self)
        
        self.dockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.NoDockWidgetArea)
        self.dockWidget.setMinimumWidth(450)
        
        self.addDockWidget(Qt.RightDockWidgetArea,self.dockWidget)
        
        self.dockWidgetEvent = event
        self.updateEventPopupText()
    
    def updateEventPopupText(self):
        try:
            timeText = self.dockWidgetEvent.t0 + ' - ' + self.dockWidgetEvent.t1 + ' (GMT)'
            self.dockWidget.timeLabel.setText(timeText)
            self.dockWidget.titleLabel.setText(self.dockWidgetEvent.title[self.lang])
            self.dockWidget.summaryLabel.setText(self.dockWidgetEvent.summary[self.lang])
            self.dockWidget.descriptionLabel.setText(self.dockWidgetEvent.description[self.lang])
            self.dockWidget.setWindowTitle(self.dockWidgetEvent.title[self.lang])
        except AttributeError:
            pass
            
    def selectNextDate(self):
        date = self.calendarWidget.selectedDate()
        self.calendarWidget.setSelectedDate(date.addDays(1))
    
    def selectPrevDate(self):
        date = self.calendarWidget.selectedDate()
        self.calendarWidget.setSelectedDate(date.addDays(-1))
    
    def selectToday(self):
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.calendarWidget.showToday()
    
    def updateNavBarDate(self):
        month = MONTH[self.calendarWidget.monthShown()][self.lang]
        year = self.calendarWidget.yearShown()
        self.displayedCalendarLabel.setText(month + " " + str(year))
    
    def updateDisplayedDate(self):
        self.dateLabel.setText(self.dateToStr(self.calendarWidget.selectedDate()))
        
        try:
            self.schedule = self.scheduleFolder.schedulers[
                    self.calendarWidget.selectedDate()]
        except KeyError:
            self.schedule = Scheduler([])
        
        self.draw()
    
    def dateToStr(self,date):
        month = MONTH[date.month()][self.lang]
        year = date.year()
        day = date.day()
        
        return month + " " + str(day) + " " + str(year)
    
    def drawAlarmFunc(self):
        self.drawAlarm.stop()
        self.draw()
    
    def draw(self, w =-1):
        self.scheduleScene = QGraphicsScene() 
        self.activatedScene = QGraphicsScene()
        
        if w == -1:
            self.w = self.scheduleView.width()
        else:
            self.w = w
        self.h = Y_SIDE * 24
        self.h_a = self.activatedView.height()
        
        self.gridPen = QPen(GRID_COLOR)
        
        for i in range(0,24):
            self.scheduleScene.addLine(0, i * Y_SIDE, self.w, i * Y_SIDE)
        
        self.drawTimeTapes()
        
        cols = self.getActivatedColumns()
        
        x_offset = WIDTH_TL * len(self.scheduleFolder.timeTapes)
        

        if (len(cols) > 0):
            col_width = (self.w - x_offset) / len(cols)
            col_positions = self.drawColumns(cols, x_offset, col_width)
            
            for i in range(0,len(self.schedule.events)):
                try:
                    pos = col_positions[self.schedule.events[i].column_abr]
                
                    self.drawEvent(self.schedule.events[i],col_width,pos)
                except KeyError:
                    pass
        
        
        t_now = QTime.currentTime().hour() + QTime.currentTime().minute() / 60
        self.gridPen = QPen(Qt.green)
        self.gridPen.setWidth(2)
        self.scheduleScene.addLine(0, t_now * (self.h/24), self.w, t_now * (self.h/24),self.gridPen)
        t_fast_return = t_now + 40 / 60
        self.gridPen = QPen(Qt.red)
        self.gridPen.setWidth(2)
        self.scheduleScene.addLine(0, t_fast_return * (self.h/24), self.w, t_fast_return * (self.h/24),self.gridPen)
        
        self.scheduleView.setScene(self.scheduleScene)
        self.activatedView.setScene(self.activatedScene)
        
    
    def drawTimeTapes(self):
        for i in range(0,len(self.scheduleFolder.timeTapes)):
            self.scheduleScene.addLine(WIDTH_TL * i, 0, WIDTH_TL * i, self.h)
            
            self.activatedScene.addLine(WIDTH_TL * i, 0, WIDTH_TL * i, self.h_a)
            
            l = QLabel(self.scheduleFolder.timeTapes[i].name)
            l.move(WIDTH_TL * i + TT_X_BUFFER, TT_Y_BUFFER)
            l.setStyleSheet(TIME_TAPE_CSS)
            self.activatedScene.addWidget(l)
            
            for j in range(0,24):
                l = QLabel(self.scheduleFolder.timeTapes[i].labels[j])
                l.move(WIDTH_TL * i + TT_X_BUFFER, Y_SIDE * j + TT_Y_BUFFER)
                l.setStyleSheet(TIME_TAPE_CSS)
                self.scheduleScene.addWidget(l)
    
    def drawColumns(self, cols, x_offset, col_width):
        
        col_positions = {}
        
        self.deactivateButtons = []
        for i in range(0,len(cols)):
            self.scheduleScene.addLine(x_offset + col_width * i, 0, 
                                       x_offset + col_width * i, self.h)
            '''
            self.activatedScene.addLine(x_offset + col_width * i, 0, 
                                        x_offset + col_width * i, self.h_a)
            '''
            
            b = QPushButton(cols[i].name['en'])
            b.move(x_offset + col_width * i + COLUMN_BUTTON_X_BUFFER + 1,0)
            b.clicked.connect(
                    partial(self.deactivateColumn,cols[i].abr))
            b.setSizePolicy(QSizePolicy.Ignored, 
                            QSizePolicy.Ignored)
            b.setStyleSheet(MAIN_BUTTONS_CSS)
            b.resize(col_width - COLUMN_BUTTON_X_BUFFER * 2, self.h_a - 2)
            
            b = self.activatedScene.addWidget(b)
            
            col_positions[cols[i].abr] = x_offset + col_width * i
        
        return col_positions
                
    def drawEvent(self,event,col_width,x_loc):
        
        t0_f = timeStrToFloat(event.t0)
        t1_f = timeStrToFloat(event.t1)
        
        length = (t1_f - t0_f) * (self.h / 24)
        
        space = QtCore.QSizeF(col_width - PEN_WIDTH, length - PEN_WIDTH)
        r = QtCore.QRectF(QtCore.QPointF(x_loc + 1, t0_f * (self.h/24) + 1), space)
        
        pen = QPen(QtCore.Qt.black)
        pen.setWidth(PEN_WIDTH)
        brush = QBrush(event.color)
        
        ### Checks maximum font size if level
        font_size = MAX_EVENT_FONT_PT
        
        l_title = QLabel(event.title[self.lang] + "  ")
        l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
    
        l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
        l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
        
        title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + \
            l_time.fontMetrics().boundingRect(l_time.text()).width() + W_BUFFER
        title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + H_BUFFER
        
        while (title_height > length or title_width > col_width) and font_size > MIN_EVENT_FONT_PT:
            font_size -= FONT_STEP
            
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
            
            title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + \
                        l_time.fontMetrics().boundingRect(l_time.text()).width() + W_BUFFER
            title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + H_BUFFER
        
        font_size_level = font_size
        over_height_level = title_height - length
        over_width_level = title_width - col_width
        
        ### Checks maximum font size if stacked
        font_size = MAX_EVENT_FONT_PT
        
        l_title = QLabel(event.title[self.lang])
        l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
        
        l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
        l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
        
        title_width = max(l_title.fontMetrics().boundingRect(l_title.text()).width(),
                          l_time.fontMetrics().boundingRect(l_time.text()).width()) + W_BUFFER
        title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + \
            l_time.fontMetrics().boundingRect(l_time.text()).height() + H_BUFFER
        
        while (title_height > length or title_width > col_width) and font_size > MIN_EVENT_FONT_PT:
            font_size -= FONT_STEP
            
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
            
            title_width = max(l_title.fontMetrics().boundingRect(l_title.text()).width(),
                          l_time.fontMetrics().boundingRect(l_time.text()).width()) + W_BUFFER
            title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + \
                    l_time.fontMetrics().boundingRect(l_time.text()).height() + H_BUFFER
        
        font_size_stacked = font_size
        over_height_stacked = title_height - length
        over_width_stacked = title_width - col_width
        
        ### Checks if it can draw the event without the time label if it is too big
        if ((over_width_level > 0 or over_height_level > 0) and \
        (over_width_stacked > 0 or over_height_stacked > 0)):
            font_size = MAX_EVENT_FONT_PT
        
            l_title = QLabel(event.title[self.lang])
        
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
            
            title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + W_BUFFER
            title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + H_BUFFER
            
            while (title_height > length or title_width > col_width) and font_size > MIN_EVENT_FONT_PT:
                font_size -= FONT_STEP
                
                l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
                
                title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + W_BUFFER
                title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + H_BUFFER
            
            font_size_level = font_size
            over_height_level = title_height - length
            over_width_level = title_width - col_width
            
            if (over_height_level > 0 or over_width_level > 0):
                l_title = QLabel('')
                l_time = QLabel('')
            else:
                l_title = QLabel(event.title[self.lang] + " ")            
                l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_level, QtGui.QFont.Bold))
                l_title.move(x_loc + X_BUFFER, t0_f * (self.h/24) + Y_BUFFER)
                l_time = QLabel('')
            
            r = RectEvent(r)
            r.setInfo(self, event)
            r.setPen(pen)
            r.setBrush(brush)
            self.scheduleScene.addItem(r)
            
            l_title.setStyleSheet(EVENT_LABEL_CSS)
            l_time.setStyleSheet(EVENT_LABEL_CSS)
            
            self.scheduleScene.addWidget(l_title)
            self.scheduleScene.addWidget(l_time)
            
            return
        
        ### Sets font and arrangement to the better layout
        if font_size_level > font_size_stacked:
            level = True
        elif font_size_level < font_size_stacked:
            level = False
        else:
            if over_width_level <= 0 and over_height_level <= 0:
                level = True
            elif over_width_level > col_width:
                level = False
            elif over_height_stacked > 0:
                level = True
            else:
                level = False
        
        if level:
            l_title = QLabel(event.title[self.lang] + "  ")
            l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
            
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_level, QtGui.QFont.Normal))
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_level, QtGui.QFont.Bold))
            
            l_title.move(x_loc + X_BUFFER, t0_f * (self.h/24) + Y_BUFFER)
            l_time.move(x_loc + X_BUFFER + \
                        l_title.fontMetrics().boundingRect(l_title.text()).width(), 
                        t0_f * (self.h/24) + Y_BUFFER)
        else:
            l_title = QLabel(event.title[self.lang])
            l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
            
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_stacked, QtGui.QFont.Normal))
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_stacked, QtGui.QFont.Bold))
            
            l_title.move(x_loc + X_BUFFER, t0_f * (self.h/24) + Y_BUFFER)
            l_time.move(x_loc + X_BUFFER, t0_f * (self.h/24) + Y_BUFFER + STACKED_BUFFER + \
                        l_title.fontMetrics().boundingRect(l_title.text()).height())
        
        r = RectEvent(r)
        r.setInfo(self, event)
        r.setPen(pen)
        r.setBrush(brush)
        self.scheduleScene.addItem(r)
        
        l_title.setStyleSheet(EVENT_LABEL_CSS)
        l_time.setStyleSheet(EVENT_LABEL_CSS)
        
        self.scheduleScene.addWidget(l_title)
        self.scheduleScene.addWidget(l_time)
        
    def getActivatedColumns(self):
        cols = []
        
        for key in self.scheduleFolder.columns:
            if self.activatedColumns[key]:
                cols.append(self.scheduleFolder.columns[key])
        
        cols = sorted(cols,key=lambda x: x.abr)
        return cols
    
    def getDeactivatedColumns(self):
        cols = []
        
        for key in self.scheduleFolder.columns:
            if not self.activatedColumns[key]:
                cols.append(self.scheduleFolder.columns[key])
        
        cols = sorted(cols,key=lambda x: x.abr)
        return cols
    
    def deactivateColumn(self, key):
        b = QPushButton(
                RESTORE[self.lang] + ' ' + self.scheduleFolder.columns[key].name[self.lang])
        b.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #b.setMinimumSize(20,1)
        b.setStyleSheet(MAIN_BUTTONS_CSS)
        self.restoreButtonLayout.insertWidget(-1,b)
        b.clicked.connect(partial(self.activateColumn,key,b))
        self.restore_buttons[b] = key
        
        self.activatedColumns[key] = False
        self.draw()
    
    def activateColumn(self,key,b):
        self.activatedColumns[key] = True
        self.draw()
        b.deleteLater()
        del self.restore_buttons[b]
        
    def restoreAllColumns(self):
        for key in self.activatedColumns:
            self.activatedColumns[key] = True
        for b in self.restore_buttons:
            b.deleteLater()
        self.restore_buttons = {}
        self.draw()
    
    def translateWidgets(self):
        restoreButs = list(self.restoreButtonLayout.itemAt(i).widget() \
                           for i in range(1,self.restoreButtonLayout.count())) 

        for widget in self.centralwidget.findChildren(QPushButton):
            if widget not in restoreButs:
                try:
                    widget.setText(self.translateDict[widget][self.lang])
                except KeyError:
                    langDict = {}
                
                    for l in languages:
                        langDict[l] = trans(widget.text(), l)
                        key = widget
                
                    self.translateDict[key] = langDict
                    
                    widget.setText(self.translateDict[widget][self.lang])
            else:
                key = self.restore_buttons[widget]
                widget.setText(RESTORE[self.lang] + ' ' + self.scheduleFolder.columns[key].name['en'])
    
    def changeLang(self,lang):
        self.lang = lang
        self.translateWidgets()
        self.drawAlarm.start(1)
        self.updateDisplayedDate()
        self.updateNavBarDate()
        self.updateEventPopupText()



app = QApplication(sys.argv)

window = SchedulerGUI()
window.show()

sys.exit(app.exec_())