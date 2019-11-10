from PyQt5.QtWidgets import QCalendarWidget


class MyCalendar(QCalendarWidget):
    def __init__(self,parent=None):
        QCalendarWidget.__init__(self,parent)
        
        
    def paintCell(self, painter, rect, date):
        print('painting')
        QCalendarWidget.paintCell(self, painter, rect, date)
        
        
        if date.day() % 5 == 0: # example condition based on date
            painter.drawText(rect.bottomLeft(), "test")