'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np
import matplotlib.font_manager as plot

from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import *



class MakeSchedPlot(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setMinimumSize(QSize(900,500))
        self.setWindowTitle("Child Activity Skeletons")
        self.dpi = 100
        self.fig = Figure((5.0, 4.5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        
        protocol = "postgres"        
        user_name = "postgres"
        password = "1234"
        host_name = "10.206.111.111"
        database_name = "mag_zone"
        
        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()
        

        self.vbox = QVBoxLayout()
        self.vbox.setStretch(0,1)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.dialogButtonBox)
        self.setLayout(self.vbox)
        
        self.on_draw()

        #self.makeTempTables(self.cursor,table)



    def isValid(self):
        return True
        #return self.checkIfTableExists(self.table)   


    def on_draw(self):
        """ Redraws the figure
        """
        
        data = [[100,0,395,300,396,332,100,729,710],
                [100,0,325,300,326,213,415,568,34,100,669,770],
                [100,0,149,513,159,18,101,182,5,300,258,484,100,743,696],
                [100,0,172,101,173,1,513,199,20,416,266,49,300,367,388,412,797,41,100,885,554],
                [100,0,302,300,303,435,101,742,10,514,775,61,101,840,0,101,841,1,100,897,542],
                [100,0,285,300,286,312,101,602,51,101,654,59,101,714,2,412,732,68,100,879,560],
                [100,0,158,300,237,518,101,759,0,514,799,15,412,839,15,415,887,3,100,906,533]
                ]
        rows = len(data)
        ticks = np.arange(rows+1)
        ind = 1
        height = 0.4
        
        bars=[]
        
        for row in data:
            rowlen = len(row)
            for i in range(2,rowlen,3):
                self.axes.barh(ind, row[i], height, left=row[i-1],color=self.colors(row[i-2]))
            ind = ind + 1
        
        bars=[]
        bars.append(barh(0, 1, 1, left=0,color=self.colors(100)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(200)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(300)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(411)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(412)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(415)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(416)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(513)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(514)))
        bars.append(barh(0, 1, 1, left=0,color=self.colors(900)))
        
        prop = matplotlib.font_manager.FontProperties(size=8)   
        self.axes.legend(bars,('In-home','Work','School','Pers Buss',
                          'Shopping','Meal','Srv Passgr','Social',
                          'Sports/Rec','Other'),prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Persons")
        self.axes.set_yticks(ticks)
                
        self.canvas.draw()
        
                 
    
    def colors(self, index):
        colorpooldict = {100:'#0000FF',101:'#0000FF',200:'#A9A9A9',300:'#7B68EE',411:'#FF9933',
                         412:'#32CD32',415:'#66CCFF',416:'#B88A00',513:'#B8002E',
                         514:'#FFD700',900:'#000000'}

        return colorpooldict[index]
    
    
        
        
    def schedule_labels(self, index):
        xtitle = {'activitytype':'Activity Type','strttime_rec':'Start Time','endtime_rec':'End Time',
                  'duration_rec':'Activity Duration (mins)'}
        activitytype = {100:'In-home',200:'Work',300:'School',411:'Pers Buss',412:'Shopping',
                        415:'Meal',416:'Serve Passgr',513:'Social Visit',514:'Sports/Rec',900:'Other'}
        strttime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        endtime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        duration = {1:'0-10',2:'11-30',3:'31-120',4:'121-240',5:'> 240'}

        if index == 0:
            return xtitle
        if index == 1:
            return activitytype
        if index == 2:
            return strttime
        if index == 3:
            return endtime
        if index == 4:
            return duration


        

def main():
    app = QApplication(sys.argv)
    diag = MakeSchedPlot()
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
