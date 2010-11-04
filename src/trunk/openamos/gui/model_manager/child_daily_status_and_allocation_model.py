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
        
        children_button = QPushButton('Children\n(5-17 years)', self)
        children_button.setGeometry((size.width()) / 2 - 120, size.height() / 2 - 560, 160, 50)
#        self.connect(children_button, SIGNAL('clicked()'), self.children)
#        self.connect(children_button, SIGNAL('clicked()'),
#                     qApp, SLOT('deleteLater()'))

        goto_school_button = QPushButton('Child goes to\nschool on\ntravel day', self)
        goto_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 460, 120, 75)
        self.connect(goto_school_button, SIGNAL('clicked()'), self.goto_school)
        
        independent_to_school_button = QPushButton('Child travels to\nschool\nindependently', self)
        independent_to_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 360, 120, 75)
        self.connect(independent_to_school_button, SIGNAL('clicked()'), self.travel_independently_to_school)
        
        drop_off_school1_button = QPushButton('Assign an adult drop-off event to\nhousehold', self)
        drop_off_school1_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 - 235, 200, 50)
        self.connect(drop_off_school1_button, SIGNAL('clicked()'), self.drop_off_event)
        
        independent_from_school_button = QPushButton('Child\nindependent\nafter-school', self)
        independent_from_school_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 135, 120, 75)
        self.connect(independent_from_school_button, SIGNAL('clicked()'), self.independently_after_school)
        
        after_school_activity_button = QPushButton('Is there time to\nengage in an\nafter school\nchild activity?', self)
        after_school_activity_button.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 35, 120, 75)
        self.connect(after_school_activity_button, SIGNAL('clicked()'), self.after_school_activity)
        
        activity_type_button = QPushButton('After-school activity type choice', self)
        activity_type_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 90, 200, 50)
        self.connect(activity_type_button, SIGNAL('clicked()'), self.choice)
        
        destination_button = QPushButton('After-school activity\ndestination choice', self)
        destination_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 170, 200, 50)
        self.connect(destination_button, SIGNAL('clicked()'), self.choice)
        
        duration_button = QPushButton('After-school activity\nduration model', self)
        duration_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 250, 200, 50)
        self.connect(duration_button, SIGNAL('clicked()'), self.choice)
        
        drop_off_school2_button = QPushButton('Assign an adult drop-off event to\nhousehold', self)
        drop_off_school2_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 330, 200, 50)
        self.connect(drop_off_school2_button, SIGNAL('clicked()'), self.drop_off_event)
        
        activity_with_adult_button = QPushButton('Adult stays with child for\nactivity', self)
        activity_with_adult_button.setGeometry((size.width()) / 2 - 140, size.height() / 2 + 410, 200, 50)
        self.connect(activity_with_adult_button, SIGNAL('clicked()'), self.activity_with_adult)
        
        
        
        in_activity_independently_button = QPushButton('Child is\nindependent', self)
        in_activity_independently_button.setGeometry((size.width()) / 2 - 340, size.height() / 2 - 460, 120, 75)
        self.connect(in_activity_independently_button, SIGNAL('clicked()'), self.child_independent)
        
        assign_hh_button = QPushButton('Assign an adult stay-\nhome event to household', self)
        assign_hh_button.setGeometry((size.width()) / 2 - 500, size.height() / 2 - 360, 200, 50)
        self.connect(assign_hh_button, SIGNAL('clicked()'), self.assign_hh)

        generate_travel_pattern_button = QPushButton('Simulate activity\ntravel patterns for\nchild dynamically', self)
        generate_travel_pattern_button.setGeometry((size.width()) / 2 - 360, size.height() / 2 - 280, 160, 50)
        self.connect(generate_travel_pattern_button, SIGNAL('clicked()'), self.generate_travel_pattern)
        
        travel_mode_school_button = QPushButton('Simulate mode\nchoice dynamically', self)
        travel_mode_school_button.setGeometry((size.width()) / 2 - 360, size.height() / 2 - 123, 160, 50)
        self.connect(travel_mode_school_button, SIGNAL('clicked()'), self.travel_mode_school)
        
        pick_up_school_button = QPushButton('Assign an adult pick-up event to\nhousehold', self)
        pick_up_school_button.setGeometry((size.width()) / 2 - 380, size.height() / 2 - 23, 200, 50)
        self.connect(pick_up_school_button, SIGNAL('clicked()'), self.pick_up_event)
        
        return_home_button = QPushButton('Return home', self)
        return_home_button.setGeometry((size.width()) / 2 - 360, size.height() / 2 + 57, 160, 50)
        self.connect(return_home_button, SIGNAL('clicked()'), self.return_home)        
 
        
        # Pre-school Children
        preschool_button = QPushButton('Pre-school Children\n(0-4 years)', self)
        preschool_button.setGeometry((size.width()) / 2 + 140, size.height() / 2 - 560, 160, 50)
        #self.connect(preschool_button, SIGNAL('clicked()'), self.preschool)
        
        goto_preschool_button = QPushButton('Child goes to\npre-school on\n travel day', self)
        goto_preschool_button.setGeometry((size.width()) / 2 + 160, size.height() / 2 - 460, 120, 75)
        self.connect(goto_preschool_button, SIGNAL('clicked()'), self.goto_preschool)
        
        assign_preschool_hh_button = QPushButton('Assign an adult stay-\nhome event to household', self)
        assign_preschool_hh_button.setGeometry((size.width()) / 2 + 360, size.height() / 2 - 448, 160, 50)
        self.connect(assign_preschool_hh_button, SIGNAL('clicked()'), self.assign_preschool_hh)
        
        drop_off_preschool_button = QPushButton('Assign an adult drop-off event to\nhousehold', self)
        drop_off_preschool_button.setGeometry((size.width()) / 2 + 130, size.height() / 2 - 335, 180, 50)
        self.connect(drop_off_preschool_button, SIGNAL('clicked()'), self.drop_off_event)
        
        pick_up_preschool_button = QPushButton('Assign an adult pick-up event to \nhousehold', self)
        pick_up_preschool_button.setGeometry((size.width()) / 2 + 130, size.height() / 2 - 255, 180, 50)
        self.connect(pick_up_preschool_button, SIGNAL('clicked()'), self.pick_up_event)
        
        Dummy  = QPushButton('', self)
        Dummy.setGeometry(0, size.height() - 4, 1140, 2)
        
        self.configob = co
        
        

        
    def goto_school(self):
        diagtitle = COMPMODEL_SCHDAILYSTATUS1
        modelkey = MODELKEY_SCHDAILYSTATUS1
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def goto_preschool(self):
        diagtitle = COMPMODEL_CSSCHPRE
        modelkey = MODELKEY_CSSCHPRE
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    def child_independent(self):
        diagtitle = COMPMODEL_CSINDCHILD
        modelkey = MODELKEY_CSINDCHILD
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def assign_hh(self):
        diagtitle = COMPMODEL_CSASSIGN
        modelkey = MODELKEY_CSASSIGN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
    
        
    def assign_preschool_hh(self):
        diagtitle = COMPMODEL_CSASSIGN
        modelkey = MODELKEY_CSASSIGN
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def travel_mode_school(self):
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
        
        
    def pick_up_event(self):
        diagtitle = COMPMODEL_CSPICKUP
        modelkey = MODELKEY_CSPICKUP
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
    
    def generate_travel_pattern(self):
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
        
        
    def return_home(self):
        diagtitle = COMPMODEL_CSRETURNH
        modelkey = MODELKEY_CSRETURNH
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()



