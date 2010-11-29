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
        #self.makeTempTables(self.cursor,table)

            
        if self.isValid():
            self.valid = True
            if table.lower() == 'trips':
                self.setWindowTitle("Trip Characteristics")
            else:
                self.setWindowTitle("Activity Characteristics")
            #self.setWindowIcon(QIcon("./images/region.png"))
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
            #self.vbox.addWidget(aardWarning)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(self.dialogButtonBox)
            self.setLayout(self.vbox)
            
            if self.table == "trips":
                self.xtitle = self.trip_labels(0)
                self.labelsdict = {}
                self.labelsdict['purpose_rec'] = self.trip_labels(1)
                self.labelsdict['mode_rec'] = self.trip_labels(2)
                self.labelsdict['strttime_rec'] = self.trip_labels(3)
                self.labelsdict['endtime_rec'] = self.trip_labels(4)
                self.labelsdict['occupancy_rec'] = self.trip_labels(5)
                self.labelsdict['duration_rec'] = self.trip_labels(6)
                self.labelsdict['miles_rec'] = self.trip_labels(7)
            else:
                self.xtitle = self.schedule_labels(0)
                self.labelsdict = {}
                self.labelsdict['activitytype'] = self.schedule_labels(1)
                self.labelsdict['strttime_rec'] = self.schedule_labels(2)
                self.labelsdict['endtime_rec'] = self.schedule_labels(3)
                self.labelsdict['duration_rec'] = self.schedule_labels(4)
                #self.labelsdict['locationid'] = self.schedule_labes(5)
            
            
            self.connect(self.choicevar1, SIGNAL("currentIndexChanged(int)"), self.on_draw1)
            self.connect(self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.on_draw2)
            self.connect(self.selectvar2, SIGNAL("clicked(bool)"), self.dropVar2)
        

    def isValid(self):
        #return self.checkIfTableExists(self.table)
        return True


    def updatecolumns(self):
        try:
            table_name = ""
            if self.table == "trips":
                table_name = "temptrips"
            else:
                table_name = 'tempschedule'
                
            self.cursor.execute("UPDATE %s SET strttime_rec = 1 WHERE strttime >= 0 AND strttime < 120"%(table_name))
            self.cursor.execute("UPDATE %s SET strttime_rec = 2 WHERE strttime >= 120 AND strttime < 300"%(table_name))
            self.cursor.execute("UPDATE %s SET strttime_rec = 3 WHERE strttime >= 300 AND strttime < 480"%(table_name))
            self.cursor.execute("UPDATE %s SET strttime_rec = 4 WHERE strttime >= 480 AND strttime < 660"%(table_name))
            self.cursor.execute("UPDATE %s SET strttime_rec = 5 WHERE strttime >= 660 AND strttime < 900"%(table_name))
            self.cursor.execute("UPDATE %s SET strttime_rec = 6 WHERE strttime >= 900"%(table_name))
            
            self.cursor.execute("UPDATE %s SET endtime_rec = 1 WHERE endtime >= 0 AND endtime < 120"%(table_name))
            self.cursor.execute("UPDATE %s SET endtime_rec = 2 WHERE endtime >= 120 AND endtime < 300"%(table_name))
            self.cursor.execute("UPDATE %s SET endtime_rec = 3 WHERE endtime >= 300 AND endtime < 480"%(table_name))
            self.cursor.execute("UPDATE %s SET endtime_rec = 4 WHERE endtime >= 480 AND endtime < 660"%(table_name))
            self.cursor.execute("UPDATE %s SET endtime_rec = 5 WHERE endtime >= 660 AND endtime < 900"%(table_name))
            self.cursor.execute("UPDATE %s SET endtime_rec = 6 WHERE endtime >= 900"%(table_name))
            
            if self.table == "trips":
                
                self.cursor.execute("UPDATE tempschedule SET duration_rec = 1 WHERE duration >= 0 AND duration <= 10")
                self.cursor.execute("UPDATE tempschedule SET duration_rec = 2 WHERE duration >= 11 AND duration <= 30")
                self.cursor.execute("UPDATE tempschedule SET duration_rec = 3 WHERE duration >= 31 AND duration <= 120")
                self.cursor.execute("UPDATE tempschedule SET duration_rec = 4 WHERE duration >= 121 AND duration <= 240")
                self.cursor.execute("UPDATE tempschedule SET duration_rec = 5 WHERE duration > 240")
        
        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e
            

    def makecolumns(self):
        try:
            if self.table == "trips":
                if not self.checkColumnExists("temptrips","strttime_rec"):
                    self.cursor.execute("ALTER TABLE temptrips ADD COLUMN strttime_rec bigint")
                if not self.checkColumnExists("temptrips","endtime_rec"):
                    self.cursor.execute("ALTER TABLE temptrips ADD COLUMN endtime_rec bigint")
            else:
                if not self.checkColumnExists("tempschedule","strttime_rec"):
                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN strttime_rec bigint")
                if not self.checkColumnExists("tempschedule","endtime_rec"):
                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN endtime_rec bigint")
                if not self.checkColumnExists("tempschedule","duration_rec"):
                    self.cursor.execute("ALTER TABLE tempschedule ADD COLUMN duration_rec bigint")
        
        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e
        
            
    def makeTempTables(self,cursor,table):
        try:
            if table == "trips":
                if not self.checkIfTableExists("temptrips"):
                    cursor.execute("CREATE TABLE temptrips AS SELECT * FROM %s"%(table))
            else:
                if not self.checkIfTableExists("tempschedule"):
                    cursor.execute("CREATE TABLE tempschedule AS SELECT * FROM %s"%(table))
        
        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e

        
    def on_draw1(self):
        """ Redraws the figure
        """
        if not self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0:
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
                self.axes.bar(ind, self.err2, color='green', align='center')
                self.axes.set_xlabel(self.xtitle[str(self.choicevar1.currentText())])
                self.axes.set_ylabel("Percent (%)")
                
                labelsdict = self.labelsdict[str(self.choicevar1.currentText())]
                labels = []
                for label in self.err1:
                    temp = label
                    if label in labelsdict.keys():
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
                
        elif self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0 and int(self.choicevar2.currentIndex()) > 0:
            self.on_draw2()
            

                


    def retrieveResults(self):

        #self.cursor = self.new_obj.cursor
        vars = self.choicevar1.currentText() + ", count(*)"
        tablename = ""
        if self.table == "trips":
            tablename = "temptrips"
        else:
            tablename = "tempschedule"
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
                tablename = ""
                if self.table == "trips":
                    tablename = "temptrips"
                else:
                    tablename = "tempschedule"
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
                temp = label
                if label in labelsdict.keys():
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
                temp = label
                if label in legenddict.keys():
                    temp = legenddict[label]
                legendlabel.append(temp)

                
            self.axes.legend(bars,legendlabel,prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
            self.axes.set_xlabel(self.xtitle[str(self.choicevar2.currentText())])
            self.axes.set_ylabel("Percent (%)")
                    
            self.canvas.draw()
        


    def boundvalue(self):

        vars = self.choicevar1.currentText()
        tablename = ""
        if self.table == "trips":
            tablename = "temptrips"
        else:
            tablename = "tempschedule"
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
            tablename = ""
            if self.table == "trips":
                tablename = "temptrips"
            else:
                tablename = "tempschedule"
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
    
        xtitle = {'purpose_rec':'Trip Purpose','strttime_rec':'Trip Start Time','endtime_rec':'Trip End Time',
                       'mode_rec':'Trip Mode','occupancy_rec':'Occupancy','duration_rec':'Trip Time (mins)','miles_rec':'Trip Length (miles)'}         
        purposedict = {0:'Return Home',1:'Work',2:'School',3:'Pers Buss',4:'Shopping',5:'Social Visit',6:'Sports/Rec',7:'Meal',
                       8:'Serve Passgr',9:'Other'}
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup Truck',5:'Bus',6:'Train',7:'School Bus',8:'Bike',9:'Walk',
                    10:'Taxi',11:'Other'}
        strttime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        endtime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        occupancy = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5 or more'}
        duration = {1:'0-10',2:'11-30',3:'31-120',4:'121-240',5:'> 240'}
        miles = {1:'0-5',2:'6-15',3:'16-30',4:'31-50',5:'> 50'}
        
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
            return occupancy
        if index == 6:
            return duration
        if index == 7:
            return miles
        
        
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