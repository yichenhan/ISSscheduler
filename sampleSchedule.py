from scheduler import Scheduler, TimeTape, Column, Event, SchedulerFolder
languages = ['en','ru','de','ja','fr','it']

from PyQt5.QtCore import QDate

from PyQt5.QtCore import *
from PyQt5.QtGui import *

P = QColor(198,169,186) # Experiments
B = QColor(111,160,188) 
BG = QColor(114,169,143) # Exercise
G = QColor(153,232,122) # Meeting Events
O = QColor(242,195,101) #Special Events
GR = QColor(181,181,181) # Everyday events

def sampleSchedule():
    GMT = TimeTape('GMT',0)
    EST = TimeTape('EST',-5)
    
    column1 = Column('SS CDR Borisenko', languages, abr = 'SS CDR')
    column2 = Column('FE-1 Samokutyaev', languages, abr = 'FE1')
    column3 = Column('FE-3 Garan', languages, abr = 'FE3')
    column4 = Column('CDR Mark', languages, abr = 'CDR')
    column5 = Column('PLT BOX', languages, abr = 'PLT')
    column6 = Column('MS1 Spanky', languages, abr = 'MS1')
    column7 = Column('MS2 Roberto', languages, abr = 'MS2')
    column8 = Column('MS3 Drew', languages, abr = 'MS3')
    column9 = Column('MS4 Taz', languages, abr = 'MS4')
    
    columns = [column1,column2,column3,column4,column5,column6,
               column7,column8,column9]

    
    events = [Event('12:30','12:40','Experiment','In the lab','throw the lab', 'A',languages),
              Event('0:00','1:30','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','SS CDR',languages,color = GR),
              Event('0:00','1:30','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','FE1',languages,color = GR),
              Event('0:00','1:30','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','FE3',languages,color = GR),
              Event('0:00','2:30','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','CDR',languages,color = GR),
              Event('0:00','2:00','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','PLT',languages,color = GR),
              Event('0:00','2:00','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','MS1',languages,color = GR),
              Event('0:00','2:45','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','MS2',languages,color = GR),
              Event('0:00','2:00','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','MS3',languages,color = GR),
              Event('0:00','2:30','Post Sleep', 'Summary','Station Morning Inspection.\nBreakfast.','MS4',languages,color = GR),
              
              Event('6:15','7:15','Midday Meal', 'Summary','Description','SS CDR',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','FE1',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','FE3',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','CDR',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','PLT',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','MS1',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','MS2',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','MS3',languages,color = GR),
              Event('6:15','7:15','Midday Meal', 'Summary','Description','MS4',languages,color = GR),
              
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','SS CDR',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','FE1',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','FE3',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','CDR',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','PLT',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','MS1',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','MS2',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','MS3',languages,color = G),
              Event('7:15','7:35','Crew Meeting', 'Discuss subjects X,Y,Z','Description','MS4',languages,color = G),
              
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','SS CDR',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','FE1',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','FE3',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','CDR',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','PLT',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','MS1',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','MS2',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','MS3',languages,color = O),
              Event('11:00','11:15','CDR Mark Farewell', 'Bye Mark','Description','MS4',languages,color = O),
              
              Event('15:00','24:00','Sleep', 'Summary','Description','SS CDR',languages,color = GR),
              Event('15:00','24:00','Sleep', 'Summary','Description','FE1',languages,color = GR),
              Event('15:00','24:00','Sleep', 'Summary','Description','FE3',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','CDR',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','PLT',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','MS1',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','MS2',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','MS3',languages,color = GR),
              Event('15:30','24:00','Sleep', 'Summary','Description','MS4',languages,color = GR),
              
              Event('13:20','15:00','Pre Sleep', 'Summary','Description','SS CDR',languages,color = GR),
              Event('13:05','15:00','Pre Sleep', 'Summary','Description','FE1',languages,color = GR),
              Event('13:05','15:00','Pre Sleep', 'Summary','Description','FE3',languages,color = GR),
              Event('14:15','15:30','Pre Sleep', 'Summary','Description','CDR',languages,color = GR),
              Event('12:50','15:30','Pre Sleep', 'Summary','Description','PLT',languages,color = GR),
              Event('12:50','15:30','Pre Sleep', 'Summary','Description','MS1',languages,color = GR),
              Event('12:50','15:30','Pre Sleep', 'Summary','Description','MS2',languages,color = GR),
              Event('12:50','15:30','Pre Sleep', 'Summary','Description','MS3',languages,color = GR),
              Event('12:50','15:30','Pre Sleep', 'Summary','Description','MS4',languages,color = GR),
              
              Event('1:30','1:45','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','SS CDR',languages,color = G),
              Event('1:30','1:45','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','FE1',languages,color = G),
              Event('1:30','1:45','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','FE3',languages,color = G),
              
              Event('11:15','12:15','Exercise T2', 'Summary','Description','SS CDR',languages,color = BG),
              Event('11:15','12:15','Exercise VE', 'Summary','Description','FE1',languages,color = BG),
              
              Event('4:30','6:00','Exercise ARED-CDF', 'Summary','Description','SS CDR',languages,color = BG),
              
              Event('8:00','8:30','Collect Tools', 'Summary','Description','SS CDR',languages,color = B),
              Event('8:45','9:15','TEX 15 Experiment', 'Summary','Description','SS CDR',languages,color = P),
              
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','SS CDR',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','FE1',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','FE3',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','PLT',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','MS1',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','MS2',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','MS3',languages,color = GR),
              Event('12:15','12:50','Evening Meal', 'Summary','Pizza','MS4',languages,color = GR),
              
              Event('12:50','13:05','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','SS CDR',languages,color = G),
              Event('12:50','13:05','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','FE1',languages,color = G),
              Event('12:50','13:05','Daily Planning', 'Discuss Daily Plan and Procedures','Audio Configuration (A):S/G 1. Minimum 15 minutes with MSFC, ESA, SSIPC, and MCC-M. Can be held via S-BD.','FE3',languages,color = G),
              
              Event('13:05','13:20','HM Conference', 'Summary','Description','SS CDR',languages,color = G),
              
              Event('8:00','8:45','COX-MN','Summary','Description','FE1',languages,color = B),
              Event('8:45','10:15','Exercise-T2','Summary','Description','FE1',languages,color = BG),
              
              Event('2:00','5:00','Solar Observation', 'Summary','Description','FE3',languages,color = P),
              Event('5:00','6:00','Exercise T2', 'Summary','Description','FE3',languages,color = BG),
              
              Event('6:00','6:15','IMM Preparation', 'Summary','Description','FE3',languages,color = B),
              Event('7:35','8:15','IMM', 'Summary','Description','FE3',languages,color = B),
              
              Event('8:20','9:50','Exercise ARED', 'Summary','Description','FE3',languages,color = BG),
              Event('9:50','10:40','Station Check', 'Summary','Description','FE3',languages,color = B),
              
              Event('10:40','11:00','Station Announcement', 'Summary','Description','FE3',languages,color = G),
              
              Event('11:15','11:40','Hatch Operation', 'Summary','Description','FE3',languages,color = B),
              Event('11:40','11:50','Station Announcement', 'Summary','Description','FE3',languages,color = G),
              
              Event('3:00','5:30','Power Check', 'Summary','Description','CDR',languages,color = B),
              Event('8:00','9:15','Exercise', 'Summary','Description','CDR',languages,color = BG),
              Event('9:15','10:00','Spinal Exercise', 'Summary','Description','CDR',languages,color = BG),
              Event('10:15','11:00','Oxygen Transfer', 'Summary','Description','CDR',languages,color = B),
              
              Event('2:40','3:40','Exercise', 'Summary','Description','PLT',languages,color = BG),
              Event('3:40','6:00','Middeck Transfer', 'Summary','Description','PLT',languages,color = B),
              
              Event('2:00','5:00','Solar Observation', 'Summary','Description','MS1',languages,color = P),
              Event('7:40','10:20','Stowage', 'Summary','Description','PLT',languages,color = B),
              Event('11:15','11:40','Hatch Operation', 'Summary','Description','PLT',languages,color = B),
              
              Event('8:15','8:30','DCP Preparation', 'Summary','Description','MS1',languages,color = B),
              Event('8:30','10:30','DCP Pack', 'Summary','Description','MS1',languages,color = B),
              Event('8:30','9:45','DCP Pack', 'Summary','Description','MS4',languages,color = B),
              
              Event('11:15','12:15','Exercise', 'Summary','Description','MS1',languages,color = BG),
              Event('3:15','4:15','Exercise', 'Summary','Description','MS2',languages,color = BG),
              
              Event('2:45','5:45','EVA Tool Stow', 'Summary','Description','MS3',languages,color = B),
              Event('2:45','5:45','EVA Tool Stow', 'Summary','Description','MS4',languages,color = B),
              
              Event('4:15','6:15','Middeck Transfer', 'Summary','Description','MS2',languages,color = B),
              Event('5:45','6:15','Middeck Transfer', 'Summary','Description','MS3',languages,color = B),
              
              Event('8:00','9:20','Middeck Transfer', 'Summary','Description','MS2',languages,color = B),
              Event('8:00','9:20','Middeck Transfer', 'Summary','Description','MS3',languages,color = B),
              
              Event('9:20','10:20','Exercise', 'Summary','Description','MS3',languages,color = BG),
              Event('10:00','11:00','Exercise', 'Summary','Description','MS4',languages,color = BG),
              
              Event('11:20','12:15','Rendezvous Tools', 'Summary','Description','MS4',languages,color = B),
              Event('11:20','12:15','Rendezvous Tools', 'Summary','Description','MS2',languages,color = B)]
    
    schedule1 = Scheduler(events)
    
    events = [Event('2:40','4:40','Exercise', 'Summary','Description','PLT',languages,color = BG),
              Event('3:40','6:40','Exercise', 'Summary','Description','MS1',languages,color = BG),
              Event('2:40','4:40','Exercise', 'Summary','Description','MS2',languages,color = BG),
              Event('11:40','12:00','TV Interview', 'Summary','Description','FE3',languages,color = G)]
    
    schedule2 = Scheduler(events)
    
    events = [Event('3:00','5:30','Power Check', 'Summary','Description','CDR',languages,color = B),
              Event('8:00','9:15','Exercise', 'Summary','Description','CDR',languages,color = BG),
              Event('2:40','4:40','Exercise', 'Summary','Description','MS2',languages,color = BG),
              Event('14:00','15:00','TV Interview', 'Summary','Description','SS CDR',languages,color = G)]
    
    schedule3 = Scheduler(events)
    
    schedulers = {}
    schedulers[QDate.currentDate()] = schedule1
    schedulers[QDate.currentDate().addDays(1)] = schedule2
    schedulers[QDate.currentDate().addDays(-3)] = schedule3
    
    scheduleFolder = SchedulerFolder([GMT,EST], columns, schedulers)
    
    return scheduleFolder