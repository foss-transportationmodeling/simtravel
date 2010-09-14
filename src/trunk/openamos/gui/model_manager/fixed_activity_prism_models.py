from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *

class FixedActivityPrismModels(QWidget):
    def __init__(self, parent=None, co=None):
        super(FixedActivityPrismModels,self).__init__(parent)
        
        self.setWindowTitle('Fixed Activity Prism Models')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        #day_start_button = QPushButton('Earliest start of day \n(time one can leave home)', self)
        day_start_button = QPushButton(COMPMODEL_DAYSTART, self)
        day_start_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 370,200, 50)
        day_start_button.setStyleSheet("background-color: rgb(0, 255, 0)")
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        self.connect(day_start_button, SIGNAL('clicked()'), self.day_start)
        
        day_end_button = QPushButton(COMPMODEL_DAYEND, self)     
        day_end_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 290, 200, 50)
        self.connect(day_end_button, SIGNAL('clicked()'), self.day_end)

        
        worker_button = QPushButton('Worker', self)
        worker_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 180, 180, 50)


        non_worker_button = QPushButton('Non-worker', self)
        non_worker_button.setGeometry((size.width()) / 2 - 195, size.height() / 2 - 180, 180, 50)
        #self.connect(non_worker_button, SIGNAL('clicked()'), self.non_worker)


        children_adults_button = QPushButton('Children (Status-School) \53 \nAdults (Status-School)', self)
        children_adults_button.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 180, 180, 50)


        children_button = QPushButton('Children \n(Status \55 Pre-school)', self)
        children_button.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 180, 180, 50)


        num_work_episodes_button = QPushButton('For each job, number of \nwork episodes \n\nSeparate models \55 first \njob, second job. Also, \nvertices for each episode \nshould be conditional on \nthe previous one to \nensure consistency', self)
        num_work_episodes_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 100, 180, 200)
        self.connect(num_work_episodes_button, SIGNAL('clicked()'), self.num_work)


        work_start_1_button = QPushButton('Latest arrival at work \nfor each episode', self)
        work_start_1_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 130, 180, 50)
        self.connect(work_start_1_button, SIGNAL('clicked()'), self.work_start1)


        work_end_1_button = QPushButton('Earliest departure from \nwork for each episode', self)
        work_end_1_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 + 210, 180, 50)
        self.connect(work_end_1_button, SIGNAL('clicked()'), self.work_end1)


        num_sch_episodes_button = QPushButton('Number of school episodes', self)
        num_sch_episodes_button.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 100, 180, 50)
        self.connect(num_sch_episodes_button, SIGNAL('clicked()'), self.school_num)


        sch_start_1_button = QPushButton('Latest arrival at school', self)
        sch_start_1_button.setGeometry((size.width()) / 2 + 15, size.height() / 2 - 20, 180, 50)
        self.connect(sch_start_1_button, SIGNAL('clicked()'), self.school_start1)


        sch_end_1_button = QPushButton('Earliest departure \nfrom school', self)
        sch_end_1_button.setGeometry((size.width()) / 2 + 15, size.height() / 2 + 60, 180, 50)
        self.connect(sch_end_1_button, SIGNAL('clicked()'), self.school_end1)


        pre_sch_button = QPushButton('The arrival and \ndeparture time from \nPre-school are dependent \non the adult \n(worker/non-worker) that \nthe kid is assigned \nto', self)
        pre_sch_button.setGeometry((size.width()) / 2 + 225, size.height() / 2 - 100, 180, 200)
        self.connect(pre_sch_button, SIGNAL('clicked()'), self.pre_sch)


        t_s_prism_vertices_button = QPushButton('Time-space prism vertices of all \nindividuals within the population', self)
        t_s_prism_vertices_button.setGeometry((size.width()) / 2 - 150, size.height() / 2 + 320, 300, 50)
        #self.connect(t_s_prism_vertices_button, SIGNAL('clicked()'), self.t_s_prism_vertices)
        
        self.configob = co

        
    def day_start(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def day_end(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def num_work(self):
        diagtitle = COMPMODEL_NUMWRKEPISODES
        modelkey = MODELKEY_NUMWRKEPISODES
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def work_start1(self):
        diagtitle = COMPMODEL_WORKSTART1
        modelkey = MODELKEY_WORKSTART1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def work_end1(self):
        diagtitle = COMPMODEL_WORKEND1
        modelkey = MODELKEY_WORKEND1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_num(self):
        diagtitle = COMPMODEL_NUMSCHEPISODES
        modelkey = MODELKEY_NUMSCHEPISODES
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_start1(self):
        diagtitle = COMPMODEL_SCHSTART1
        modelkey = MODELKEY_SCHSTART1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_end1(self):
        diagtitle = COMPMODEL_SCHEND1
        modelkey = MODELKEY_SCHEND1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
#    def non_worker(self):
#        diagtitle = COMPMODEL_NONWORKER
#        modelkey = MODELKEY_NONWORKER
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
    def pre_sch(self):
        diagtitle = COMPMODEL_ARRIVALDEPARTPRESCH
        modelkey = MODELKEY_ARRIVALDEPARTPRESCH
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
#    def t_s_prism_vertices(self):
#        diagtitle = COMPMODEL_TIMESPACE
#        modelkey = MODELKEY_TIMESPACE
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        


   
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

        




 


