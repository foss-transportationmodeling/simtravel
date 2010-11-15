from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class Travel_Reconciliation_System(QWidget):
    def __init__(self, parent=None, co=None):
        super(Travel_Reconciliation_System, self).__init__(parent)
        
        self.setWindowTitle('Activity Travel Reconciliation System')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()

        pattern_onciliation_button = QPushButton('Activity-travel \nPattern Reconciliation', self)
        pattern_onciliation_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 270, 200, 80)
        #self.connect(pattern_onciliation_button, SIGNAL('clicked()'), self.pattern_reconciliation)

        person_constraints_2_button = QPushButton("Within person constraints", self)     
        person_constraints_2_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 160, 200, 80)
        #self.connect(person_constraints_2_button, SIGNAL('clicked()'), self.person_constraints_2)

        hhold_constraints_button = QPushButton("Within household constraints", self)     
        hhold_constraints_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 50, 200, 80)
        #self.connect(hhold_constraints_button, SIGNAL('clicked()'), self.hhold_constraints)

        adjustment_2_button = QPushButton('Duration adjustment \nafter arrival', self)
        adjustment_2_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 + 60, 200, 80)
        #self.connect(adjustment_2_button, SIGNAL('clicked()'), self.adjustment_2)
        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
        
        self.configob = co
        
        
#    def skeleton_reconciliation(self):
#        diagtitle = COMPMODEL_ASRECONCIL
#        modelkey = MODELKEY_ASRECONCIL
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def person_constraints_1(self):
#        diagtitle = COMPMODEL_ASCONST
#        modelkey = MODELKEY_ASCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def adjustment_1(self):
#        diagtitle = COMPMODEL_ASADJUST
#        modelkey = MODELKEY_ASADJUST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def pattern_reconciliation(self):
#        diagtitle = COMPMODEL_ATRECONCIL
#        modelkey = MODELKEY_ATRECONCIL
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def person_constraints_2(self):
#        diagtitle = COMPMODEL_ATPERCONST
#        modelkey = MODELKEY_ATPERCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def hhold_constraints(self):
#        diagtitle = COMPMODEL_ATHOUCONST
#        modelkey = MODELKEY_ATHOUCONST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
#        
#    def adjustment_2(self):
#        diagtitle = COMPMODEL_ATADJUST
#        modelkey = MODELKEY_ATADJUST
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()       
        

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        #line.drawLine(widgetwidth / 2 - 200, widgetheight / 2 - 140, widgetwidth / 2 - 200, widgetheight / 2)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 190, widgetwidth / 2, widgetheight / 2 + 60)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
#        point.setX(widgetwidth / 2 - 200)  
#        point.setY(widgetheight / 2 - 110)
#        arrow.setBrush(QColor("black"))
#        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
#
#        point.setX(widgetwidth / 2 - 200)  
#        point.setY(widgetheight / 2)
#        arrow.setBrush(QColor("black"))
#        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 160)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 50)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.end()


 


