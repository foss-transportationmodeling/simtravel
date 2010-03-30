from PyQt4.QtCore import *
from PyQt4.QtGui import *



class Skeleton_Reconciliation_System(QWidget):
    def __init__(self, parent=None):
        super(Skeleton_Reconciliation_System, self).__init__(parent)
        
        self.setWindowTitle('Activity Skeleton Reconciliation System')
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        skeletonrecbutton = QPushButton('Activity \nSkeleton Reconciliation', self)
        skeletonrecbutton.setGeometry((size.width()) / 2 - 300, size.height() / 2 - 220, 200, 80)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        personconstraints1button = QPushButton("Within person constraints", self)     
        personconstraints1button.setGeometry((size.width()) / 2 - 300, size.height() / 2 - 110, 200, 80)

        
        adjustment1button = QPushButton('Adjustments to the activity \nskeleton based on expected \nTravel Time from previous day', self)
        adjustment1button.setGeometry((size.width()) / 2 - 300, size.height() / 2, 200, 80)


        patternrecbutton = QPushButton('Activity-travel \nPattern Reconciliation', self)
        patternrecbutton.setGeometry((size.width()) / 2 + 100, size.height() / 2 - 220, 200, 80)


        personconstraints2button = QPushButton("Within person constraints", self)     
        personconstraints2button.setGeometry((size.width()) / 2 + 100, size.height() / 2 - 110, 200, 80)


        hholdconstraints2button = QPushButton("Within household constraints", self)     
        hholdconstraints2button.setGeometry((size.width()) / 2 + 100, size.height() / 2, 200, 80)


        adjustment2button = QPushButton('Duration adjustment \nafter arrival', self)
        adjustment2button.setGeometry((size.width()) / 2 + 100, size.height() / 2 + 110, 200, 80)

    def paintEvent(self, parent = None):
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2 - 200, widgetheight / 2 - 140, widgetwidth / 2 - 200, widgetheight / 2)
        line.drawLine(widgetwidth / 2 + 200, widgetheight / 2 - 140, widgetwidth / 2 + 200, widgetheight / 2 + 110)
        line.end()

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


 


