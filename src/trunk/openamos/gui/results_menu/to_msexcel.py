'''
Created on Aug 17, 2011

@author: dhyou
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

import time
from xlwt import *



class Export_Outputs(QDialog):
    '''
    classdocs
    '''
    
    def __init__(self, configobject = None, parent = None):
        QDialog.__init__(self, parent)
        '''
        Constructor
        '''
        
        self.connects(configobject)
        self.setWindowTitle("Create basic OpenAmos outputs as .csv")
        self.setMinimumSize(QSize(300,200))
        alllayout = QVBoxLayout()
        self.setLayout(alllayout)
        
        
        excelinputbox = QGroupBox("")
        excellayout = QGridLayout()
        excelinputbox.setLayout(excellayout)
        
        selectwidget1 = QWidget()
        selectlayout1 = QVBoxLayout()
        selectwidget1.setLayout(selectlayout1)
        selectlayout1.setContentsMargins(0,0,0,40)
        
        csvnamelabel = QLabel("Save Outputs")
        selectlayout1.addWidget(csvnamelabel)
        
        filewidget = QWidget()
        filelayout = QHBoxLayout()
        filewidget.setLayout(filelayout)
        filelayout.setContentsMargins(0,0,0,0)
        self.xlsname = QLineEdit()
        filelayout.addWidget(self.xlsname)
        self.openfilebutton = QPushButton('...')
        self.openfilebutton.setMaximumWidth(30)
        filelayout.addWidget(self.openfilebutton)
        selectlayout1.addWidget(filewidget)
        
        tablenamelabel = QLabel("Select a person type")
        selectlayout1.addWidget(tablenamelabel)
        
        self.pptype = QComboBox()
        self.pptype.addItems([QString("Adult Worker"),QString("Adult Non-worker"),QString("Non-adult (5-17)"),QString("Preschooler (0-4)")])
        selectlayout1.addWidget(self.pptype)
        
        
        selectwidget2 = QWidget()
        selectlayout2 = QVBoxLayout()
        selectwidget2.setLayout(selectlayout2)
        
        resultlabel = QLabel("Choose result(s)")
        self.resultchoice = QListWidget()
        self.resultchoice.setSelectionMode(QAbstractItemView.MultiSelection)
        self.resultchoice.setFixedWidth(170)
        self.resultchoice.setMinimumHeight(150)
        vars = self.items()
        self.resultchoice.addItems(vars)
        selectlayout2.addWidget(resultlabel)
        selectlayout2.addWidget(self.resultchoice)
        

        #self.export_nhts = QCheckBox("Check if you would export NHTS instead of OpenAmos")
        self.isNHTS = False
        if (self.new_obj.check_if_table_exists("schedule_nhts") and self.new_obj.check_if_table_exists("trips_nhts") \
            and self.new_obj.check_if_table_exists("households_nhts") and self.new_obj.check_if_table_exists("persons_nhts") \
            and self.new_obj.check_if_table_exists("daily_work_status_nhts")):
            
            self.isNHTS = True
        #    self.export_nhts.setDisabled(True)
            
        self.check_all = QCheckBox("Check to select all")

        
        excellayout.addWidget(selectwidget1,0,0)
        excellayout.addWidget(selectwidget2,0,1)
        #excellayout.addWidget(self.export_nhts,1,0)
        excellayout.addWidget(self.check_all,1,0)
    

        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        alllayout.addWidget(excelinputbox)
        alllayout.addWidget(self.dialogButtonBox)
        
        self.connect(self.openfilebutton, SIGNAL("clicked(bool)"), self.save_folder)
        self.connect(self.check_all, SIGNAL("stateChanged(int)"), self.select_all)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

        
    def reject(self):
        self.disconnects()
        QDialog.accept(self)


    def accept(self):
        t1 = time.time()
        
        self.dialogButtonBox.setDisabled(True)
        filename = str(self.xlsname.text())
        sitems = self.resultchoice.selectedItems()
        if filename <> "" and len(sitems) > 0:
            wb = Workbook()
            
            columns = ["starttime","endtime","duration","trippurpose","starttime","endtime","duration","","dweltime","dweltime"]
            for i in range(self.resultchoice.count()):
                item = self.resultchoice.item(i)
                if item.isSelected() and i < 4:
                    wsheet = wb.add_sheet(columns[i])
                    self.sql_quary1(wsheet,columns[i],False)
                    if self.isNHTS:
                        self.sql_quary1(wsheet,columns[i],True)
                elif item.isSelected() and i >= 4 and i < 7:
                    wsheet = wb.add_sheet("%sbyPurpose"%(columns[i]))
                    self.sql_quary2(wsheet,columns[i],False)
                    if self.isNHTS:
                        self.sql_quary2(wsheet,columns[i],True)
                elif item.isSelected() and i == 7:
                    wsheet = wb.add_sheet("TripRate")
                    self.sql_quary3(wsheet,False)
                    if self.isNHTS:
                        self.sql_quary3(wsheet,True)
                elif item.isSelected() and i == 8:
                    wsheet = wb.add_sheet(columns[i])
                    self.sql_quary1(wsheet,columns[i],False)
                    if self.isNHTS:
                        self.sql_quary1(wsheet,columns[i],True)
                elif item.isSelected() and i > 8:
                    wsheet = wb.add_sheet("%sbyPurpose"%(columns[i]))
                    self.sql_quary2(wsheet,columns[i],False)
                    if self.isNHTS:
                        self.sql_quary2(wsheet,columns[i],True)
                        
            wb.save(filename)
            QMessageBox.information(self, "",
                QString("""Outputs exporting is successful!"""), 
                QMessageBox.Yes)
            
            self.reject()
            
        else:
            QMessageBox.warning(self, "Save Outputs...",
                                QString("""Select at least one on the list."""), 
                                QMessageBox.Ok)            
        
        self.dialogButtonBox.setEnabled(True)
        t2 = time.time()
        print 'time taken --> %s'%(t2-t1)

                
    def save_folder(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(self,"Save File","","Comma Delimit (*.xls)")
        if filename <> "":
            self.xlsname.setText(filename)


    def sql_quary1(self,wsheet,column,nhts):
        
        nhts_var = ""
        if nhts and column <> "dweltime":
            count = "sum(a.wttrdfin)"
            nhts_var = ", wttrdfin"
        else:
            count = "count(*)"
            
        if column == "dweltime":
            column = "duration"
            tnames = self.tables(False)
        else:
            tnames = self.tables(True)
                
        if nhts:
            self.table_name(tnames)
#            for i in range(len(tnames)):
#                tnames[i] = tnames[i].replace("_r","") + "_nhts"

        
        cond = self.time_categroy(column)
        labels = self.trip_labels(column)
        temp = cond.keys()
        temp.sort()
        i = 1
        
        err1 = []
        err2 = []
        total = 0
        for key in temp:

            lowhigh = cond[key]
            sql = "select %s from "%(count)
            if len(lowhigh) > 1:
                sql = "%s(select houseid, personid%s from %s where %s >= %d and %s < %d order by houseid, personid) as a" %(sql,nhts_var,tnames[0],column,lowhigh[0],column,lowhigh[1])
            else:
                sql = "%s(select houseid, personid%s from %s where %s = %d) as a" %(sql,nhts_var,tnames[0],column,lowhigh[0])
                
            sql = "%s, (select houseid, personid from %s where %s order by houseid, personid) as b"%(sql,tnames[1],self.age_cond(nhts))
            wrk = self.wrk_cond()
            if wrk != "":
                sql = "%s, (select * from %s where wrkdailystatus = %s order by houseid, personid) as c"%(sql,tnames[2],wrk)
                sql = "%s where a.houseid = b.houseid and a.personid = b.personid and a.houseid = c.houseid and a.personid = c.personid"%(sql)
            else:
                sql = "%s where a.houseid = b.houseid and a.personid = b.personid"%(sql)
            
            print sql
            self.new_obj.cursor.execute(sql)
            data = self.new_obj.cursor.fetchall()
            
            for j in data:
                if j[0] > 0:
                    i += 1
                    
                    err1.append(labels[key])
                    err2.append(long(j[0]))
                    total = total + long(j[0])
        
        #self.cnames(wsheet)
        j = 0
        if nhts:
            self.cnames(wsheet,5)
            j = 4
        else:
            self.cnames(wsheet,1)
            
        for i in range(len(err1)):

            if total > 0.0:
                percent = round(100*float(err2[i])/total,2)
            else:
                percent = 0.0
            wsheet.write(i+2,j,str(err1[i]))
            wsheet.write(i+2,j+1,long(err2[i]))
            wsheet.write(i+2,j+2,percent)


    def sql_quary2(self,wsheet,column,nhts):

        nhts_var = ""
        if nhts and column <> "dweltime":
            count = "sum(a.wttrdfin)"
            nhts_var = ", wttrdfin"
        else:
            count = "count(*)"
            
        if column == "dweltime":
            column = "duration"
            tnames = self.tables(False)
            acttype = "activitytype"
        else:
            tnames = self.tables(True)
            acttype = "trippurpose"
        
            
        if nhts:
            self.table_name(tnames)
        
        
        cond = self.time_categroy(column)
        ylabels = self.trip_labels(column)
        ykeys = cond.keys()
        ykeys.sort()

        xlabels = self.trip_labels("trippurpose")
        xkeys = xlabels.keys()
        xkeys.sort()
        
        yvalue = []
        cumulate = []
        for j in range(len(xkeys)):
            cumulate.append(0)
            
        for key in ykeys:
                
            lowhigh = cond[key]
            xvalue = []
            for j in range(len(xkeys)):
                xvalue.append(0)
                
            sql = "select %s, a.%s from "%(count,acttype)
            if len(lowhigh) > 1:
                sql = "%s(select houseid, personid, %s%s from %s where %s >= %d and %s < %d order by houseid, personid) as a" %(sql,acttype,nhts_var,tnames[0],column,lowhigh[0],column,lowhigh[1])
            else:
                sql = "%s(select houseid, personid, %s%s from %s where %s = %d) as a" %(sql,acttype,nhts_var,tnames[0],column,lowhigh[0])
            sql = "%s, (select houseid, personid from %s where %s order by houseid, personid) as b"%(sql,tnames[1],self.age_cond(nhts))
            
            wrk = self.wrk_cond()
            if wrk != "":
                sql = "%s, (select * from %s where wrkdailystatus = %s order by houseid, personid) as c"%(sql,tnames[2],wrk)
                sql = "%s where a.houseid = b.houseid and a.personid = b.personid and a.houseid = c.houseid and a.personid = c.personid"%(sql)
            else:
                sql = "%s where a.houseid = b.houseid and a.personid = b.personid"%(sql)
            sql = "%s group by a.%s order by a.%s"%(sql,acttype,acttype)
            
            print sql
            self.new_obj.cursor.execute(sql)
            data = self.new_obj.cursor.fetchall()


            for t in data:
                if self.purpose_index(int(t[1])) > 0:
                    index = xkeys.index(self.purpose_index(int(t[1])))
                    xvalue[index] = xvalue[index] + long(t[0])
                    cumulate[index] = cumulate[index] + long(t[0])
            
            yvalue.append(xvalue)
            

        j = 1
        if nhts:
            j = len(xkeys)+4
            wsheet.write(0,len(xkeys)+3,"NHTS")            
        else:
            wsheet.write(0,0,"OpenAmos")
            
        for xkey in xkeys:
            wsheet.write(1,j,str(xlabels[xkey]))
            j += 1
        
        i = 2
        for y in yvalue:

            if nhts:
                wsheet.write(i,len(xkeys)+3,str(ylabels[ykeys[i-2]]))
            else:
                wsheet.write(i,0,str(ylabels[ykeys[i-2]]))
                
            for j in range(len(y)):
                if cumulate[j] > 0.0:
                    percent = round(100*float(y[j])/cumulate[j],2)
                else:
                    percent = 0.0

                if nhts:
                    wsheet.write(i,j+len(xkeys)+4,percent)
                else:
                    wsheet.write(i,j+1,percent)
                
            i += 1


    def sql_quary3(self,wsheet,nhts):
   
        tnames = self.tables(True)
        if nhts:
            self.table_name(tnames)
#            for i in range(len(tnames)):
#                tnames[i] = tnames[i].replace("_r","") + "_nhts"
                
        wrk = self.wrk_cond()
        if wrk == "":
            table = "%s as p"%(tnames[1])
            condition = ""
        else:
            table = "%s as p, %s as w"%(tnames[1],tnames[2])
            condition = "p.houseid = w.houseid and p.personid = w.personid and w.wrkdailystatus = %s and "%(wrk)
        
        nhts_var = ""
        if nhts:
            count = "sum(wtperfin)"
            nhts_var = ", p.wtperfin"
        else:
            count = "count(*)"
            
        sql = "select b.freq, %s from (select p.houseid, p.personid%s from %s"%(count,nhts_var,table)
        sql = "%s where %sp.%s) as a left join "%(sql,condition,self.age_cond(nhts))
        sql = "%s (select houseid, personid, count(*) as freq from %s group by houseid, personid) as b "%(sql,tnames[0])
        sql = "%s on a.houseid = b.houseid and a.personid = b.personid group by b.freq order by b.freq"%(sql)

        
        print sql
        self.new_obj.cursor.execute(sql)
        data = self.new_obj.cursor.fetchall()
        
        err1 = []
        err2 = []
        total = 0
        for j in data:
            if j[0] != None:

                err1.append(j[0])
                err2.append(long(j[1]))
                total += long(j[1])
        
        
        
        j = 0
        if nhts:
            self.cnames(wsheet,5)
            j = 4 
        else:
            self.cnames(wsheet,1)
            
        for i in range(len(err1)):
            if total > 0.0:
                percent = round(100*float(err2[i])/total,2)
            else:
                percent = 0.0
                
            wsheet.write(i+2,j,str(err1[i]))
            wsheet.write(i+2,j+1,long(err2[i]))
            wsheet.write(i+2,j+2,percent)

            


    def purpose_index(self, key):

        index = 0
        if key == 100:
            index = 1
        elif key >= 101 and key < 200:
            index = 2
        elif key >= 200 and key < 300:
            index = 3
        elif key >= 300 and key < 400:
            index = 4
        elif key >= 400 and key < 500:
            index = 5
        elif key >= 500 and key < 597:
            index = 6
        elif key >= 597 and key <=598:
            index = 7
        elif key == 600:
            index = 8
        elif key == 601:
            index = 9
        elif key == 599:
            index = 10
            
        return index                

    def age_cond(self,nhts):
        if self.pptype.currentIndex() <= 1:
            age = "age >= 18"
        elif self.pptype.currentIndex() == 2:
            age = "age < 18 and age >= 5"
        else:
            age = "age < 5"
            
        if nhts:
            age = age.replace("age", "r_age")
        return age

    def wrk_cond(self):
        if self.pptype.currentIndex() == 0:
            return "1"
        elif self.pptype.currentIndex() == 1:
            return "0"
        else:
            return ""
        
    def tables(self,istrip):
        if istrip:
            table_names = ["trips_r","persons","daily_work_status_r"]
            return table_names
        else:
            table_names = ["schedule_final_r","persons","daily_work_status_r"]
            return table_names 
    
    def table_name(self,names):
        for i in range(len(names)):
            if names[i].find("_final_r") > -1:
                names[i] = names[i].replace("_final_r","") + "_nhts"
            elif names[i].find("_r") > -1:
                names[i] = names[i].replace("_r","") + "_nhts"  
            else:
                names[i] = names[i] + "_nhts"      

    def time_categroy(self,column):
        time = {1:[0,60],2:[60,120],3:[120,180],4:[180,240],5:[240,300],6:[300,360],
                7:[360,420],8:[420,480],9:[480,540],10:[540,600],11:[600,660],12:[660,720],
                13:[720,780],14:[780,840],15:[840,900],16:[900,960],17:[960,1020],18:[1020,1440]}
        mode = {1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],11:[11]}
        duration = {1:[0,10],2:[10,20],3:[20,30],4:[30,50],5:[50,70],
                    6:[70,100],7:[100,150],8:[150,200],9:[200,250],10:[250,1440]}
        miles = {1:[0,5],2:[5,10],3:[10,15],4:[15,20],5:[20,25],
                 6:[25,30],7:[30,40],8:[40,50],9:[50,30000]}
        occupancy = {1:[0],2:[1],3:[2],4:[3],5:[4],6:[5,30000]}
        activitytype = {1:[100],2:[101,200],3:[200,300],4:[300,400],5:[400,500],
                        6:[500,597],7:[597,599],8:[600],9:[601],10:[599]}

        if column == "starttime" or column == "endtime": 
            return time
        elif column == "tripmode":
            return mode
        elif column == "duration":
            return duration
        elif column == "miles":
            return miles
        elif column == "occupancy":
            return occupancy
        elif column == "activitytype" or column == "trippurpose":
            return activitytype

    def trip_labels(self, column):
        activitytype = {1:'Home',2:'In-Home',3:'Work',4:'School',5:'Maintenance',6:'Discretionary',
                        7:'Anchor',8:'Pick Up',9:'Drop Off',10:'OH-Other'}             
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup Truck',5:'Bus',6:'Train',7:'School Bus',8:'Bike',9:'Walk',
                    10:'Taxi',11:'Other'}
        starttime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                    7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                    13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        endtime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                   7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                   13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        occupancy = {1:'0',2:'1',3:'2',4:'3',5:'4',6:'5 or more'}
        duration = {1:'0-10',2:'10-20',3:'20-30',4:'30-50',5:'50-70',
                    6:'70-100',7:'100-150',8:'150-200',9:'200-250',10:'>= 250'}
        miles = {1:'0-5',2:'5-10',3:'10-15',4:'15-20',5:'20-25',
                 6:'25-30',7:'30-40',8:'40-50',9:'>= 50'}
        
        if column == "activitytype" or column == "trippurpose":
            return activitytype
        if column == "tripmode":
            return modedict
        if column == "starttime":
            return starttime
        if column == "endtime":
            return endtime
        if column == "occupancy":
            return occupancy
        if column == "duration":
            return duration
        if column == "miles":
            return miles

    def select_all(self):
        if self.check_all.isChecked():
            for i in range(self.resultchoice.count()):
                temp = self.resultchoice.item(i)
                temp.setSelected(True)  
        else:
            for i in range(self.resultchoice.count()):
                temp = self.resultchoice.item(i)
                temp.setSelected(False)  
            
    def items(self):
        vars = ["trip starttime","trip endtime","trip duration","trip purpose","trip starttime by purpose",
                "trip endtime by purpose","trip duration by purpose","trip episode rate","dwell time","dwell time by activity"]
        return vars
    
    def tnames(self,wsheet,ind):
        names = self.items()
        wsheet.write(0,0,names[ind])

    def cnames(self,wsheet,i):
        if i == 1:
            wsheet.write(0,i-1,"OpenAmos")
        else:
            wsheet.write(0,i-1,"NHTS")
            
        wsheet.write(1,i,"Frequency")
        wsheet.write(1,i+1,"Percent(%)")
            
    def connects(self,configobject):
        
        protocol = configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        user_name = configobject.getConfigElement(DB_CONFIG,DB_USER)
        password = configobject.getConfigElement(DB_CONFIG,DB_PASS)
        host_name = configobject.getConfigElement(DB_CONFIG,DB_HOST)
        database_name = configobject.getConfigElement(DB_CONFIG,DB_NAME)
        
        self.database_config_object = DataBaseConfiguration(protocol, user_name, password, host_name, database_name)
        self.new_obj = DataBaseConnection(self.database_config_object)
        self.new_obj.new_connection()
        

    def disconnects(self):
        self.new_obj.close_connection()


def main():
    app = QApplication(sys.argv)
    wizard = Export_Outputs()
    wizard.show()
    app.exec_()

if __name__=="__main__":
    main()