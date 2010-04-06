from PyQt4.QtCore import *
from PyQt4.QtGui import *



class LongTermModels(QWidget):
    def __init__(self, parent=None):
        super(LongTermModels, self).__init__(parent)
        self.setWindowTitle('Long_Term_Choices')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
     
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        generate_synthetic_population = QPushButton('Generate Synthetic Population', self)
        generate_synthetic_population.setGeometry((size.width())/2 - 100, size.height() / 2 - 400,200, 50)

        self.connect(generate_synthetic_population, SIGNAL('clicked()'),
                     qApp, SLOT('deleteLater()'))


        
        labor_force_participation_model = QPushButton('If worker status was not \n generated then run a Labor \n Force Participation Model to \n simulate the worker status \n individuals', self)
        labor_force_participation_model.setGeometry((size.width())/2 - 100, size.height() / 2 - 320, 200, 110)

        
        number_of_jobs = QPushButton('For each worker identify \n the number of jobs', self)
        number_of_jobs.setGeometry((size.width())/2 - 100, size.height() / 2 - 180, 200, 50)


        primary_worker = QPushButton('Primary worker in the \nhousehold \n\nIn the absence of data \nidentified based on personal \nincome', self)
        primary_worker.setGeometry((size.width())/2 - 100, size.height() / 2 - 100, 200, 130)


        school_status  = QPushButton('School status of everyone \nincluding those individuals \nthat are workers', self)
        school_status.setGeometry((size.width())/2 - 100, size.height() / 2 + 60, 200, 70)


        residential_location_choice  = QPushButton('Residential Location Choice', self)
        residential_location_choice.setGeometry((size.width())/2 - 100, size.height() / 2 + 160, 200, 50)

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine((widgetwidth) / 2, widgetheight / 2 - 350, (widgetwidth) / 2, widgetheight / 2 + 160)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 160)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        arrow.end()



 


