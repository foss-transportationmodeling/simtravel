from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Activity_Travel_Pattern_Simulator(QWidget):
    def __init__(self, parent=None):
        super(Activity_Travel_Pattern_Simulator, self).__init__(parent)
        self.setWindowTitle('Activity Travel Pattern Simulator')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
     
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        time_slice_button = QPushButton('Within a time slice', self)
        time_slice_button.setGeometry(size.width() / 2 - 100, 40, 200, 50)

        children_button = QPushButton('Children with after school \ndependent activities', self)
        children_button.setGeometry((size.width()) * 3 / 4 - 100, 120, 200, 50)

        activity_pursued_1_button = QPushButton('Can activity be pursued \njointly (Spatial and Temporal \nfeasibility) with a Household \nmember?', self)
        activity_pursued_1_button.setGeometry((size.width()) * 3 / 4 - 100, 200, 200, 70)

        assign_to_non_hhold_button = QPushButton('Activity assigned to a \nNon-household member \ncomprising Joint Activity with \nNon-household member', self)
        assign_to_non_hhold_button.setGeometry((size.width()) * 3 / 4 + 50, 300, 200, 70)

        assign_to_hhold_button = QPushButton('Assign the activity to \nHousehold member comprising\nJoint Activity with \nhousehold member', self)
        assign_to_hhold_button.setGeometry((size.width()) * 3 / 4 - 250, 300, 200, 70)

        mode_choice_model_button = QPushButton('Mode choice model for \nintra-household joint \ntrips with children', self)
        mode_choice_model_button.setGeometry((size.width()) * 3 / 4 - 250, 400, 200, 50)



       
        all_other_individuals_button = QPushButton('All other individuals', self)
        all_other_individuals_button.setGeometry((size.width()) / 4 - 100, 120, 200, 50)

        adult_individuals_button = QPushButton('Adult individuals, children \nwith independent activities \n(if children stay at home then \nthey shadow the activity-travel \npatterns of adult to whom \nthey are assigned)', self)
        adult_individuals_button.setGeometry((size.width()) / 4 - 100, 200, 200, 100)       

        travel_time_button = QPushButton('Is travel time to next \nfixed activity \74 time \navailable in the prism?', self)
        travel_time_button.setGeometry((size.width()) / 4 - 100, 330, 200, 50)

        activity_choice_button = QPushButton('Activity Type Choice\nMode-Destination Choice; mode-\ndestination choices are limited \nby the TSP and travel time to \nnext fixed activity\nActivity Duration Choice', self)
        activity_choice_button.setGeometry((size.width()) / 4 - 250, 410, 200, 100)

        actual_start_time_button = QPushButton('Actual start time \nfor the activity', self)
        actual_start_time_button.setGeometry((size.width()) / 4 - 250, 540, 200, 50)

        time_in_activity_button = QPushButton('Is there enough time to \nengage in the activity?', self)
        time_in_activity_button.setGeometry((size.width()) / 4 - 250, 620, 200, 50)

        proceed_next_activity_button = QPushButton('Proceed to next \nfixed activity', self)
        proceed_next_activity_button.setGeometry((size.width()) / 4 + 50, 620, 200, 50)

        mode_choice_next_activity_button = QPushButton('Mode Choice to the \nnext fixed activity', self)
        mode_choice_next_activity_button.setGeometry((size.width()) / 4 + 50, 700, 200, 50)

        hov_button = QPushButton('Is the mode of \nthe trip HOV?', self)
        hov_button.setGeometry((size.width()) / 4 - 250, 790, 200, 50)

        activity_pursued_2_button = QPushButton('Can activity be pursued \njointly (Spatial and Temporal \nfeasibility) with Household \nmembers?', self)
        activity_pursued_2_button.setGeometry((size.width()) / 4 + 50, 780, 200, 70)

        check_if_join_activity_button = QPushButton('For each available household \nmember, check to see if \nhe/she will join the activity?', self)
        check_if_join_activity_button.setGeometry((size.width()) / 4 + 350, 780, 200, 70)

        activity_non_hhold_button = QPushButton('Joint Activity with \nNon-household member', self)
        activity_non_hhold_button.setGeometry((size.width()) / 4 + 50, 880, 200, 50)

        activity_hhold_button = QPushButton('Joint Activity with \nhousehold member', self)
        activity_hhold_button.setGeometry((size.width()) / 4 + 350, 880, 200, 50)

        sov_hov_button = QPushButton('If mode is SOV or HOV Driver identify \nvehicle (for only trips where household \nmember is the driver) ', self)
        sov_hov_button.setGeometry((size.width()) / 2 - 150, 990, 300, 50)

        activity_travel_pattern_button = QPushButton('Activity-travel patterns for \nall individuals within the time-slice', self)
        activity_travel_pattern_button.setGeometry((size.width()) / 2 - 150, 1070, 300, 50)



    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 4, 105, widgetwidth * 3 / 4, 105)
        line.drawLine(widgetwidth / 2, 90, widgetwidth / 2, 105)
        line.drawLine(widgetwidth / 4, 105, widgetwidth / 4, 330)
        line.drawLine(widgetwidth * 3 / 4, 105, widgetwidth * 3 / 4, 200)
        line.drawLine(widgetwidth * 3 / 4 - 150, 235, widgetwidth * 3 / 4 + 150, 235)
        line.drawLine(widgetwidth * 3 / 4 - 150, 235, widgetwidth * 3 / 4 - 150, 480)
        line.drawLine(widgetwidth * 3 / 4 - 150, 480, widgetwidth * 3 / 4 + 150, 480)
        line.drawLine(widgetwidth * 3 / 4 + 150, 235, widgetwidth * 3 / 4 + 150, 960)

        line.drawLine(widgetwidth / 4 + 150, 355, widgetwidth / 4 - 150, 355)
        line.drawLine(widgetwidth / 4 + 150, 355, widgetwidth / 4 - 150, 355)
        line.drawLine(widgetwidth / 4 - 150, 355, widgetwidth / 4 - 150, 960)
        line.drawLine(widgetwidth / 4 + 150, 355, widgetwidth / 4 + 150, 770)
        line.drawLine(widgetwidth / 4 - 150, 770, widgetwidth / 4 + 150, 770)
        line.drawLine(widgetwidth / 4 - 150, 645, widgetwidth / 4 + 150, 645)
        line.drawLine(widgetwidth / 4 - 150, 960, widgetwidth * 3 / 4 + 150, 960)
        line.drawLine(widgetwidth / 4 - 150, 815, widgetwidth / 4 + 600, 815)
        line.drawLine(widgetwidth / 4 + 600, 815, widgetwidth / 4 + 600, 905)
        line.drawLine(widgetwidth / 4 + 550, 905, widgetwidth / 4 + 600, 905)
        line.drawLine(widgetwidth / 4 + 150, 850, widgetwidth / 4 + 150, 960)
        line.drawLine(widgetwidth / 4 + 450, 930, widgetwidth / 4 + 450, 960)
        line.drawLine(widgetwidth / 4 + 450, 850, widgetwidth / 4 + 450, 865)
        line.drawLine(widgetwidth / 4 + 150, 865, widgetwidth / 4 + 450, 865)
        line.drawLine(widgetwidth / 2, 960, widgetwidth / 2, 1070)

        
        line.end()




        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 4)  
        point.setY(120)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3/ 4)  
        point.setY(120)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(200)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(330)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 - 150)  
        point.setY(410)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 - 150)  
        point.setY(540)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 - 150)  
        point.setY(620)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 - 150)  
        point.setY(790)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

 
        point.setX(widgetwidth / 4 + 150)  
        point.setY(620)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 + 150)  
        point.setY(700)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4 - 150)  
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4 + 150)  
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4 - 150)  
        point.setY(400)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 + 150)  
        point.setY(880)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4 + 550)  
        point.setY(905)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() + 13, point.y() - 4), QPoint(point.x() + 13, point.y() + 4))

        point.setX(widgetwidth / 4 + 50)  
        point.setY(815)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13,point.y() - 4), QPoint(point.x() - 13,point.y() + 4))

        point.setX(widgetwidth / 4 + 350)  
        point.setY(815)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 13,point.y() - 4), QPoint(point.x() - 13,point.y() + 4))

        point.setX(widgetwidth / 2)  
        point.setY(990)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(1070)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth * 3 / 4 - 160)  
        point.setY(230)
        text.drawText(point, "Yes")

        point.setX(widgetwidth * 3 / 4 + 145)  
        point.setY(230)
        text.drawText(point, "No")

        point.setX(widgetwidth / 4 - 160)  
        point.setY(350)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 4 + 145)  
        point.setY(350)
        text.drawText(point, "No")

        point.setX(widgetwidth / 4 - 5)  
        point.setY(640)
        text.drawText(point, "No")

        point.setX(widgetwidth / 4 - 175)  
        point.setY(725)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 4 - 7)  
        point.setY(810)
        text.drawText(point, "HOV")

        point.setX(widgetwidth / 4 + 293)  
        point.setY(810)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 4 + 295)  
        point.setY(860)
        text.drawText(point, "No")

        point.setX(widgetwidth / 4 + 135)  
        point.setY(860)
        text.drawText(point, "No")

        point.setX(widgetwidth / 4 + 605)  
        point.setY(865)
        text.drawText(point, "Yes")

        

        point.setX(widgetwidth / 4 - 200)  
        point.setY(890)
        text.drawText(point, "SOV \53")

        point.setX(widgetwidth / 4 - 220)  
        point.setY(905)
        text.drawText(point, "Other Modes")


        text.begin(self)

        


 


