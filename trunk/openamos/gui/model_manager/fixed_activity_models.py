# -*- coding: cp936 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class FixedActivityModels(QWidget):
    def __init__(self, parent=None):
        super(FixedActivityModels, self).__init__(parent)
        
        self.setWindowTitle('Fixed Activity Location Choice Generator')
        size =  parent.geometry()
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        workersbutton = QPushButton('Workers', self)
        workersbutton.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 280,200, 50)
        #self.connect(workersbutton, SIGNAL('clicked()'), qApp, SLOT('Close()'))
        
        childrenadultbutton = QPushButton("Children (Status-School) \n+ Adult (Status-School)", self)     
        childrenadultbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 280, 200, 50)

        
        childrenbutton = QPushButton('Children \n(Status-Preschool)', self)
        childrenbutton.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 280, 200, 50)


        worklocbutton = QPushButton('For each job identify \na primary work location;\n\n\nDuring simulation, \ngenerate Choice Sets \nconditional on the home \nlocation e.g. within a 90 \nmin or 120 min travel time\n\nWork related trips/\nactivities will be generated \nduring the open periods to \naccount for multiple job \nsites per job', self)
        worklocbutton.setGeometry((size.width()) / 4 - 100, size.height() / 2 - 200, 200, 400)


        schoollocbutton = QPushButton('School location choice\n\nDuring simulation, \ngenerate Choice Sets \nconditional on the home \nlocation e.g. within a 60 \nmin', self)
        schoollocbutton.setGeometry((size.width()) / 2 - 100, size.height() / 2 - 200, 200, 400)


        preschoollocbutton = QPushButton('Pre-school location \nchoice\n\nDuring simulation, \ngenerate Choice Sets \nthat are within a 20 \nminute driving distance \nfrom home or work \nlocation of the adult(s)\n\nAlternatively just identify\n possible locations similar \nto school location', self)
        preschoollocbutton.setGeometry((size.width()) * 3 / 4 - 100, size.height() / 2 - 200, 200, 400)


        activitylocbutton = QPushButton('Fixed activity locations for all individuals within the population', self)
        activitylocbutton.setGeometry((size.width()) / 4 - 100, size.height() / 2 + 230, (size.width()) / 2 + 200, 50)

    def paintEvent(self, parent = None):
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




 


