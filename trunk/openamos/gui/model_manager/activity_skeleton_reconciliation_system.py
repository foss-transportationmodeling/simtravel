from PyQt4.QtCore import *
from PyQt4.QtGui import *



class Skeleton_Reconciliation_System(QWidget):
    def __init__(self, parent=None):
        super(Skeleton_Reconciliation_System, self).__init__(parent)
        
        self.setWindowTitle('Activity Skeleton Reconciliation System')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        skeleton_reconciliation_button = QPushButton('Activity \nSkeleton Reconciliation', self)
        skeleton_reconciliation_button.setGeometry((size.width()) / 2 - 300, size.height() / 2 - 220, 200, 80)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        person_constraints_1_button = QPushButton("Within person constraints", self)     
        person_constraints_1_button.setGeometry((size.width()) / 2 - 300, size.height() / 2 - 110, 200, 80)

        
        adjustment_1_button = QPushButton('Adjustments to the activity \nskeleton based on expected \nTravel Time from previous day', self)
        adjustment_1_button.setGeometry((size.width()) / 2 - 300, size.height() / 2, 200, 80)


        pattern_reconciliation_button = QPushButton('Activity-travel \nPattern Reconciliation', self)
        pattern_reconciliation_button.setGeometry((size.width()) / 2 + 100, size.height() / 2 - 220, 200, 80)


        person_constraints_2_button = QPushButton("Within person constraints", self)     
        person_constraints_2_button.setGeometry((size.width()) / 2 + 100, size.height() / 2 - 110, 200, 80)


        hhold_constraints_button = QPushButton("Within household constraints", self)     
        hhold_constraints_button.setGeometry((size.width()) / 2 + 100, size.height() / 2, 200, 80)


        adjustment_2_button = QPushButton('Duration adjustment \nafter arrival', self)
        adjustment_2_button.setGeometry((size.width()) / 2 + 100, size.height() / 2 + 110, 200, 80)

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2 - 200, widgetheight / 2 - 140, widgetwidth / 2 - 200, widgetheight / 2)
        line.drawLine(widgetwidth / 2 + 200, widgetheight / 2 - 140, widgetwidth / 2 + 200, widgetheight / 2 + 110)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 200)  
        point.setY(widgetheight / 2 - 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 200)  
        point.setY(widgetheight / 2)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        point.setX(widgetwidth / 2 + 200)  
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.end()


 


