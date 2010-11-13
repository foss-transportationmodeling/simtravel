'''
Created on Nov 9, 2010

@author: dhyou
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from core_plot import *
import numpy as np
import matplotlib.font_manager as plot


class MakePlot(Matplot):
    def __init__(self, config, table, parent=None):
        Matplot.__init__(self)
        self.valid = False
        self.connects(config)
        self.cursor = self.new_obj.cursor
        self.table = table
        if self.isValid():
            self.valid = True
            self.setWindowTitle("Average Absolute Relative Difference Distribution")
            self.setWindowIcon(QIcon("./images/region.png"))
            aardWarning = QLabel("""<font color = blue>Note: The above chart shows the distribution of the """
                                 """Average Absolute Relative Difference (AARD)"""
                                 """ across all geographies for which a synthetic population was generated. """
                                 """ The AARD measure gives the average deviation of the person weighted sums """
                                 """with respect to composite person type constraints. """
                                 """The measure is used to monitor convergence in the Iterative Proportional Updating (IPU)"""
                                 """ algorithm of PopGen. </font>""")
    
            aardWarning.setWordWrap(True)
            self.fill_variable1(self.table)
            self.vbox.addWidget(self.addfilter)
            self.vbox.addWidget(aardWarning)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(self.dialogButtonBox)
            self.setLayout(self.vbox)
            
            if self.table == "trips":
                self.xtitle = self.trip_labels(0)
                self.labelsdict = {}
                self.labelsdict['purpose'] = self.trip_labels(1)
                self.labelsdict['mode'] = self.trip_labels(2)
                self.labelsdict['strttime'] = self.trip_labels(3)
                self.labelsdict['endtime'] = self.trip_labels(4)
                self.labelsdict['occupancy'] = self.trip_labels(5)
            
            
            self.connect(self.choicevar1, SIGNAL("currentIndexChanged(int)"), self.on_draw1)
            self.connect(self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.on_draw2)
            self.connect(self.selectvar2, SIGNAL("clicked(bool)"), self.dropVar2)
        

    def isValid(self):
        return self.checkIfTableExists(self.table)

    def on_draw1(self):
        """ Redraws the figure
        """
        if not self.selectvar2.isChecked() and str(self.choicevar1.currentIndex())>0:
            self.err1 = []
            self.err2 = []          
            if self.retrieveResults():
            # clear the axes and redraw the plot anew
                self.axes.clear()
                self.axes.grid(True)
                N=len(self.err1)
                ind = np.arange(N)
        
                #self.axes.hist(self.err, range=(1,10), normed=True, cumulative=False, histtype='bar', align='mid', orientation='vertical', log=False)
                #self.axes.hist(self.err, normed=False, align='left')
                self.axes.bar(ind, self.err2, align='center')
                self.axes.set_xlabel(self.xtitle[str(self.choicevar1.currentText())])
                self.axes.set_ylabel("Percent (%)")
                
                labelsdict = self.labelsdict[str(self.choicevar1.currentText())]
                labels = []
                for label in self.err1:
                    temp = labelsdict[label]
                    labels.append(temp)
                    
                self.axes.set_xticks(ind)
                if len(labels) >= 13:
                    self.axes.set_xticklabels(labels, size='xx-small')
                elif (len(labels) >= 7):
                    self.axes.set_xticklabels(labels, size='x-small')
                else:
                    self.axes.set_xticklabels(labels)
            
                self.canvas.draw()

                


    def retrieveResults(self):

        #self.cursor = self.new_obj.cursor
        vars = self.choicevar1.currentText() + ", count(*)"
        tablename = self.table
        filter = self.choicevar1.currentText() + " >= 0"
        group = self.choicevar1.currentText()
        order = self.choicevar1.currentText()
        
        try:
            total = 0.0
            retrieve = self.executeSelectQuery(self.cursor, vars, tablename, filter, group, order)
            for i in retrieve:
                self.err1.append(i[0])
                self.err2.append(i[1])
                total = total + i[1]
                
            for i in range(len(self.err1)):
                self.err2[i] = 100*float(self.err2[i])/total

            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e
            
        return False


    def on_draw2(self):
        """ Redraws the figure
        """
        self.err1 = []
        self.err2 = []
            
        if self.x_axe_value():
            
            bound = self.boundvalue()
            bound.sort()
            
            self.axes.clear()
            self.axes.grid(True)
            N=len(self.err1)
            ind = np.arange(N)
            
            bars = []
            cumulate = []
            for j in range(len(self.err1)):
                cumulate.append(0)
            
            i = 0       
            for var in bound:
                
                vars = "%s, count(*)" %(self.choicevar2.currentText())
                tablename = self.table
                filter = "%s = %s and %s >= 0 and %s >= 0" %(self.choicevar1.currentText(),var,
                                                             self.choicevar1.currentText(),self.choicevar2.currentText())
                group = self.choicevar2.currentText()
                order = self.choicevar2.currentText()
            
                value1 = []
                previous = []
                for j in range(len(self.err1)):
                    value1.append(0)
                    previous.append(cumulate[j])
                    
                try:
                    retrieve = self.executeSelectQuery(self.cursor, vars, tablename, filter, group, order)
                    for k in retrieve:
                        index = self.err1.index(k[0])
                        value1[index] = 100*float(k[1])/self.err2[index]
                        cumulate[index] = cumulate[index] + value1[index]                    
        
                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e
    
                colors = self.colors(i)
                if i == 0:
                    temp = self.axes.bar(ind, value1, color=colors, align='center')
                    bars.append(temp[0])
                else:
                    temp = self.axes.bar(ind, value1, color=colors, align='center', bottom=previous)
                    bars.append(temp[0])
                i = i + 1
            
            prop = matplotlib.font_manager.FontProperties(size=8)

            
            labelsdict = self.labelsdict[str(self.choicevar2.currentText())]
            labels = []
            for label in self.err1:
                temp = labelsdict[label]
                labels.append(temp)
                
            self.axes.set_xticks(ind)
            if len(labels) >= 13:
                self.axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                self.axes.set_xticklabels(labels, size='x-small')
            else:
                self.axes.set_xticklabels(labels)
            
            legenddict = self.labelsdict[str(self.choicevar1.currentText())]
            legendlabel = []
            for label in bound:
                temp = legenddict[label]
                legendlabel.append(temp)
                
            self.axes.legend(bars,legendlabel,prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
            self.axes.set_xlabel(self.xtitle[str(self.choicevar2.currentText())])
            self.axes.set_ylabel("Percent (%)")
                    
            self.canvas.draw()
        


    def boundvalue(self):

        vars = self.choicevar1.currentText()
        tablename = self.table
        filter = "%s >= 0" %(self.choicevar1.currentText())
        group = self.choicevar1.currentText()
        order = self.choicevar1.currentText()
        
        values = []
        try:
            retrieve = self.executeSelectQuery(self.cursor, vars, tablename, filter, group, order)
            for i in retrieve:
                values.append(i[0])
            return values

        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e
                        
        return values
    
    
    def x_axe_value(self):

        if str(self.choicevar1.currentIndex())>0 and str(self.choicevar2.currentIndex())>0:
            vars = "%s, count(*)" %(self.choicevar2.currentText())
            tablename = self.table
            filter = "%s >= 0 and %s >= 0" %(self.choicevar1.currentText(),self.choicevar2.currentText())
            group = self.choicevar2.currentText()
            order = self.choicevar2.currentText()
    
            try:
                retrieve = self.executeSelectQuery(self.cursor, vars, tablename, filter, group, order)
                for i in retrieve:
                    self.err1.append(i[0])
                    self.err2.append(i[1])
                
                return True
    
            except Exception, e:
                print '\tError while fetching the columns from the table'
                print e
            
            return False
        else:
            return False
                        
    
    def colors(self, index):
        colorpool = ['#0000FF','#FFFF00','#7B68EE','#FF4500','#1E90FF','#F0E68C','#87CEFA','#FFFACD',
                     '#FFD700','#4169E1','#FFA500','#6495ED','#BDB76B','#00BFFF','#FF6347','#B0E0E6',
                     '#ADFF2F','#808080','#32CD32','#C0C0C0','#00FA9A','#DCDCDC','#228B22','#006400',
                     '#696969','#00FF00','#A9A9A9','#98FB98','#D3D3D3','#3CB371']
        return colorpool[index]
    
    
    def trip_labels(self, index):
    
        xtitle = {'purpose':'Trip Purpose','strttime':'Trip Starting Time','endtime':'Trip Ending Time',
                       'mode':'Transportation Mode','occupancy':'Occupancies'}         
        purposedict = {0:'Home',1:'Work',2:'School',3:'Pers Buss',4:'Shopping',5:'Social',6:'Recreation',7:'Meals',
                       8:'Serve Pass',9:'Other'}
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup',5:'Truck',6:'RV',7:'Motorcycle',8:'Gold Cart',9:'Public Bus',
                    10:'Commu Bus',11:'School Bus',12:'Charter',13:'City-City Bus',14:'Shuttle',15:'Amtrak',
                    16:'Commu Train',17:'Subway',18:'Trolley',19:'Taxicab',20:'Ferry',21:'Airplane',22:'Bicycle',
                    23:'Walk',24:'Wheelchair',97:'Other'}
        strttime = {1:'0 to 1',2:'1 to 2',3:'2 to 3',4:'3 to 4',5:'4 to 5',6:'5 to 6',7:'6 to 7',8:'7 to 8',
                    9:'8 to 9',10:'9 to 10',11:'10 to 11',12:'11 to 12',13:'12 to 13',14:'13 to 14',15:'14 to 15',
                    16:'15 to 16',17:'16 to 17',18:'17 to 18',19:'18 to 19',20:'19 to 20',21:'20 to 21',
                    22:'21 to 22',23:'22 to 23',24:'23 to 24'}
        endtime = {1:'0 to 1',2:'1 to 2',3:'2 to 3',4:'3 to 4',5:'4 to 5',6:'5 to 6',7:'6 to 7',8:'7 to 8',
                   9:'8 to 9',10:'9 to 10',11:'10 to 11',12:'11 to 12',13:'12 to 13',14:'13 to 14',15:'14 to 15',
                   16:'15 to 16',17:'16 to 17',18:'17 to 18',19:'18 to 19',20:'19 to 20',21:'20 to 21',
                   22:'21 to 22',23:'22 to 23',24:'23 to 24'}
        accmp = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',
                 9:'9',10:'10',11:'11',12:'12',13:'13',14:'14',15:'15'}
        
        if index == 0:
            return xtitle
        if index == 1:
            return purposedict
        if index == 2:
            return modedict
        if index == 3:
            return strttime
        if index == 4:
            return endtime
        if index == 5:
            return accmp
        
        
    def dropVar2(self):
        if not self.selectvar2.isChecked():
            self.choicevar2.setEnabled(False)
        else:
            self.choicevar2.setEnabled(True)


        

def main():
    app = QApplication(sys.argv)
    diag = MakePlot('project')
    diag.show()
    #res.show()
    app.exec_()

if __name__ == "__main__":
    main()