# -*- coding: cp936 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class VehicleOwnershipModels(QWidget):
    def __init__(self, parent=None):
        super(VehicleOwnershipModels, self).__init__(parent)
        
        self.setWindowTitle('Vehicle Ownership Model')
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        numvehsbutton = QPushButton('Count of Vehicles \nOwned by The household', self)
        numvehsbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 180,200, 50)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        vehtypesbutton = QPushButton("Vehicle body/fuel type \nfor each household vehicle \n\nIf the data permits also \nthe age of the vehicle \n\nBody types \55 Use the \ncategories from MOVES to \nenable emission estimation \n\nFuel types \55 Gasoline, Others", self)     
        vehtypesbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 100, 200, 200)

        

    def paintEvent(self, parent = None):
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 130, widgetwidth / 2, widgetheight / 2 - 100)

        
        line.end()




 


