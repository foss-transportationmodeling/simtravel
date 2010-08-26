from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *


class Child_Model(QWidget):
    def __init__(self, parent=None, co=None):
        super(Child_Model, self).__init__(parent)
        self.setWindowTitle('Child Daily Status and Allocation Model')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
     
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        children_button = QPushButton('Children (0-17 years old)', self)
        children_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 560,200, 50)
        self.connect(children_button, SIGNAL('clicked()'), self.children)
#        self.connect(children_button, SIGNAL('clicked()'),
#                     qApp, SLOT('deleteLater()'))

        children_school_1_button = QPushButton('Children (Status \55 School)', self)
        children_school_1_button.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 480, 200, 50)
        self.connect(children_school_1_button, SIGNAL('clicked()'), self.children_school_1)

        children_preschool_1_button = QPushButton('Children (Status \55 Pre-school)', self)
        children_preschool_1_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 480, 200, 50)
        self.connect(children_preschool_1_button, SIGNAL('clicked()'), self.children_preschool_1)

        children_home_button = QPushButton('Children (Status \55 Stay home)', self)
        children_home_button.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 480, 200, 50)
        self.connect(children_home_button, SIGNAL('clicked()'), self.children_home)

        school_preschool_2_button = QPushButton('Is the child going to School \nor Pre-school today?', self)
        school_preschool_2_button.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 400, 200, 50)
        self.connect(school_preschool_2_button, SIGNAL('clicked()'), self.school_preschool_2)

        child_activity_button = QPushButton('Can the child engage in \nactivities independently?', self)
        child_activity_button.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 360, 200, 50)
        self.connect(child_activity_button, SIGNAL('clicked()'), self.child_activity)

        children_school_2_button = QPushButton('Children (Status \55 School)', self)
        children_school_2_button.setGeometry((size.width()) / 5 - 100, size.height() / 2 - 310, 200, 60)
        self.connect(children_school_2_button, SIGNAL('clicked()'), self.children_school_2)

        children_preschool_2_button = QPushButton('Children (Status \55 Pre-school)\nPick-up and Drop-off Mandatory', self)
        children_preschool_2_button.setGeometry((size.width()) * 2 / 5 - 100, size.height() / 2 - 310, 200, 60)
        self.connect(children_preschool_2_button, SIGNAL('clicked()'), self.children_preschool_2)

        in_activity_independently_button = QPushButton('Child can engage \nin activities \nindependently like \nadults', self)
        in_activity_independently_button.setGeometry((size.width()) * 3 / 5 - 100, size.height() / 2 - 280, 150, 70)
        self.connect(in_activity_independently_button, SIGNAL('clicked()'), self.in_activity_independently)

        assign_to_hhold_button = QPushButton('Assign the child to household \n(particular adult gets selected \nin the next step; working or \nnon-working adult)', self)
        assign_to_hhold_button.setGeometry((size.width()) * 4 / 5 - 150, size.height() / 2 - 280, 250, 70)
        self.connect(assign_to_hhold_button, SIGNAL('clicked()'), self.assign_to_hhold)

        travel_mode_to_school_button = QPushButton('Travel Mode to School (this \ndecision occurs in the \nActivity-travel Simulator) ', self)
        travel_mode_to_school_button.setGeometry((size.width()) / 2 - 470, size.height() / 2 - 200, 230, 50)
        self.connect(travel_mode_to_school_button, SIGNAL('clicked()'), self.travel_mode_to_school)

        travel_independently_to_school_button = QPushButton('Does the child travel \nindependently to school?', self)
        travel_independently_to_school_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 - 200, 160, 50)
        self.connect(travel_independently_to_school_button, SIGNAL('clicked()'), self.travel_independently_to_school)

        drop_off_event_button = QPushButton('Assign a drop-off event to household \n(particular adult gets selected in the \nnext step; working or non-working adult)? ', self)
        drop_off_event_button.setGeometry((size.width()) / 2 + 45, size.height() / 2 - 150, 280, 50)
        self.connect(drop_off_event_button, SIGNAL('clicked()'), self.drop_off_event)

        travel_mode_from_school_button = QPushButton('Travel Mode from School (this \ndecision occurs in the Activity-\ntravel Simulator) Constrained \nMode Choice Set based on TO Mode ', self)
        travel_mode_from_school_button.setGeometry((size.width()) / 2 - 470, size.height() / 2 - 110, 230, 70)
        self.connect(travel_mode_from_school_button, SIGNAL('clicked()'), self.travel_mode_from_school)

        travel_independently_from_school_button = QPushButton('Does the child travel \nindependently from \nschool?', self)
        travel_independently_from_school_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 - 100, 160, 50)
        self.connect(travel_independently_from_school_button, SIGNAL('clicked()'), self.travel_independently_from_school)

        pick_up_event_button = QPushButton('Assign a pick-up event to household \n(particular adult gets selected in the \nnext step; working or non-working adult)', self)
        pick_up_event_button.setGeometry((size.width()) / 2 + 45, size.height() / 2 - 50, 280, 50)
        self.connect(pick_up_event_button, SIGNAL('clicked()'), self.pick_up_event)

        generate_activity_travel_pattern_button = QPushButton('Treat the child like an adult \nand generate activity-travel \npatterns', self)
        generate_activity_travel_pattern_button.setGeometry((size.width()) / 2 - 460, size.height() / 2 + 30, 200, 50)
        self.connect(generate_activity_travel_pattern_button, SIGNAL('clicked()'), self.generate_activity_travel_pattern)

        independently_after_school_button = QPushButton('Activity pursued independently \nafter school?', self)
        independently_after_school_button.setGeometry((size.width()) / 2 - 190, size.height() / 2 + 30, 220, 50)
        self.connect(independently_after_school_button, SIGNAL('clicked()'), self.independently_after_school)

        after_school_activity_button = QPushButton('Is there time to \nengage in an after school \nCHILD activity?', self)
        after_school_activity_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 + 110, 200, 50)
        self.connect(after_school_activity_button, SIGNAL('clicked()'), self.after_school_activity)

        choice_button = QPushButton('Activity Type Choice\nDestination Choice\nActivity Duration Choice', self)
        choice_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 + 190, 200, 50)
        self.connect(choice_button, SIGNAL('clicked()'), self.choice)

        activity_with_adult_button = QPushButton('Flag the child as a dependent \nand the child engages in \nactivity with an adult \n(particular adult gets selected \nin the activity-travel \nsimulator)', self)
        activity_with_adult_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 + 270, 200, 100)
        self.connect(activity_with_adult_button, SIGNAL('clicked()'), self.activity_with_adult)

        more_activity_button = QPushButton('More activities', self)
        more_activity_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 + 400, 200, 50)
        self.connect(more_activity_button, SIGNAL('clicked()'), self.more_activity)

        return_home_button = QPushButton('Return Home', self)
        return_home_button.setGeometry((size.width()) / 2 - 180, size.height() / 2 + 480, 200, 50)
        self.connect(return_home_button, SIGNAL('clicked()'), self.return_home)

        to_adult_button = QPushButton('Move to Adult Daily Status', self)
        to_adult_button.setGeometry((size.width()) / 2 + 180, size.height() / 2 + 535, 200, 50)
        self.connect(to_adult_button, SIGNAL('clicked()'), self.to_adult)
        
        self.configob = co
        
        
    def children(self):
        diagtitle = COMPMODEL_CSCHILD017
        modelkey = MODELKEY_CSCHILD017
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def children_school_1(self):
        diagtitle = COMPMODEL_SCHDAILYSTATUS1
        modelkey = MODELKEY_SCHDAILYSTATUS1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def children_preschool_1(self):
        diagtitle = COMPMODEL_PRESCHDAILYSTATUS1
        modelkey = MODELKEY_PRESCHDAILYSTATUS1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def children_home(self):
        diagtitle = COMPMODEL_CSCHILDSTA
        modelkey = MODELKEY_CSCHILDSTA
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def school_preschool_2(self):
        diagtitle = COMPMODEL_CSSCHPRE
        modelkey = MODELKEY_CSSCHPRE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def child_activity(self):
        diagtitle = COMPMODEL_CSINDCHILD
        modelkey = MODELKEY_CSINDCHILD
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def children_school_2(self):
        diagtitle = COMPMODEL_SCHDAILYSTATUS2
        modelkey = MODELKEY_SCHDAILYSTATUS2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def children_preschool_2(self):
        diagtitle = COMPMODEL_PRESCHDAILYSTATUS2
        modelkey = MODELKEY_PRESCHDAILYSTATUS2
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def in_activity_independently(self):
        diagtitle = COMPMODEL_CSCHILDIND
        modelkey = MODELKEY_CSCHILDIND
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def assign_to_hhold(self):
        diagtitle = COMPMODEL_CSASSIGN
        modelkey = MODELKEY_CSASSIGN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def travel_mode_to_school(self):
        diagtitle = COMPMODEL_CSMODETOSCH
        modelkey = MODELKEY_CSMODETOSCH
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def travel_independently_to_school(self):
        diagtitle = COMPMODEL_SCHDAILYINDEPENDENCE
        modelkey = MODELKEY_SCHDAILYINDEPENDENCE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def drop_off_event(self):
        diagtitle = COMPMODEL_CSDROPOFF
        modelkey = MODELKEY_CSDROPOFF
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def travel_mode_from_school(self):
        diagtitle = COMPMODEL_CSMODEFROMSCH
        modelkey = MODELKEY_CSMODEFROMSCH
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def travel_independently_from_school(self):
        diagtitle = COMPMODEL_AFTSCHDAILYINDEPENDENCE
        modelkey = MODELKEY_AFTSCHDAILYINDEPENDENCE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def pick_up_event(self):
        diagtitle = COMPMODEL_CSPICKUP
        modelkey = MODELKEY_CSPICKUP
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def generate_activity_travel_pattern(self):
        diagtitle = COMPMODEL_CSTREAT
        modelkey = MODELKEY_CSTREAT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def independently_after_school(self):
        diagtitle = COMPMODEL_AFTSCHACTSTATUS
        modelkey = MODELKEY_AFTSCHACTSTATUS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def after_school_activity(self):
        diagtitle = COMPMODEL_CSISTHERE
        modelkey = MODELKEY_CSISTHERE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def choice(self):
        diagtitle = COMPMODEL_CSACTTYPE
        modelkey = MODELKEY_CSACTTYPE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def activity_with_adult(self):
        diagtitle = COMPMODEL_CSWORKSTAT
        modelkey = MODELKEY_CSWORKSTAT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def more_activity(self):
        diagtitle = COMPMODEL_CSMOREACT
        modelkey = MODELKEY_CSMOREACT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def return_home(self):
        diagtitle = COMPMODEL_CSRETURNH
        modelkey = MODELKEY_CSRETURNH
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def to_adult(self):
        diagtitle = COMPMODEL_CSMOVEADULT
        modelkey = MODELKEY_CSMOVEADULT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
        
    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 510, widgetwidth / 2, widgetheight / 2 - 415)
        line.drawLine(widgetwidth / 4, widgetheight / 2 - 495, widgetwidth / 4, widgetheight / 2 - 330)
        line.drawLine(widgetwidth * 3 / 4, widgetheight / 2 - 495, widgetwidth * 3 / 4, widgetheight / 2 - 195)  
        line.drawLine(widgetwidth / 4, widgetheight / 2 - 495, widgetwidth * 3 / 4, widgetheight / 2 - 495)
        line.drawLine(widgetwidth / 2, widgetheight / 2 - 415, widgetwidth / 4, widgetheight / 2 - 415)
        line.drawLine(widgetwidth / 4 + 100, widgetheight / 2 - 375, widgetwidth * 3 / 4, widgetheight / 2 - 375)
        line.drawLine(widgetwidth / 5, widgetheight / 2 - 330, widgetwidth / 5, widgetheight / 2 - 225)
        line.drawLine(widgetwidth * 2 / 5, widgetheight / 2 - 330, widgetwidth * 2 / 5, widgetheight / 2 - 225)
        line.drawLine(widgetwidth / 5, widgetheight / 2 - 330, widgetwidth * 2 / 5, widgetheight / 2 - 330)
        line.drawLine(widgetwidth / 5, widgetheight / 2 - 225, widgetwidth / 2 - 100, widgetheight / 2 - 225)
        line.drawLine(widgetwidth / 2 - 100, widgetheight / 2 - 200, widgetwidth / 2 - 100, widgetheight / 2 - 225)
        line.drawLine(widgetwidth / 2 - 250, widgetheight / 2 - 175, widgetwidth / 2 + 185, widgetheight / 2 - 175)
        line.drawLine(widgetwidth / 2 + 185, widgetheight / 2 - 150, widgetwidth / 2 + 185, widgetheight / 2 - 175)
        line.drawLine(widgetwidth / 2 + 50, widgetheight / 2 - 125, widgetwidth / 2 - 355, widgetheight / 2 - 125)
        line.drawLine(widgetwidth / 2 - 355, widgetheight / 2 - 150, widgetwidth / 2 - 355, widgetheight / 2 - 125)
        line.drawLine(widgetwidth / 2 - 100, widgetheight / 2 - 100, widgetwidth / 2 - 100, widgetheight / 2 - 125)
        line.drawLine(widgetwidth / 2 - 355, widgetheight / 2 - 75, widgetwidth / 2 + 185, widgetheight / 2 - 75)
        line.drawLine(widgetwidth / 2 + 185, widgetheight / 2 + 15, widgetwidth / 2 + 185, widgetheight / 2 - 75)
        line.drawLine(widgetwidth / 2 + 185, widgetheight / 2 + 15, widgetwidth / 2 - 355, widgetheight / 2 + 15)
        line.drawLine(widgetwidth / 2 - 355, widgetheight / 2 - 50, widgetwidth / 2 - 355, widgetheight / 2 + 15)
        line.drawLine(widgetwidth / 2 - 80, widgetheight / 2 + 560, widgetwidth / 2 - 80, widgetheight / 2 + 15)
        line.drawLine(widgetwidth / 2 - 360, widgetheight / 2 + 560, widgetwidth / 2 - 360, widgetheight / 2 + 80)
        line.drawLine(widgetwidth / 2 - 360, widgetheight / 2 + 560, widgetwidth / 2 + 180, widgetheight / 2 + 560)
        
        line.drawLine(widgetwidth / 2 - 80, widgetheight / 2 + 95, widgetwidth / 2 + 55, widgetheight / 2 + 95)
        line.drawLine(widgetwidth / 2 + 55, widgetheight / 2 + 95, widgetwidth / 2 + 55, widgetheight / 2 + 425)
        line.drawLine(widgetwidth / 2 + 20, widgetheight / 2 + 425, widgetwidth / 2 + 55, widgetheight / 2 + 425)
        line.drawLine(widgetwidth / 2 - 180, widgetheight / 2 + 135, widgetwidth / 2 - 215, widgetheight / 2 + 135)
        line.drawLine(widgetwidth / 2 - 215, widgetheight / 2 + 465, widgetwidth / 2 - 215, widgetheight / 2 + 135)
        line.drawLine(widgetwidth / 2 - 215, widgetheight / 2 + 465, widgetwidth / 2 - 80, widgetheight / 2 + 465)
        line.drawLine(widgetwidth / 2 - 180, widgetheight / 2 + 55, widgetwidth / 2 - 260, widgetheight / 2 + 55)

        line.drawLine(widgetwidth * 3 / 4 - 100, widgetheight / 2 - 335, widgetwidth * 3 / 5 - 25, widgetheight / 2 - 335)
        line.drawLine(widgetwidth * 3 / 5 - 25, widgetheight / 2 - 335, widgetwidth * 3 / 5 - 25, widgetheight / 2 - 195)
        line.drawLine(widgetwidth * 3 / 5 - 25, widgetheight / 2 - 195, widgetwidth * 3 / 4 + 100, widgetheight / 2 - 195)
        line.drawLine(widgetwidth * 3 / 4 + 100, widgetheight / 2 + 505, widgetwidth * 3 / 4 + 100, widgetheight / 2 - 195)
        line.drawLine(widgetwidth * 3 / 4 + 100, widgetheight / 2 + 505, widgetwidth / 2 + 120, widgetheight / 2 + 505)
        line.drawLine(widgetwidth / 2 + 120, widgetheight / 2 + 560, widgetwidth / 2 + 120, widgetheight / 2 + 505)


        line.end()



        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 480)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(widgetheight / 2 - 480)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(widgetheight / 2 - 480)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(widgetheight / 2 - 400)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3/ 4)  
        point.setY(widgetheight / 2 - 360)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(widgetheight / 2 - 280)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 5 - 25)  
        point.setY(widgetheight / 2 - 280)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 5)  
        point.setY(widgetheight / 2 - 310)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 2 / 5)  
        point.setY(widgetheight / 2 - 310)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 100)  
        point.setY(widgetheight / 2 - 200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 100)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 185)  
        point.setY(widgetheight / 2 - 150)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 185)  
        point.setY(widgetheight / 2 - 50)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 30)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 110)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 190)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 270)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 400)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 480)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4, point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 - 80)  
        point.setY(widgetheight / 2 + 560)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4, point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 180)  
        point.setY(widgetheight / 2 + 560)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))

        point.setX(widgetwidth / 2 - 260)  
        point.setY(widgetheight / 2 + 55)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        point.setX(widgetwidth / 2 - 240)  
        point.setY(widgetheight / 2 - 175)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        point.setX(widgetwidth / 2 - 240)  
        point.setY(widgetheight / 2 - 75)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 4 - 23)  
        point.setY(widgetheight / 2 - 335)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 + 27)  
        point.setY(widgetheight / 2 - 380)
        text.drawText(point, "No")

        point.setX(widgetwidth * 3 / 5 - 35)  
        point.setY(widgetheight / 2 - 340)
        text.drawText(point, "Yes")

        point.setX(widgetwidth * 3 / 4 - 20)  
        point.setY(widgetheight / 2 - 285)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 220)  
        point.setY(widgetheight / 2 - 180)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 220)  
        point.setY(widgetheight / 2 - 80)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 + 60)  
        point.setY(widgetheight / 2 - 180)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 + 60)  
        point.setY(widgetheight / 2 - 80)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 230)  
        point.setY(widgetheight / 2 + 50)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 100)  
        point.setY(widgetheight / 2 + 90)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 105)  
        point.setY(widgetheight / 2 + 173)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 100)  
        point.setY(widgetheight / 2 + 460)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 + 30)  
        point.setY(widgetheight / 2 + 437)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 + 130)
        text.drawText(point, "No")





        text.begin(self)

        


 


