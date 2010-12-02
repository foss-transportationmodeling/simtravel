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
        
        # Adult worker
        day_start1_button = QPushButton(COMPMODEL_DAYSTART, self)
        day_start1_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 370,180, 50)
        day_start1_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_start1_button, SIGNAL('clicked()'), self.day_start_aw)

        day_end1_button = QPushButton(COMPMODEL_DAYEND, self)     
        day_end1_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 290, 180, 50)
        day_end1_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_end1_button, SIGNAL('clicked()'), self.day_end_aw)
        
        num_work_episodes_button = QPushButton(COMPMODEL_WRKEPISODES, self)
        num_work_episodes_button.setGeometry((size.width()) / 2 - 405, size.height() / 2 - 210, 180, 50)
        num_work_episodes_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(num_work_episodes_button, SIGNAL('clicked()'), self.num_work)

        work_start_button = QPushButton(COMPMODEL_WORKSTART, self)
        work_start_button.setGeometry((size.width()) / 2 - 505, size.height() / 2 - 60, 180, 50)
        work_start_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_start_button, SIGNAL('clicked()'), self.work_start)

        work_end_button = QPushButton(COMPMODEL_WORKEND, self)
        work_end_button.setGeometry((size.width()) / 2 - 505, size.height() / 2 + 20, 180, 50)
        work_end_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_end_button, SIGNAL('clicked()'), self.work_end)

        work_start_1_button = QPushButton(COMPMODEL_WORKSTART1, self)
        work_start_1_button.setGeometry((size.width()) / 2 - 305, size.height() / 2 - 60, 180, 50)
        work_start_1_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_start_1_button, SIGNAL('clicked()'), self.work_start1)

        work_end_1_button = QPushButton(COMPMODEL_WORKEND1, self)
        work_end_1_button.setGeometry((size.width()) / 2 - 305, size.height() / 2 + 20, 180, 50)
        work_end_1_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_end_1_button, SIGNAL('clicked()'), self.work_end1)
        
        work_start_2_button = QPushButton(COMPMODEL_WORKSTART2, self)
        work_start_2_button.setGeometry((size.width()) / 2 - 305, size.height() / 2 + 100, 180, 50)
        work_start_2_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_start_2_button, SIGNAL('clicked()'), self.work_start2)

        work_end_2_button = QPushButton(COMPMODEL_WORKEND2, self)
        work_end_2_button.setGeometry((size.width()) / 2 - 305, size.height() / 2 + 180, 180, 50)
        work_end_2_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(work_end_2_button, SIGNAL('clicked()'), self.work_end2)
        
        
        # Adult non-worker
        day_start2_button = QPushButton(COMPMODEL_DAYSTART, self)
        day_start2_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 - 370,180, 50)
        day_start2_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_start2_button, SIGNAL('clicked()'), self.day_start_nw)
        
        day_end2_button = QPushButton(COMPMODEL_DAYEND, self)     
        day_end2_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 - 290, 180, 50)
        day_end2_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_end2_button, SIGNAL('clicked()'), self.day_end_nw)
        
        
        # Children (5 - 17)
        day_start3_button = QPushButton(COMPMODEL_DAYSTART, self)
        day_start3_button.setGeometry((size.width()) / 2 + 125, size.height() / 2 - 370,180, 50)
        day_start3_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_start3_button, SIGNAL('clicked()'), self.day_start_na)
        
        day_end3_button = QPushButton(COMPMODEL_DAYEND, self)     
        day_end3_button.setGeometry((size.width()) / 2 + 125, size.height() / 2 - 290, 180, 50)
        day_end3_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_end3_button, SIGNAL('clicked()'), self.day_end_na)

        children_arrive_button = QPushButton(COMPMODEL_SCHSTART, self)
        children_arrive_button.setGeometry((size.width()) / 2 + 125, size.height() / 2 - 210, 180, 50)
        children_arrive_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(children_arrive_button, SIGNAL('clicked()'), self.school_start)

        children_depart_button = QPushButton(COMPMODEL_SCHEND, self)
        children_depart_button.setGeometry((size.width()) / 2 + 125, size.height() / 2 - 130, 180, 50)
        children_depart_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(children_depart_button, SIGNAL('clicked()'), self.school_end)


        # Children (0 - 4)
        day_start4_button = QPushButton(COMPMODEL_DAYSTART, self)
        day_start4_button.setGeometry((size.width()) / 2 + 390, size.height() / 2 - 370,180, 50)
        day_start4_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_start4_button, SIGNAL('clicked()'), self.day_start_ps)
        
        day_end4_button = QPushButton(COMPMODEL_DAYEND, self)     
        day_end4_button.setGeometry((size.width()) / 2 + 390, size.height() / 2 - 290, 180, 50)
        day_end4_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(day_end4_button, SIGNAL('clicked()'), self.day_end_ps)

        presch_arrive_button = QPushButton(COMPMODEL_PRESCHSTART, self)
        presch_arrive_button.setGeometry((size.width()) / 2 + 390, size.height() / 2 - 210, 180, 50)
        presch_arrive_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(presch_arrive_button, SIGNAL('clicked()'), self.preschool_start)

        presch_depart_button = QPushButton(COMPMODEL_PRESCHEND, self)
        presch_depart_button.setGeometry((size.width()) / 2 + 390, size.height() / 2 - 130, 180, 50)
        presch_depart_button.setStyleSheet("background-color: #FFFDD0")
        self.connect(presch_depart_button, SIGNAL('clicked()'), self.preschool_end)

        
        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
        
        self.configob = co
  
    def day_start_aw(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_AW
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_start_nw(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_AN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_start_na(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_NA
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_start_ps(self):
        diagtitle = COMPMODEL_DAYSTART
        modelkey = MODELKEY_DAYSTART_PS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def day_end_aw(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_AW
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_end_nw(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_NW
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_end_na(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_NA
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def day_end_ps(self):
        diagtitle = COMPMODEL_DAYEND
        modelkey = MODELKEY_DAYEND_PS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def num_work(self):
        diagtitle = COMPMODEL_WRKEPISODES
        modelkey = MODELKEY_WRKEPISODES
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        

    def work_start(self):
        diagtitle = COMPMODEL_WORKSTART
        modelkey = MODELKEY_WORKSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def work_end(self):
        diagtitle = COMPMODEL_WORKEND
        modelkey = MODELKEY_WORKEND
        
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
        

    def work_start2(self):
        diagtitle = COMPMODEL_WORKSTART2
        modelkey = MODELKEY_WORKSTART2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def work_end2(self):
        diagtitle = COMPMODEL_WORKEND2
        modelkey = MODELKEY_WORKEND2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_start(self):
        diagtitle = COMPMODEL_SCHSTART
        modelkey = MODELKEY_SCHSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_end(self):
        diagtitle = COMPMODEL_SCHEND
        modelkey = MODELKEY_SCHEND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
#    def non_worker(self):
#        diagtitle = COMPMODEL_NONWORKER
#        modelkey = MODELKEY_NONWORKER
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
#    def pre_sch(self):
#        diagtitle = COMPMODEL_ARRIVALDEPARTPRESCH
#        modelkey = MODELKEY_ARRIVALDEPARTPRESCH
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
    def preschool_start(self):
        diagtitle = COMPMODEL_PRESCHSTART
        modelkey = MODELKEY_PRESCHSTART
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def preschool_end(self):
        diagtitle = COMPMODEL_PRESCHEND
        modelkey = MODELKEY_PRESCHEND
        
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

        line.drawLine(widgetwidth / 2 - 315, widgetheight / 2 - 400, widgetwidth / 2 - 315, widgetheight / 2 - 120)
        line.drawLine(widgetwidth / 2 - 415, widgetheight / 2 - 120, widgetwidth / 2 - 415, widgetheight / 2 + 40)
        line.drawLine(widgetwidth / 2 - 215, widgetheight / 2 - 120, widgetwidth / 2 - 215, widgetheight / 2 + 200)
        line.drawLine(widgetwidth / 2 - 415, widgetheight / 2 - 120, widgetwidth / 2 - 215, widgetheight / 2 - 120)
        
        line.drawLine(widgetwidth / 2 - 50, widgetheight / 2 - 400, widgetwidth / 2 - 50, widgetheight / 2 - 290)
        line.drawLine(widgetwidth / 2 + 215, widgetheight / 2 - 400, widgetwidth / 2 + 215, widgetheight / 2 - 100)
        line.drawLine(widgetwidth / 2 + 480, widgetheight / 2 - 400, widgetwidth / 2 + 480, widgetheight / 2 - 100)

                
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()


        # Adult Workers Arrow
        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 - 370)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 - 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 315)  
        point.setY(widgetheight / 2 - 210)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 415)  
        point.setY(widgetheight / 2 - 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 415)  
        point.setY(widgetheight / 2 + 20)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 215)  
        point.setY(widgetheight / 2 - 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 215)  
        point.setY(widgetheight / 2 + 20)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 215)  
        point.setY(widgetheight / 2 + 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 215)  
        point.setY(widgetheight / 2 + 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        

        # Adult Non-workers Arrow
        point.setX(widgetwidth / 2 - 50)  
        point.setY(widgetheight / 2 - 370)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 50)  
        point.setY(widgetheight / 2 - 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        # Non-adults
        point.setX(widgetwidth / 2 + 215)  
        point.setY(widgetheight / 2 - 370)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 215)  
        point.setY(widgetheight / 2 - 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 215)  
        point.setY(widgetheight / 2 - 210)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 215)  
        point.setY(widgetheight / 2 - 130)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        # Non-adults
        point.setX(widgetwidth / 2 + 480)  
        point.setY(widgetheight / 2 - 370)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 480)  
        point.setY(widgetheight / 2 - 290)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 480)  
        point.setY(widgetheight / 2 - 210)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 480)  
        point.setY(widgetheight / 2 - 130)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.setBrush(QColor("#1e90ff"))
        #arrow.setOpacity(0.7)
        arrow.drawRoundedRect(widgetwidth/2 - 405, widgetheight/2 - 450, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 - 140, widgetheight/2 - 450, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 125, widgetheight/2 - 450, 180, 50, 15.0, 15.0)
        arrow.drawRoundedRect(widgetwidth/2 + 390, widgetheight/2 - 450, 178, 50, 15.0, 15.0)
        arrow.setBrush(QColor("#F0F0F0"))
        arrow.drawRoundedRect(widgetwidth/2 + 150, widgetheight/2 + 180, 350, 50, 15.0, 15.0)
        
        arrow.end()


        text = QPainter()
        text.begin(self)
        point = QPoint()
        
        point.setX(widgetwidth / 2 - 415)  
        point.setY(widgetheight / 2 - 125)
        text.drawText(point, "One")

        point.setX(widgetwidth / 2 - 230)  
        point.setY(widgetheight / 2 - 125)
        text.drawText(point, "Two")
        
        temp = QRect(widgetwidth/2 - 405, widgetheight/2 - 450, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Adult Workers')
        
        temp = QRect(widgetwidth/2 - 140, widgetheight/2 - 450, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Adult Non-workers')

        temp = QRect(widgetwidth/2 + 125, widgetheight/2 - 450, 180, 50)
        text.drawText(temp, Qt.AlignCenter, 'Children (5-17 years)')

        temp = QRect(widgetwidth/2 + 390, widgetheight/2 - 450, 178, 50)
        text.drawText(temp, Qt.AlignCenter, 'Preschool Children\n(0-4 years)')
        
        temp = QRect(widgetwidth/2 + 150, widgetheight/2 + 180, 350, 50)
        text.drawText(temp, Qt.AlignCenter, 'Time-space Prism Vertices for the Population')

        text.end()


        
