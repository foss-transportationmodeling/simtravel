# -*- coding: cp936 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class FixedActivityModels(QWidget):
    def __init__(self, parent=None):
        super(FixedActivityModels, self).__init__(parent)
        
        self.setWindowTitle('Fixed Activity Location Choice Generator')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        workers = QPushButton('Workers', self)
        workers.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 280,200, 50)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        children_adult = QPushButton("Children (Status-School) \n+ Adult (Status-School)", self)     
        children_adult.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 280, 200, 50)

        
        children = QPushButton('Children \n(Status-Preschool)', self)
        children.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 280, 200, 50)


        work_loc = QPushButton('For each job identify \na primary work location;\n\n\nDuring simulation, \ngenerate Choice Sets \nconditional on the home \nlocation e.g. within a 90 \nmin or 120 min travel time\n\nWork related trips/\nactivities will be generated \nduring the open periods to \naccount for multiple job \nsites per job', self)
        work_loc.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 200, 200, 400)


        school_loc = QPushButton('School location choice\n\nDuring simulation, \ngenerate Choice Sets \nconditional on the home \nlocation e.g. within a 60 \nmin', self)
        school_loc.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 200, 200, 400)


        preschool_loc = QPushButton('Pre-school location \nchoice\n\nDuring simulation, \ngenerate Choice Sets \nthat are within a 20 \nminute driving distance \nfrom home or work \nlocation of the adult(s)\n\nAlternatively just identify\n possible locations similar \nto school location', self)
        preschool_loc.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 200, 200, 400)


        activity_loc = QPushButton('Fixed activity locations for all individuals within the population', self)
        activity_loc.setGeometry((size.width()) / 4 - 100, size.height() / 2 + 230, (size.width()) / 2 + 200, 50)

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 4, widgetheight / 2 - 230, widgetwidth / 4, widgetheight / 2 - 200)
        line.drawLine(widgetwidth / 4, widgetheight / 2 + 200, widgetwidth / 4, widgetheight / 2 + 230)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 230, widgetwidth / 2, widgetheight / 2 - 200)
        line.drawLine(widgetwidth / 2, widgetheight / 2 + 200, widgetwidth / 2, widgetheight / 2 + 230)
        line.drawLine(widgetwidth * 3 / 4, widgetheight / 2 - 230, widgetwidth * 3 / 4, widgetheight / 2 - 200)
        line.drawLine(widgetwidth * 3 / 4, widgetheight / 2 + 200, widgetwidth * 3 / 4, widgetheight / 2 + 230)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 4)  
        point.setY(widgetheight / 2 - 200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(widgetheight / 2 + 230)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 230)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(widgetheight / 2 + 230)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(widgetheight / 2 - 200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(widgetheight / 2 + 230)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        arrow.end()


 


