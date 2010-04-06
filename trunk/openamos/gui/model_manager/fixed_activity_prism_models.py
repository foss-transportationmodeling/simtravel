from PyQt4.QtCore import *
from PyQt4.QtGui import *



class FixedActivityPrismModels(QWidget):
    def __init__(self, parent=None):
        super(FixedActivityPrismModels,self).__init__(parent)
        
        self.setWindowTitle('Fixed Activity Prism Models')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        day_start = QPushButton('Earliest start of day \n(time one can leave home)', self)
        day_start.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 370,200, 50)
        day_start.setStyleSheet("background-color: rgb(0, 255, 0)")
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        day_end = QPushButton("Latest end of day (time \nby which one has to be home)", self)     
        day_end.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 290, 200, 50)

        
        worker = QPushButton('Worker', self)
        worker.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 180, 180, 50)


        non_worker = QPushButton('Non-worker', self)
        non_worker.setGeometry((size.width()) / 2 - 195, size.height() / 2 - 180, 180, 50)


        children_adults = QPushButton('Children (Status-School) \53 \nAdults (Status-School)', self)
        children_adults.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 180, 180, 50)


        children = QPushButton('Children \n(Status \55 Pre-school)', self)
        children.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 180, 180, 50)


        num_work_episodes = QPushButton('For each job, number of \nwork episodes \n\nSeparate models \55 first \njob, second job. Also, \nvertices for each episode \nshould be conditional on \nthe previous one to \nensure consistency', self)
        num_work_episodes.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 100, 180, 200)


        work_start_1 = QPushButton('Latest arrival at work \nfor each episode', self)
        work_start_1.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 130, 180, 50)


        work_end_1 = QPushButton('Earliest departure from \nwork for each episode', self)
        work_end_1.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 210, 180, 50)


        num_sch_episodes = QPushButton('Number of school episodes', self)
        num_sch_episodes.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 100, 180, 50)


        sch_start_1 = QPushButton('Latest arrival at school', self)
        sch_start_1.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 20, 180, 50)


        sch_end_1 = QPushButton('Earliest departure \nfrom school', self)
        sch_end_1.setGeometry((size.width()) / 2 + 15, size.height() / 2 + 60, 180, 50)


        pre_sch = QPushButton('The arrival and \ndeparture time from \nPre-school are dependent \non the adult \n(worker/non-worker) that \nthe kid is assigned \nto', self)
        pre_sch.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 100, 180, 200)


        t_s_prism_vertices = QPushButton('Time-space prism vertices of all \nindividuals within the population', self)
        t_s_prism_vertices.setGeometry((size.width()) / 2 - 150, size.height() / 2 + 320, 300, 50)




   
    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 320, widgetwidth / 2, widgetheight / 2 - 210)
        line.drawLine(widgetwidth / 2 - 315, widgetheight / 2 - 210, widgetwidth / 2 + 315, widgetheight / 2 - 210)
        line.drawLine(widgetwidth / 2 - 315, widgetheight / 2 - 210, widgetwidth / 2 - 315, widgetheight / 2 + 290)
        line.drawLine(widgetwidth / 2 - 105, widgetheight / 2 - 210, widgetwidth / 2 - 105, widgetheight / 2 + 290)
        line.drawLine(widgetwidth / 2 + 105, widgetheight / 2 - 210, widgetwidth / 2 + 105, widgetheight / 2 + 290)
        line.drawLine(widgetwidth / 2 + 315, widgetheight / 2 - 210, widgetwidth / 2 + 315, widgetheight / 2 + 290)
        line.drawLine(widgetwidth / 2 - 315, widgetheight / 2 + 290, widgetwidth / 2 + 315, widgetheight / 2 + 290)
        line.drawLine(widgetwidth / 2 - 315, widgetheight / 2 + 100, widgetwidth / 2 - 315, widgetheight / 2 - 100)
        line.drawLine(widgetwidth / 2, widgetheight / 2 + 290, widgetwidth / 2, widgetheight / 2 + 320)

        line.drawLine(widgetwidth / 2, widgetheight / 2 - 35, widgetwidth / 2, widgetheight / 2 + 85)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 35, widgetwidth / 2 +105, widgetheight / 2 - 35)
        line.drawLine(widgetwidth / 2, widgetheight / 2 + 85, widgetwidth / 2 + 15, widgetheight / 2 + 85)

        line.drawLine(widgetwidth / 2 - 420, widgetheight / 2 + 115, widgetwidth / 2 - 420, widgetheight / 2 + 235)
        line.drawLine(widgetwidth / 2 - 420, widgetheight / 2 + 115, widgetwidth / 2 - 315, widgetheight / 2 + 115)
        line.drawLine(widgetwidth / 2 - 420, widgetheight / 2 + 235, widgetwidth / 2 - 315, widgetheight / 2 + 235)        
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()
        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 210)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 + 130)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 + 210)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 + 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 105)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 105)  
        point.setY(widgetheight / 2 + 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 105)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 105)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 105)  
        point.setY(widgetheight / 2 - 20)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 105)  
        point.setY(widgetheight / 2 + 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 105)  
        point.setY(widgetheight / 2 + 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 315)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 315)  
        point.setY(widgetheight / 2 + 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 315)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.end()

        




 


