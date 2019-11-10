import sys
from untitled import Ui_MainWindow
from PyQt5 import QtWidgets

from PyQt5 import QtCore, QtGui

NUM_X = 24
NUM_Y = 5
X_MARG = 0
Y_MARG = 10

spacing = [50,200,200,200]

contents = []

row0 = [[],[]]
for i in range(0,24):
    row0[0].append(i)
    
    l = str(i) + ':00'
    #l = QtWidgets.QGraphicsWidget(l)
    row0[1].append(l)
    
contents.append(row0)

row1 = [[],[]]

storedInfo = ['5:00','5:05','Spaghetti','Cook it']
row1[1].append(storedInfo)
storedInfo = ['6:07','6:17','Orange Juice','Eat it']
row1[1].append(storedInfo)
contents.append(row1)

def timeStrToFloat(string):
    hour = float(string.partition(':')[0])
    minute = float(string.partition(':')[2])
    
    return hour + minute / 60
    
class MyFirstGuiProgram(QtWidgets.QMainWindow, Ui_MainWindow):
    
    resized = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        
        self.resized.connect(self.draw)
        
        self.setupUi(self)
        self.graphicsView.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        self.graphicsView.setMinimumWidth(1200)
        self.graphicsView.setMinimumHeight(500)
        
        self.pen = QtGui.QPen(QtCore.Qt.gray)
        
    
    def createWidgets(self, storedInfo, spacing, current_y):
        t0 = storedInfo[0]
        t1 = storedInfo[1]
        title = storedInfo[2]
        desc = storedInfo[3]
        
        t0_f = timeStrToFloat(t0)
        t1_f = timeStrToFloat(t1)
        
        length = (t1_f - t0_f) * (self.w/24)
        print(t0_f, t1_f)
        
        
        r = QtCore.QRectF(QtCore.QPointF(t0_f * (self.w/24), current_y), 
                                  QtCore.QSizeF(length, spacing))
        
        pen2 = QtGui.QPen(QtCore.Qt.blue)
        brush = QtGui.QBrush(QtCore.Qt.blue)
        self.scene.addRect(r, pen2, brush)
        
        x = QtWidgets.QLabel(title)
        x.move(t0_f * (self.w/24), current_y)

        self.scene.addWidget(x)
        
        
        
    
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MyFirstGuiProgram, self).resizeEvent(event)
    
    def draw(self):
        self.scene = QtWidgets.QGraphicsScene()   
        
        #w = self.graphicsView.width() - 2 * X_MARG
        self.w = 4000
        self.h = self.graphicsView.height() - 2 * Y_MARG
        #h = sum(spacing)
        #self.h = sum(spacing) - 2 * Y_MARG
        
        side_X = (self.w) / NUM_X
        side_Y = (self.h) / NUM_Y
        
        for i in range(1,NUM_X):
            #l = QtCore.QLine()
            self.scene.addLine(i*side_X,Y_MARG,i*side_X,self.h-Y_MARG, self.pen)
        
        
        current_y = Y_MARG
        
        for i in range(0,len(contents)):
            
            
            for j in range(0,len(contents[i][1])):
                
                if isinstance(contents[i][1][j],str):
                    x = QtWidgets.QLabel(contents[i][1][j])
                    x.move(contents[i][0][j] * (self.w/24), current_y)
                    self.scene.addWidget(x)
                else:
                    self.createWidgets(contents[i][1][j],spacing[i],current_y)
            
            current_y += spacing[i]

            self.scene.addLine(X_MARG,current_y,self.w-X_MARG,current_y)
        
        
        '''
        for i in range(NUM_X):
            for j in range(NUM_Y):
                r = QtCore.QRectF(QtCore.QPointF(i*side_X, j*side_Y), 
                                  QtCore.QSizeF(side_X, side_Y))
                self.scene.addRect(r, self.pen)
        '''
        
        self.graphicsView.setScene(self.scene)
        print("someFunction")



def closeEvent(self):
    quit()
    
app = QtWidgets.QApplication(sys.argv)
window = MyFirstGuiProgram()
window.show()
window.draw()

window.closeEvent = closeEvent

sys.exit(app.exec_())