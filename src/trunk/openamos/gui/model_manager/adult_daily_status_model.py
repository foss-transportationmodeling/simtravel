from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Adult_Model(QWidget):
    def __init__(self, parent=None):
        super(Adult_Model, self).__init__(parent)
        self.setWindowTitle('Adult Daily Status Model')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
     
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        children_assigned_button = QPushButton('Is a dependent child/children assigned \nto household including stay home and \nchauffeuring activities?', self)
        children_assigned_button.setGeometry((size.width()) / 2 - 150, 40, 300, 60)

        children_stay_home_button = QPushButton('Child/Children with staying \nhome activities', self)
        children_stay_home_button.setGeometry((size.width()) / 2 - 100, 140, 200, 50)
       
        children_chauffeuring_button = QPushButton('Child/Children with \nchauffeuring activities', self)
        children_chauffeuring_button.setGeometry((size.width()) * 3 / 4 - 100, 140, 200, 50)
       
        nonworking_adult_button = QPushButton('Households with at least \none non-working adult', self)
        nonworking_adult_button.setGeometry((size.width()) / 2 - 100, 220, 200, 50)
       
        all_working_adult_button = QPushButton('Households with all \nworking adults', self)
        all_working_adult_button.setGeometry((size.width()) / 4 - 100, 220, 200, 50)

        assign_children_3_button = QPushButton('Assign each dependent child \nto a household adult subject \nto the fixed activity \nschedule of the adult', self)
        assign_children_3_button.setGeometry((size.width()) * 3 / 4 - 100, 220, 200, 80)

        assign_children_1_button = QPushButton('Assign all dependent \nchildren to a working adult', self)
        assign_children_1_button.setGeometry((size.width()) / 4 - 100, 300, 200, 50)

        assign_children_2_button = QPushButton('Assign all dependent \nchildren to one \nnon-working adult', self)
        assign_children_2_button.setGeometry((size.width()) / 2 - 100, 300, 200, 50)

        adult_work_button = QPushButton('This adult works from home', self)
        adult_work_button.setGeometry((size.width()) / 4 - 100, 380, 200, 50)

        check_adult_button = QPushButton('For all other adults, \ncheck to see if the \nadult is worker?', self)
        check_adult_button.setGeometry((size.width()) / 2 - 100, 470, 200, 50)

        work_today_button = QPushButton('Is an employed adult \ngoing to work today?', self)
        work_today_button.setGeometry((size.width()) / 4 - 100, 550, 200, 50)

        work_from_home_button = QPushButton('Work from home', self)
        work_from_home_button.setGeometry((size.width()) / 4 - 100, 630, 200, 50)

        go_to_work_button = QPushButton('Go to Work', self)
        go_to_work_button.setGeometry((size.width()) / 2 - 100, 630, 200, 50)

        no_work_episodes_button = QPushButton('No Work Episodes', self)
        no_work_episodes_button.setGeometry((size.width()) * 3 / 4 - 100, 630, 200, 50)



    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine(widgetwidth / 2, 100, widgetwidth / 2, 470)
        line.drawLine(widgetwidth / 2, 120, widgetwidth * 3 / 4, 120)
        line.drawLine(widgetwidth * 3 / 4, 120, widgetwidth * 3 / 4, 450)
        line.drawLine(widgetwidth / 4 - 200, 450, widgetwidth * 3 / 4, 450)
        line.drawLine(widgetwidth / 4 - 200, 450, widgetwidth / 4 - 200, 70)
        line.drawLine(widgetwidth / 2, 70, widgetwidth / 4 - 200, 70)
        line.drawLine(widgetwidth / 2, 205, widgetwidth / 4, 205)
        line.drawLine(widgetwidth / 4, 450, widgetwidth / 4, 205)
        line.drawLine(widgetwidth * 3 / 4, 495, widgetwidth / 4, 495)
        line.drawLine(widgetwidth / 4, 630, widgetwidth / 4, 495)
        line.drawLine(widgetwidth * 3 / 4, 630, widgetwidth * 3 / 4, 495)
        line.drawLine(widgetwidth / 4, 575, widgetwidth / 2, 575)
        line.drawLine(widgetwidth / 2, 630, widgetwidth / 2, 575)
        line.end()



        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2)  
        point.setY(140)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3/ 4)  
        point.setY(140)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(220)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(300)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(380)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(470)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

 
        point.setX(widgetwidth / 4)  
        point.setY(550)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 4)  
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth * 3 / 4)  
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(630)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        arrow.end()

        # Drawing text
        text = QPainter()
        text.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 4 - 40)  
        point.setY(65)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 20)  
        point.setY(115)
        text.drawText(point, "Yes")

        point.setX(widgetwidth / 4 - 20)  
        point.setY(490)
        text.drawText(point, "Worker")

        point.setX(widgetwidth * 3 / 4 - 30)  
        point.setY(490)
        text.drawText(point, "Non-Worker")

        point.setX(widgetwidth / 4 - 15)  
        point.setY(615)
        text.drawText(point, "No")

        point.setX(widgetwidth / 2 - 110)  
        point.setY(570)
        text.drawText(point, "Yes")


        text.begin(self)

        


 


