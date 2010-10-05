# -*- coding: cp936 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class VehicleOwnershipModels(QWidget):
    def __init__(self, parent=None, co=None):
        super(VehicleOwnershipModels, self).__init__(parent)
        
        self.setWindowTitle('Vehicle Ownership Model')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        num_vehs_button = QPushButton('Count of Vehicles \nOwned by The household', self)
        num_vehs_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 180,200, 50)
        self.connect(num_vehs_button, SIGNAL('clicked()'), self.num_vehs)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        veh_types_button = QPushButton("Vehicle body/fuel type \nfor each household vehicle \n\nIf the data permits also \nthe age of the vehicle \n\nBody types \55 Use the \ncategories from MOVES to \nenable emission estimation \n\nFuel types \55 Gasoline, Others", self)     
        veh_types_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 100, 200, 200)
        self.connect(veh_types_button, SIGNAL('clicked()'), self.veh_types)
        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
        
        self.configob = co
        
        
        
    def num_vehs(self):
        diagtitle = COMPMODEL_NUMVEHS
        modelkey = MODELKEY_NUMVEHS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def veh_types(self):
        diagtitle = COMPMODEL_NUMTYPES
        modelkey = MODELKEY_VEHTYPE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 130, widgetwidth / 2, widgetheight / 2 - 100)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        arrow.end()



 