#    def children(self):
#        diagtitle = COMPMODEL_CSCHILD017
#        modelkey = MODELKEY_CSCHILD017
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()

    
#    def children_preschool_1(self):
#        diagtitle = COMPMODEL_PRESCHDAILYSTATUS1
#        modelkey = MODELKEY_PRESCHDAILYSTATUS1
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()

  
#    def children_home(self):
#        diagtitle = COMPMODEL_CSCHILDSTA
#        modelkey = MODELKEY_CSCHILDSTA
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
#    def children_school_2(self):
#        diagtitle = COMPMODEL_SCHDAILYSTATUS2
#        modelkey = MODELKEY_SCHDAILYSTATUS2
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
    
#    def children_preschool_2(self):
#        diagtitle = COMPMODEL_PRESCHDAILYSTATUS2
#        modelkey = MODELKEY_PRESCHDAILYSTATUS2
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
        
#    def in_activity_independently(self):
#        diagtitle = COMPMODEL_CSCHILDIND
#        modelkey = MODELKEY_CSCHILDIND
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()


#    def more_activity(self):
#        diagtitle = COMPMODEL_CSMOREACT
#        modelkey = MODELKEY_CSMOREACT
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
    
#    def to_adult(self):
#        diagtitle = COMPMODEL_CSMOVEADULT
#        modelkey = MODELKEY_CSMOVEADULT
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
        
    
#    def travel_independently_from_school(self):
#        diagtitle = COMPMODEL_AFTSCHDAILYINDEPENDENCE
#        modelkey = MODELKEY_AFTSCHDAILYINDEPENDENCE
#        
#        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
#        diag.exec_()
 
        
    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)

        # Children (5-17 years)
        line.drawLine(widgetwidth / 2 - 40, widgetheight / 2 - 520, widgetwidth / 2 - 40, widgetheight / 2 + 420)
        line.drawLine(widgetwidth / 2 - 280, widgetheight / 2 - 400, widgetwidth / 2 - 280, widgetheight / 2 - 270)
        line.drawLine(widgetwidth / 2 - 280, widgetheight / 2 - 3, widgetwidth / 2 - 280, widgetheight / 2 + 67)
        
        line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 - 423, widgetwidth / 2 - 90, widgetheight / 2 - 423)
        line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 - 98, widgetwidth / 2 - 90, widgetheight / 2 - 98)
        line.drawLine(widgetwidth / 2 - 230, widgetheight / 2 + 3, widgetwidth / 2 - 90, widgetheight / 2 + 3)
        
        line.drawLine(widgetwidth / 2 - 330, widgetheight / 2 - 423, widgetwidth / 2 - 400, widgetheight / 2 - 423)
        line.drawLine(widgetwidth / 2 - 400, widgetheight / 2 - 423, widgetwidth / 2 - 400, widgetheight / 2 - 350)
        
        line.drawLine(widgetwidth / 2 - 350, widgetheight / 2 - 255, widgetwidth / 2 - 400, widgetheight / 2 - 255)
        line.drawLine(widgetwidth / 2 - 400, widgetheight / 2 - 255, widgetwidth / 2 - 400, widgetheight / 2 - 98)
        line.drawLine(widgetwidth / 2 - 350, widgetheight / 2 - 98, widgetwidth / 2 - 400, widgetheight / 2 - 98)

        line.drawLine(widgetwidth / 2 - 90, widgetheight / 2 - 323, widgetwidth / 2 - 170, widgetheight / 2 - 323)
        line.drawLine(widgetwidth / 2 - 170, widgetheight / 2 - 323, widgetwidth / 2 - 170, widgetheight / 2 - 98)
        
        line.drawLine(widgetwidth / 2 - 50, widgetheight / 2 - 98, widgetwidth / 2 + 90, widgetheight / 2 - 98)
        line.drawLine(widgetwidth / 2 + 90, widgetheight / 2 - 98, widgetwidth / 2 + 90, widgetheight / 2 + 435)
        line.drawLine(widgetwidth / 2 + 30, widgetheight / 2 + 435, widgetwidth / 2 + 90, widgetheight / 2 + 435)
        
        # Pre-school Children
        line.drawLine(widgetwidth / 2 + 220, widgetheight / 2 - 520, widgetwidth / 2 + 220, widgetheight / 2 - 245)
        line.drawLine(widgetwidth / 2 + 270, widgetheight / 2 - 423, widgetwidth / 2 + 370, widgetheight / 2 - 423)

        line.end()



        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 - 460)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 - 360)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 - 235)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 - 135)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 - 35)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 + 90)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 + 170)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 + 250)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 + 330)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 40)  
        point.setY(widgetheight / 2 + 410)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 280)  
        point.setY(widgetheight / 2 - 280)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 280)  
        point.setY(widgetheight / 2 + 57)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 - 400)  
        point.setY(widgetheight / 2 - 360)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        # Arrow for west
        point.setX(widgetwidth / 2 - 220)  
        point.setY(widgetheight / 2 - 423)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))
        
        point.setX(widgetwidth / 2 - 200)  
        point.setY(widgetheight / 2 - 98)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))

        point.setX(widgetwidth / 2 - 180)  
        point.setY(widgetheight / 2 + 3)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))
        
        point.setX(widgetwidth / 2 + 20)  
        point.setY(widgetheight / 2 - 98)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13,point.y() + 4))
        
        # Arrow for east
        point.setX(widgetwidth / 2 - 360)  
        point.setY(widgetheight / 2 - 255)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))


        
        # Pre-school Children (0-4 years)
        point.setX(widgetwidth / 2 + 220)  
        point.setY(widgetheight / 2 - 460)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 220)  
        point.setY(widgetheight / 2 - 335)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2 + 220)  
        point.setY(widgetheight / 2 - 255)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))
        
        point.setX(widgetwidth / 2 + 360)  
        point.setY(widgetheight / 2 - 423)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13, point.y() - 4), QPoint(point.x() - 13, point.y() + 4))
        

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2 - 60)  
        point.setY(widgetheight / 2 - 375)
        text.drawText(point, "Yes")
        
        point.setX(widgetwidth / 2 - 160)  
        point.setY(widgetheight / 2 - 428)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 275)  
        point.setY(widgetheight / 2 - 330)
        text.drawText(point, "Yes")
        
        point.setX(widgetwidth / 2 - 400)  
        point.setY(widgetheight / 2 - 428)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 170)  
        point.setY(widgetheight / 2 - 328)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 57)  
        point.setY(widgetheight / 2 - 260)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 150)  
        point.setY(widgetheight / 2 - 103)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 57)  
        point.setY(widgetheight / 2 - 50)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 60)  
        point.setY(widgetheight / 2 + 65)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 - 140)  
        point.setY(widgetheight / 2 - 2)
        text.drawText(point, "No")
        
#
#        point.setX(widgetwidth / 2 - 105)  
#        point.setY(widgetheight / 2 + 173)
#        text.drawText(point, "Yes")
#
#        point.setX(widgetwidth / 2 - 100)  
#        point.setY(widgetheight / 2 + 460)
#        text.drawText(point, "No")

        # Pre-school Children
        point.setX(widgetwidth / 2 + 200)  
        point.setY(widgetheight / 2 - 360)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 2 + 310)  
        point.setY(widgetheight / 2 - 428)
        text.drawText(point, "No")





        text.begin(self)

        


 


