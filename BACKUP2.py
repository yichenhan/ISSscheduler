import sys
from functools import partial
#from googletrans import Translator
#from goslate import Goslate
from translator import trans

from layout import Ui_MainWindow
from scheduler import Scheduler, TimeTape, Column, Event

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, \
                            QGraphicsScene, QLabel, QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5 import QtCore
from PyQt5 import QtGui


languages = ['en','ru','de']

WIDTH_TL = 40
Y_SIDE = 80

MAX_EVENT_FONT_PT = 16
MIN_EVENT_FONT_PT = 5
DEFAULT_EVENT_FONT = "times"

RESTORE = {}
for l in languages:
    RESTORE[l] = trans('Restore', l)

def timeStrToFloat(string):
    hour = float(string.partition(':')[0])
    minute = float(string.partition(':')[2])
    
    return hour + minute / 60

class SchedulerGUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        
        self.schedule = sampleSchedule()
        
        self.activatedColumns = {}
        
        for key in self.schedule.columns:
            self.activatedColumns[key] = True
        
        self.lang = 'en'
        
        self.restore_buttons = []
        self.restoreAllButton.clicked.connect(self.restoreAllColumns)
        
        self.translateDict = {}
        for widget in self.centralwidget.findChildren((QPushButton,QLabel)):
            langDict = {}
            
            for l in languages:
                langDict[l] = trans(widget.text(), l)
            key = widget
            
            self.translateDict[key] = langDict
        
        self.translateWidgets()
        
        self.language0Button.clicked.connect(partial(self.changeLang,'en'))
        self.language1Button.clicked.connect(partial(self.changeLang,'ru'))
        self.language2Button.clicked.connect(partial(self.changeLang,'de'))
        
        self.drawAlarm = QTimer()
        self.drawAlarm.timeout.connect(self.drawAlarmFunc)
        self.drawAlarm.start(0.3)
        
    def closeEvent(self, event):
        quit()
    
    def resizeEvent(self, event):
        self.draw()
    
    def drawAlarmFunc(self):
        self.drawAlarm.stop()
        self.draw()
    
    def draw(self):
        self.scheduleScene = QGraphicsScene() 
        self.activatedScene = QGraphicsScene()
        
        self.w = self.scheduleView.width()
        self.h = Y_SIDE * 24
        self.h_a = self.activatedView.height()
        
        self.gridPen = QPen(QtCore.Qt.gray)
        
        for i in range(0,24):
            self.scheduleScene.addLine(0, i * Y_SIDE, self.w, i * Y_SIDE)
        
        self.drawTimeTapes()
        
        cols = self.getActivatedColumns()
        
        if (len(cols) > 0):
            self.drawColumns(cols)
            
        self.scheduleView.setScene(self.scheduleScene)
        self.activatedView.setScene(self.activatedScene)
        
    
    def drawTimeTapes(self):
        for i in range(0,len(self.schedule.timeTapes)):
            self.scheduleScene.addLine(WIDTH_TL * i, 0, WIDTH_TL * i, self.h)
            
            self.activatedScene.addLine(WIDTH_TL * i, 0, WIDTH_TL * i, self.h_a)
            
            l = QLabel(self.schedule.timeTapes[i].name)
            l.move(WIDTH_TL * i, 0)
            self.activatedScene.addWidget(l)
            
            for j in range(0,24):
                l = QLabel(self.schedule.timeTapes[i].labels[j])
                l.move(WIDTH_TL * i, Y_SIDE * j)
                self.scheduleScene.addWidget(l)
    
    def drawColumns(self, cols):
        x_offset = WIDTH_TL * len(self.schedule.timeTapes)
        
        act_col_width = (self.w - x_offset) / len(cols)
        
        self.deactivateButtons = []
        for i in range(0,len(cols)):
            self.scheduleScene.addLine(x_offset + act_col_width * i, 0, 
                                       x_offset + act_col_width * i, self.h)
            self.activatedScene.addLine(x_offset + act_col_width * i, 0, 
                                        x_offset + act_col_width * i, self.h_a)
            
            b = QPushButton(cols[i].name[self.lang])
            b.move(x_offset + act_col_width * i,0)
            b.clicked.connect(
                    partial(self.deactivateColumn,cols[i].abr))
            b.setSizePolicy(QSizePolicy.Ignored, 
                            QSizePolicy.Ignored)
            b.resize(act_col_width, self.h_a)
            b = self.activatedScene.addWidget(b)
            
            
            for event in cols[i].events:
                self.drawEvent(event,x_offset,act_col_width,i)
                
    def drawEvent(self,event,x_offset,col_width,x_loc):
        t0_f = timeStrToFloat(event.t0)
        t1_f = timeStrToFloat(event.t1)
        
        length = (t1_f - t0_f) * (self.h / 24)
        
        space = QtCore.QSizeF(col_width, length)
        
        ### Checks maximum font size if level
        font_size = MAX_EVENT_FONT_PT
        
        l_title = QLabel(event.title[self.lang])
        l_time = QLabel(' (' + event.t0 + ' - ' + event.t1 + ')')
    
        l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
        l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
        
        title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + \
            l_time.fontMetrics().boundingRect(l_time.text()).width()
        title_height = l_title.fontMetrics().boundingRect(l_title.text()).height()
        
        while (title_height > length or title_width > col_width) and font_size > MIN_EVENT_FONT_PT:
            font_size -= 1
            
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
            
            title_width = l_title.fontMetrics().boundingRect(l_title.text()).width() + \
                        l_time.fontMetrics().boundingRect(l_time.text()).width()
            title_height = l_title.fontMetrics().boundingRect(l_title.text()).height()
        
        font_size_level = font_size
        over_height_level = title_height - length
        over_width_level = title_width - col_width
        
        ### Checks maximum font size ifstacked
        font_size = MAX_EVENT_FONT_PT
        
        l_title = QLabel(event.title[self.lang])
        l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
        
        l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
        l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
        
        title_width = max(l_title.fontMetrics().boundingRect(l_title.text()).width(),
                          l_time.fontMetrics().boundingRect(l_time.text()).width())
        title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + \
            l_time.fontMetrics().boundingRect(l_time.text()).height()
        
        while (title_height > length or title_width > col_width) and font_size > MIN_EVENT_FONT_PT:
            font_size -= 1
            
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Bold))
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size, QtGui.QFont.Normal))
            
            title_width = max(l_title.fontMetrics().boundingRect(l_title.text()).width(),
                          l_time.fontMetrics().boundingRect(l_time.text()).width())
            title_height = l_title.fontMetrics().boundingRect(l_title.text()).height() + \
                    l_time.fontMetrics().boundingRect(l_time.text()).height()
        
        font_size_stacked = font_size
        over_height_stacked = title_height - length
        over_width_stacked = title_width - col_width
        
        ### Doesn't draw labels if there is no way to fit them in the available
        #space
        if ((over_width_level > 0 or over_height_level > 0) and \
        (over_width_stacked > 0 or over_height_stacked > 0)):
            r = QtCore.QRectF(QtCore.QPointF(x_offset + x_loc * col_width, 
                                         t0_f * (self.h/24)), space)
        
            pen = QtGui.QPen(QtCore.Qt.red)
            brush = QtGui.QBrush(QtCore.Qt.red)
            self.scheduleScene.addRect(r, pen, brush)
            
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
            l_title = QLabel(event.title[self.lang])
            l_time = QLabel(' (' + event.t0 + ' - ' + event.t1 + ')')
            
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_level, QtGui.QFont.Normal))
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_level, QtGui.QFont.Bold))
            
            l_title.move(x_offset + x_loc * col_width, t0_f * (self.h/24))
            l_time.move(x_offset + x_loc * col_width + \
                        l_title.fontMetrics().boundingRect(l_title.text()).width(), t0_f * (self.h/24))
        else:
            l_title = QLabel(event.title[self.lang])
            l_time = QLabel('(' + event.t0 + ' - ' + event.t1 + ')')
            
            l_time.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_stacked, QtGui.QFont.Normal))
            l_title.setFont(QtGui.QFont(DEFAULT_EVENT_FONT, font_size_stacked, QtGui.QFont.Bold))
            
            l_title.move(x_offset + x_loc * col_width, t0_f * (self.h/24))
            l_time.move(x_offset + x_loc * col_width, t0_f * (self.h/24) + \
                        l_title.fontMetrics().boundingRect(l_title.text()).height())
        
        r = QtCore.QRectF(QtCore.QPointF(x_offset + x_loc * col_width, 
                                         t0_f * (self.h/24)), space)
        
        pen = QtGui.QPen(QtCore.Qt.blue)
        brush = QtGui.QBrush(QtCore.Qt.blue)
        self.scheduleScene.addRect(r, pen, brush)
        
        self.scheduleScene.addWidget(l_title)
        self.scheduleScene.addWidget(l_time)
        
        
                
    
    def getActivatedColumns(self):
        cols = []
        
        for key in self.schedule.columns:
            if self.activatedColumns[key]:
                cols.append(self.schedule.columns[key])
        
        cols = sorted(cols,key=lambda x: x.abr)
        return cols
    
    def getDeactivatedColumns(self):
        cols = []
        
        for key in self.schedule.columns:
            if not self.activatedColumns[key]:
                cols.append(self.schedule.columns[key])
        
        cols = sorted(cols,key=lambda x: x.abr)
        return cols
    
    def deactivateColumn(self, key):
        b = QPushButton(
                RESTORE[self.lang] + ' ' + self.schedule.columns[key].name[self.lang])
        b.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #b.setMinimumSize(20,1)
        self.restoreButtonLayout.insertWidget(-1,b)
        b.clicked.connect(partial(self.activateColumn,key,b))
        self.restore_buttons.append(b)
        
        self.activatedColumns[key] = False
        self.draw()
    
    def activateColumn(self,key,b):
        self.activatedColumns[key] = True
        self.draw()
        b.deleteLater()
        self.restore_buttons.remove(b)
        
    def restoreAllColumns(self):
        for key in self.activatedColumns:
            self.activatedColumns[key] = True
        for b in self.restore_buttons:
            b.deleteLater()
        self.restore_buttons = []
        self.draw()
    
    def translateWidgets(self):
        for widget in self.centralwidget.findChildren((QPushButton,QLabel)):
            try:
                widget.setText(self.translateDict[widget][self.lang])
            except KeyError:
                langDict = {}
            
                for l in languages:
                    langDict[l] = trans(widget.text(), l)
                    key = widget
            
                self.translateDict[key] = langDict
                
                widget.setText(self.translateDict[widget][self.lang])
    
    def changeLang(self,lang):
        self.lang = lang
        self.translateWidgets()
        self.drawAlarm.start(1)
        
def sampleSchedule():
    GMT = TimeTape('GMT',0)
    EST = TimeTape('EST',-5)
    
    column1 = Column('Larry', languages, abr = 'L')
    column2 = Column('Gerry', languages, abr = 'G')
    column3 = Column('Alp', languages, abr = 'A')
    column4 = Column('Balp', languages, abr = 'B')
    column5 = Column('Calp', languages, abr = 'C')
    column6 = Column('Dalp', languages, abr = 'D')
    column7 = Column('Ealp', languages, abr = 'E')
    
    '''
    spaghet = Event('3:00','4:00','Spaghetti', 'Eat it', 'Eat with fork',
                    languages)
    column1.addEvent(spaghet)
    '''
    column3.events = [Event('3:00','4:00','Search', 'Eat it', 'Eat with fork',languages),
                      Event('4:45','5:00','Sleep','In the bed','For lots of time', languages)]
    
    column2.events = [Event('12:30','12:35','Experiment','In the lab','throw the lab', languages)]
    
    schedule = Scheduler([GMT,EST],[column1, column2, column3, column4, 
                         column5, column6,column7])

    return schedule



app = QApplication(sys.argv)

window = SchedulerGUI()
window.show()

sys.exit(app.exec_())