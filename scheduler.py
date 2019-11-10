#from googletrans import Translator
#from goslate import Goslate

from translator import trans
from PyQt5.QtCore import QDate, Qt

class TimeTape():
    def __init__(self,name,GMToffset):
        
        self.times = []
        self.labels = []
        self.name = name
        
        for i in range(0,24):
            self.times.append((i + 24 + GMToffset) % 24)
        
            self.labels.append(str(self.times[i]) + ':00')
        
class Column():
    def __init__(self, name, languages, abr = ''):
        self.name = {}
        
        for lang in languages:
            self.name[lang] = trans(name,lang)
        
        if abr == '':
            self.abr = name
        else:
            self.abr = abr

class Event():
    def __init__(self,t0,t1,title,summary,description, column_abr, languages, color = Qt.blue, customGUI = None):
        self.t0 = t0
        self.t1 = t1
        self.column_abr = column_abr
        
        self.title = {}
        self.summary = {}
        self.description = {}
        
        self.color = color
        self.customGUI = customGUI
        
        for lang in languages:
            self.title[lang] = trans(title,lang)
            self.summary[lang] = trans(summary,lang)
            self.description[lang] = trans(description,lang)

class Scheduler():
    def __init__(self, events):
        self.events = events
    
class SchedulerFolder():
    def __init__(self, timeTapes, columns, schedulers):
        self.timeTapes = timeTapes
        self.schedulers = schedulers
        
        self.columns = {}
        
        for column in columns:
            self.columns[column.abr] = column
        
        