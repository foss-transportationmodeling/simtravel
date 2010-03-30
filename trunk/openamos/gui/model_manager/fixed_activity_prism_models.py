from PyQt4.QtCore import *
from PyQt4.QtGui import *



class FixedActivityPrismModels(QWidget):
    def __init__(self, parent=None):
        super(FixedActivityPrismModels,self).__init__(parent)
        
        self.setWindowTitle('Fixed Activity Prism Models')
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        daystartbutton = QPushButton('Earliest start of day \n(time one can leave home)', self)
        daystartbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 370,200, 50)
        daystartbutton.setStyleSheet("background-color: rgb(0, 255, 0)")
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        dayendbutton = QPushButton("Latest end of day (time \nby which one has to be home)", self)     
        dayendbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 290, 200, 50)

        
        workerbutton = QPushButton('Worker', self)
        workerbutton.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 180, 180, 50)


        nonworkerbutton = QPushButton('Non-worker', self)
        nonworkerbutton.setGeometry((size.width()) / 2 - 195, size.height() / 2 - 180, 180, 50)


        childrenadultsbutton = QPushButton('Children (Status-School) \53 \nAdults (Status-School)', self)
        childrenadultsbutton.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 180, 180, 50)


        childrenbutton = QPushButton('Children \n(Status \55 Pre-school)', self)
        childrenbutton.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 180, 180, 50)


        numworkepisodesbutton = QPushButton('For each job, number of \nwork episodes \n\nSeparate models \55 first \njob, second job. Also, \nvertices for each episode \nshould be conditional on \nthe previous one to \nensure consistency', self)
        numworkepisodesbutton.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 100, 180, 200)


        workstart1button = QPushButton('Latest arrival at work \nfor each episode', self)
        workstart1button.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 130, 180, 50)


        workend1button = QPushButton('Earliest departure from \nwork for each episode', self)
        workend1button.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 210, 180, 50)


        numschepisodesbutton = QPushButton('Number of school episodes', self)
        numschepisodesbutton.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 100, 180, 50)


        schstart1button = QPushButton('Latest arrival at school', self)
        schstart1button.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 20, 180, 50)


        schend1button = QPushButton('Earliest departure \nfrom school', self)
        schend1button.setGeometry((size.width()) / 2 + 15, size.height() / 2 + 60, 180, 50)


        preschbutton = QPushButton('The arrival and \ndeparture time from \nPre-school are dependent \non the adult \n(worker/non-worker) that \nthe kid is assigned \nto', self)
        preschbutton.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 100, 180, 200)


        tsprismverticesbutton = QPushButton('Time-space prism vertices of all \nindividuals within the population', self)
        tsprismverticesbutton.setGeometry((size.width()) / 2 - 150, size.height() / 2 + 320, 300, 50)


#        self.hbar = QScrollBar(self)
#        self.hbar.setGeometry(100, size.width() - 20, size.height() - 20, 20)
#        self.hbar.setOrientation(Qt.Horizontal)
#        self.hbar.setObjectName("horizontalScrollBar")
        
#        self.vbar = QScrollBar(self)
#        self.vbar.setGeometry(size.height() - 20, 0, 20, size.width() - 20)
#        self.vbar.setOrientation(Qt.Vertical)
#        self.vbar.setObjectName("verticalScrollBar")

   
    def paintEvent(self, parent = None):
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

        




 


