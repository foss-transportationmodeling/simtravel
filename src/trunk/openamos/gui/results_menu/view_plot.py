'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random
import numpy as np
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *

from pylab import *
#from core_plot import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as plot
from matplotlib.patches import Patch, Rectangle
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MakeResultPlot(QDialog):
    def __init__(self, config, parent=None):
        QDialog.__init__(self, parent)

        self.setMinimumSize(QSize(900,600))
        self.setWindowTitle("Profile of Activity Travel Pattern")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.new_obj = None
        self.project = None        
        self.valid = False
        self.connects(config)
        self.cursor = self.new_obj.cursor
        self.table = 'households'
        self.data = []
        self.figs = []
        self.sketches = []
        self.axes = []
        self.toolbars = []

        self.makeVarsWidget1()
        self.tabs = QTabWidget()
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self.tabs, SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok)

        radiowidget = QWidget(self)
        radiolayout = QHBoxLayout()
        radiowidget.setLayout(radiolayout)
        segment = QGroupBox(self)
        addsegment = QHBoxLayout()
        segment.setLayout(addsegment)
        self.tripradio = QRadioButton("Travel Characteristics")
        self.tripradio.setChecked(True)
        self.actiradio = QRadioButton("Activity Characteristics")
        addsegment.addWidget(self.tripradio)
        addsegment.addWidget(self.actiradio)
        radiolayout.addWidget(segment)
        
        filter = QGroupBox(self)
        addfilter = QHBoxLayout()
        filter.setLayout(addfilter)
        var1 = QLabel("Variable 1")
        self.choicevar1 = QComboBox()
        self.choicevar1.setMinimumWidth(150)
        var2 = QLabel("Variable 2")
        self.choicevar2 = QComboBox()
        self.choicevar2.setMinimumWidth(150)
        addfilter.addWidget(var1)
        addfilter.addWidget(self.choicevar1)
        addfilter.addWidget(var2)
        addfilter.addWidget(self.choicevar2)
        radiolayout.addWidget(filter)
        radiolayout.setContentsMargins(0,0,0,0)
        self.fill_vari()       

        stablewidget = QWidget(self)
        stablelayout = QHBoxLayout()
        stablewidget.setLayout(stablelayout)
        
        tools = QToolBar()
        tools.setMaximumWidth(150)
        home_action = self.createaction("Go Home",self.gohome,"home","")
        zoom_action = self.createaction("Zoom",self.zoom,"viewmag+","")
        pan_action = self.createaction("Pan",self.panzoom,"pan")
        tools.addAction(home_action)
        tools.addAction(zoom_action)
        tools.addAction(pan_action)
        stablelayout.addWidget(tools)

        output = QGroupBox(self)
        addoutput = QHBoxLayout()
        output.setLayout(addoutput)
        self.freq = QRadioButton("Frequency     ")
        self.freq.setChecked(True)
        self.percent = QRadioButton("Percent(%) ")
        addoutput.addWidget(self.freq)
        addoutput.addWidget(self.percent)
        addoutput.setAlignment(Qt.AlignCenter)
        stablelayout.addWidget(output)
        
        substablewidget = QWidget(self)
        substablelayout = QHBoxLayout()
        substablewidget.setLayout(substablelayout)
        substablelayout.setAlignment(Qt.AlignLeft)
        stablelayout.addWidget(substablewidget) 
        self.resetbutton = QPushButton('Reset')
        self.resetbutton.setFixedWidth(80)
        stablelayout.addWidget(self.resetbutton)      
        self.showbutton = QPushButton('Show Plot')
        self.showbutton.setFixedWidth(80)
        stablelayout.addWidget(self.showbutton)
        stablelayout.setContentsMargins(0,0,0,0)

        progresswidget = QWidget(self)
        progresslayout = QHBoxLayout()
        progresswidget.setLayout(progresslayout)
        self.progresslabel = QLabel("")
        self.progresslabel.setMinimumWidth(150)
        progresslayout.addWidget(self.progresslabel)
        progresslayout.addWidget(self.dialogButtonBox)
        progresslayout.setContentsMargins(0,0,0,0)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(radiowidget)
        self.vbox.addWidget(self.varswidget1)
        self.vbox.addWidget(stablewidget)
        self.vbox.addWidget(self.tabs)
        self.vbox.addWidget(progresswidget)
        self.vbox.setStretch(3,1)
        self.setLayout(self.vbox)
        
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.disconnects)
        self.connect(self.resetbutton, SIGNAL("clicked(bool)"), self.reset_all)
        self.connect(self.showbutton, SIGNAL("clicked(bool)"), self.draw_plot)
        self.connect(self.tripradio, SIGNAL("clicked(bool)"), self.fill_vari)
        self.connect(self.actiradio, SIGNAL("clicked(bool)"), self.fill_vari)
        self.connect(self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.set_disable)

        self.labelsdict = {}
        self.labelsdict['activitytype'] = self.trip_labels(2)
        self.labelsdict['purpose'] = self.trip_labels(3)
        self.labelsdict['tripmode'] = self.trip_labels(4)
        self.labelsdict['starttime'] = self.trip_labels(5)
        self.labelsdict['endtime'] = self.trip_labels(6)
        self.labelsdict['occupancy'] = self.trip_labels(7)
        self.labelsdict['duration'] = self.trip_labels(8)
        self.labelsdict['miles'] = self.trip_labels(9)


    def makeVarsWidget1(self):
        
        self.varswidget1 = QGroupBox("")
        self.varslayout = QGridLayout()
        self.varswidget1.setLayout(self.varslayout)
        self.varswidget1.setContentsMargins(0,0,0,0)

        segment = QGroupBox(self)
        addsegment = QVBoxLayout()
        segment.setLayout(addsegment)
        self.segment1 = QRadioButton("Households")
        self.segment1.setChecked(True)
        self.segment2 = QRadioButton("Persons")
        addsegment.addWidget(self.segment1)
        addsegment.addWidget(self.segment2)
        self.varslayout.addWidget(segment,1,0)
        segment.setContentsMargins(0,0,0,0)
                        
        tableslabel = QLabel('Columns')
        self.varslayout.addWidget(tableslabel,0,1)
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        if self.columnName() <> None:
            self.colswidget.addItems(self.columnName())
        self.colswidget.setMaximumWidth(180)
        self.colswidget.setMaximumHeight(150)
        self.varslayout.addWidget(self.colswidget,1,1)
        
        varslabel = QLabel('Values')
        self.varslayout.addWidget(varslabel,0,2)
        self.valwidget = QListWidget()
        self.valwidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.valwidget.setMaximumWidth(180)
        self.valwidget.setMaximumHeight(150)
        self.varslayout.addWidget(self.valwidget,1,2)        
        
        buttonwidget1 = QWidget(self)
        buttonlayout1 = QVBoxLayout()
        buttonwidget1.setLayout(buttonlayout1)
        self.selbutton1 = QPushButton('>>')
        self.selbutton1.setFixedWidth(60)
        buttonlayout1.addWidget(self.selbutton1)
        self.delbutton = QPushButton('<<')
        self.delbutton.setFixedWidth(60)
        buttonlayout1.addWidget(self.delbutton)
        self.varslayout.addWidget(buttonwidget1,1,3)

        self.varstable = QTableWidget(0,2,self)
        self.varstable.setHorizontalHeaderLabels(['Column', 'Value'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.setMaximumWidth(360)
        self.varstable.setMaximumHeight(150)
        self.varslayout.addWidget(self.varstable,1,4)

        self.connect(self.colswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateValues)
        self.connect(self.selbutton1, SIGNAL("clicked(bool)"), self.selValue)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delValue)
        self.connect(self.segment1, SIGNAL("clicked(bool)"), self.initTables)
        self.connect(self.segment2, SIGNAL("clicked(bool)"), self.initTables)


    def createaction(self, text, slot=None, icon=None,
                     tip=None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)

        return action


    def on_context_menu(self,point):
        menubar = QMenu(self)
        one = menubar.addAction("Show Plot")
        two = menubar.addAction("Remove Current Tab")
        three = menubar.addAction("Save Plot as PNG")

        self.connect(one,SIGNAL("triggered()"),self.draw_plot)
        self.connect(two,SIGNAL("triggered()"),self.removeTab)
        self.connect(three,SIGNAL("triggered()"),self.saveimg)
        menubar.popup(self.tabs.mapToGlobal(point))

    def saveimg(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(self,"Save Image","","PNG image (*.png)")
        if str(filename) != "":
            index = self.tabs.currentIndex()
            fig = self.figs[index]
            fig.savefig(str(filename))
             
    def draw_plot(self):
        if self.choicevar1.currentText() != "" and self.choicevar2.currentText() != "":
            self.on_draw2()
        elif self.choicevar1.currentText() != "":
            self.on_draw1()

    def makePlotTab(self,chart):
        page1 = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(chart)
        page1.setLayout(vbox)
        chartname = ""
        index = -1
        if self.tabs.count() > 0:
            index = self.tabs.count() - 1
            tabtitle = self.tabs.tabText(index)
            numtab = int(tabtitle.split(" ")[1]) + 1
            chartname = "Chart %s" %(numtab)
        else:
            chartname = "Chart 1"
        self.tabs.addTab(page1, chartname)
        index = index + 1
        self.tabs.setCurrentIndex(index)

    def makeTableTab(self,stable):
        page1 = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(stable)
        page1.setLayout(vbox)
        chartname = ""
        index = -1
        if self.tabs.count() > 0:
            index = self.tabs.count() - 1
            tabtitle = self.tabs.tabText(index)
            numtab = int(tabtitle.split(" ")[1]) + 1
            chartname = "Table %s" %(numtab)
        else:
            chartname = "Table 1"
        self.tabs.addTab(page1, chartname)
        index = index + 1
        self.tabs.setCurrentIndex(index)

    def removeTab(self):
        index = self.tabs.currentIndex()
        reply = QMessageBox.information(self,"Warning","Do you really want to remove?",QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes and index >= 0:
            self.tabs.removeTab(index)
            self.figs.pop(index)
            self.sketches.pop(index)
            self.axes.pop(index)
            self.toolbars.pop(index)
    
    def reset_all(self):
        reply = QMessageBox.information(self,"Warning","Do you really want to remove?",QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tabs.clear()
            self.figs = []
            self.sketches = []
            self.axes = []
            self.toolbars = []
            
            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())
        
 
    def createCanvas(self):
#        mydpi = 100
#        myfig = Figure((5.0, 4.5), dpi=mydpi)
        myfig = plt.figure()
        self.figs.append(myfig)
        sketch = FigureCanvas(myfig)
        QWidget.setSizePolicy(sketch,QSizePolicy.Expanding,QSizePolicy.Expanding)
        myaxes = myfig.add_subplot(111)
        
        myCanvas = []
        myCanvas.append(sketch)
        myCanvas.append(myaxes)
        self.sketches.append(sketch)
        self.axes.append(myaxes)
        
        tool = NavigationToolbar(sketch,self)
        self.toolbars.append(tool)
        
        return myCanvas
        

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
        self.close()

    def set_disable(self):
        if self.choicevar2.currentText() != "":
            self.percent.setChecked(True)
            self.freq.setEnabled(False)
        else:
            self.freq.setEnabled(True)

    def columnName(self):
        if self.new_obj.check_if_table_exists(self.table):
            cols = self.new_obj.get_column_list(self.table)
            columns = []
            for col in cols:
                
                columns.append(QString(col))
            return columns
        else:
            return None
    
    def populateValues(self, item):
        
        try:
            values = []
            temp = None
            vars = str(item.text())
            tablename = self.table
            order = str(item.text())
            
            self.cursor.execute("""SELECT DISTINCT %s FROM %s ORDER BY %s"""%(vars,tablename,order))
            temp = self.cursor.fetchall()
            
            for i in temp:
                value = str(i[0])
                values.append(value)
                
            self.valwidget.clear()
            self.valwidget.addItems(values)

        except Exception, e:
            print '\tError while creating the table %s'%self.table_name
            print e


    def selValue(self):
        if (self.colswidget.currentItem() != None) & (self.valwidget.currentItem() != None):
            currcolumn = (self.colswidget.currentItem()).text()
            currvar = (self.valwidget.currentItem()).text()
            if not self.isExist(currcolumn,currvar):
                self.varstable.insertRow(self.varstable.rowCount())
                tableitem = QTableWidgetItem()
                tableitem.setText(currcolumn)
                tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
                
                varitem = QTableWidgetItem()
                varitem.setText(currvar)
                varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
                
        else:
            msg = "Please select a Column and a Value"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok) 


    def isExist(self, ccolumn, cvalue):
        numrows = self.varstable.rowCount()
        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            value = str((self.varstable.item(i,1)).text())
            if (column == ccolumn) & (value == cvalue):
                return True
            
        return False
    

    def delValue(self):
        self.varstable.removeRow(self.varstable.currentRow())


    def initTables(self):
        if self.segment1.isChecked() and self.table != 'households':
            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            self.table = 'households'
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())
        if self.segment2.isChecked() and self.table != 'persons':
            self.colswidget.clear()
            self.valwidget.clear()
            self.delRow()
            self.table = 'persons'
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())


    def delRow(self):
        numrows = self.varstable.rowCount() - 1
        while numrows > -1:
            self.varstable.removeRow(numrows)
            numrows = numrows - 1  

    def selectedResults(self):
        sindex = self.idwidget.selectedIndexes()
        sdata = []
        for i in sindex:
            temp = self.data[i.row()]
            sdata.append(temp)
            
        return sdata


    def x_label(self):
        xtitle_trip = {'purpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
                       'tripmode':'Trip Mode','occupancy':'Occupancy','duration':'Trip Time (mins)','miles':'Trip Length (miles)'} 
        xtitle_acti = {'activitytype':'Activity Type','starttime':'Start Time','endtime':'End Time',
                  'duration':'Activity Duration (mins)'}
        
        column1 = str(self.choicevar1.currentText())
        column2 = str(self.choicevar2.currentText())
        
        if self.tripradio.isChecked():
            if column2 != "":
                return xtitle_trip[column2]
            else:
                return xtitle_trip[column1]
        else:
            if column2 != "":
                return xtitle_acti[column2]
            else:
                return xtitle_acti[column1]
            
            
    def plot_title(self):
        xtitle_trip = {'purpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
                       'tripmode':'Trip Mode','occupancy':'Occupancy','duration':'Trip Time (mins)','miles':'Trip Length (miles)'} 
        xtitle_acti = {'activitytype':'Activity Type','starttime':'Start Time','endtime':'End Time',
                  'duration':'Activity Duration (mins)'}
        
        column1 = str(self.choicevar1.currentText())
        column2 = str(self.choicevar2.currentText())
        
        title = ""
        if self.tripradio.isChecked():
            title = xtitle_trip[column1]
        else:
            title = xtitle_acti[column1]
        
        if column2 != "":
            title = title + " by "
            if self.tripradio.isChecked():
                title = title + xtitle_trip[column2]
            else:
                title = title + xtitle_acti[column2]
        
        return title
    
    def stateSQL(self,id):
        tablename = '%s AS A' %(self.schedule_table())
        vars = 'A.houseid, A.personid, A.activitytype, A.starttime, (A.endtime - A.starttime)' #A.duration'
        order = 'A.houseid, A.personid, A.starttime'
        filter = 'A.starttime >= 0'
        
        if self.segment1.isChecked():
            filter = filter + " AND A.houseid = '%s'" %(id)
        else:
            ids = id.split(',')
            filter = filter + " AND A.houseid = '%s' AND A.personid = '%s'" %(ids[0],ids[1])
            
        state = """SELECT DISTINCT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order)

        return state


    def socio_sql(self):
        table1 = ""
        if self.segment1.isChecked():
            table1 = "households"
        else:
            table1 = "persons"
            
        vars = ''
        if self.segment1.isChecked():
            vars = 'houseid'
        else:
            vars = 'houseid, personid'
        
        filter = ''
        numrows = self.varstable.rowCount()
        if numrows < 1:
            return ""
        
        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            value = str((self.varstable.item(i,1)).text())
            filter = filter + "%s = '%s' AND " %(column,value)
        filter = filter[0:len(filter)-5]
        state = ", (SELECT DISTINCT %s FROM %s WHERE %s) AS B " %(vars,table1,filter)

        return state


#    def colors(self, index):
#        colorpooldict = {100:'#191970',101:'#6495ED',150:'#66FFEE', 151:'#00FFFF', # Blue Shades
#             200:'#B03060',
#             300:'#7B68EE',
#             411:'#FF0000',412:'#B30000',415:'#FFBFBF',416:'#FF8080', # Red Shades
#                         461:'#2f4f4f',462:'#696969',465:'#708090',466:'#bebebe',
#                     513:'#FF8000',514:'#B35A00', # Brown shades
#                         600:'#006400',601:'#7CFC00', # Green shades
#             900:'#000000'}
#
#        return colorpooldict[index]




#    def schedule_labels(self, index):
#        xtitle = {'activitytype':'Activity Type','strttime_rec':'Start Time','endtime_rec':'End Time',
#                  'duration_rec':'Activity Duration (mins)'}
#        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn', 151:'IH-Dependent',
#            200:'OH-Work',
#            300:'OH-School',
#            411:'OH-Pers Buss',412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',
#            461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',
#            513:'OH-Social Visit',514:'OH-Sports/Rec',
#                        600:'Pick Up',601:'Drop Off',
#            900:'OH-Other'}
#        strttime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
#        endtime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
#        duration = {1:'0-10',2:'11-30',3:'31-120',4:'121-240',5:'> 240'}
#
#        if index == 0:
#            return xtitle
#        if index == 1:
#            return activitytype
#        if index == 2:
#            return strttime
#        if index == 3:
#            return endtime
#        if index == 4:
#            return duration

    def checkColumnExists(self, tablename, columnname):
        columns = self.new_obj.get_column_list(tablename)
        try:
            columns.index(columnname)
        except:
            return False
        return True

    def fill_vari(self):
        self.choicevar1.clear()
        self.choicevar2.clear()
        vars = [""]
        if self.tripradio.isChecked():
            temp = ["starttime","endtime","tripmode","miles","occupancy","duration"]
            for i in temp:
                if self.checkColumnExists("trips_r",i):
                    vars.append(i)
        else:
            temp = ["activitytype","starttime","endtime","duration"]
            for i in temp:
                if self.checkColumnExists("schedule_final_r",i):
                    vars.append(i)

        self.choicevar1.addItems(vars)
        self.choicevar2.addItems(vars)
        
    def retrieveResult(self):
        tablename = ""
        if self.tripradio.isChecked():
            tablename = "trips_r"
        else:
            tablename = "schedule_final_r"
        
        column = self.choicevar1.currentText()
        if column == "":
            return False
        
        try:
            total = 0.0
            cond = self.time_categroy(column)
            for key in cond.keys():
                lowhigh = cond[key]
                
                filter = ""
                socio = str(self.socio_sql())
                if socio != "": 
                    if self.segment1.isChecked():
                        filter = " AND A.houseid = B.houseid"
                    else:
                        filter = " AND A.houseid = B.houseid AND A.personid = B.personid"
                    
                sql = ""   
                if len(lowhigh) > 1:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s >= %d AND A.%s < %d%s" %(tablename,socio,column,lowhigh[0],column,lowhigh[1],filter)
                else:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s = %d%s" %(tablename,socio,column,lowhigh[0],filter)
                
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                for j in data:
                    self.err1.append(key)
                    self.err2.append(j[0])
                    total = total + j[0]
                
            if self.percent.isChecked():
                for i in range(len(self.err1)):
                    self.err2[i] = 100*float(self.err2[i])/total

            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e
            
        return False
    
    def time_categroy(self,column):
        time = {1:[0,120],2:[120,300],3:[300,480],4:[480,660],5:[660,900],6:[900,1440]}
        mode = {1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],11:[11]}
        duration = {1:[0,11],2:[11,31],3:[31,121],4:[121,240],5:[240,1440]}
        miles = {1:[0,6],2:[6,16],3:[16,31],4:[31,51],5:[51,30000]}    
        occupancy = {0:[0],1:[1],2:[2],3:[3],4:[4],5:[5,30000]}
        activitytype = {100:[100],101:[101],150:[150],151:[151],200:[200],300:[300],411:[411],412:[412],
                        415:[415],416:[416],461:[461],462:[462],465:[465],466:[466],513:[513],514:[514],
                        900:[900],600:[600],601:[601]}

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
        elif column == "activitytype":
            return activitytype


    def trip_labels(self, index):
        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn',151:'IH-Dependent',200:'OH-Work',300:'OH-School',411:'OH-Pers Buss',
                        412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',
                        465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',513:'OH-Social Visit',514:'OH-Sports/Rec',900:'Other',
                        600:'Pick-up',601:'Drop-off'}                
        purposedict = {0:'Return Home',1:'Work',2:'School',3:'Pers Buss',4:'Shopping',5:'Social Visit',6:'Sports/Rec',7:'Meal',
                       8:'Serve Passgr',9:'Other'}
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup Truck',5:'Bus',6:'Train',7:'School Bus',8:'Bike',9:'Walk',
                    10:'Taxi',11:'Other'}
        strttime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        endtime = {1:'4am-6am',2:'6am-9am',3:'9am-12pm',4:'12pm-3pm',5:'3pm-7pm',6:'after 7pm'}
        occupancy = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5 or more'}
        duration = {1:'0-10',2:'11-30',3:'31-120',4:'121-240',5:'> 240'}
        miles = {1:'0-5',2:'6-15',3:'16-30',4:'31-50',5:'> 50'}
        
        if index == 2:
            return activitytype
        if index == 3:
            return purposedict
        if index == 4:
            return modedict
        if index == 5:
            return strttime
        if index == 6:
            return endtime
        if index == 7:
            return occupancy
        if index == 8:
            return duration
        if index == 9:
            return miles

    def on_draw1(self):
        """ Redraws the figure
        """     
        #if not self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0:
        self.err1 = []
        self.err2 = []          
        if self.retrieveResult():
        # clear the axes and redraw the plot anew
            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]
            
            axes.clear()
            axes.grid(True)
            N=len(self.err1)
            ind = np.arange(N)
    
            axes.set_title(self.plot_title())
            axes.bar(ind, self.err2, color='green', align='center')
            axes.set_xlabel(str(self.x_label()))
            if self.percent.isChecked():
                axes.set_ylabel("Percent (%)")
            else:
                axes.set_ylabel("Frequencies")
            #axes.set_ylim(0,100)
            
            labelsdict = self.labelsdict[str(self.choicevar1.currentText())]
            labels = []
            for label in self.err1:
                temp = label
                if label in labelsdict.keys():
                    temp = labelsdict[label]
                labels.append(temp)
                
            axes.set_xticks(ind)
            if len(labels) >= 13:
                axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_xticklabels(labels, size='x-small')
            else:
                axes.set_xticklabels(labels)
            
            Canvas.draw()
            self.makePlotTab(Canvas)
            
#            vtable = QTableWidget()
#            vtable.setColumnCount(1)
#            if self.freq.isChecked():
#                header = QTableWidgetItem(str("Frequency"))
#                vtable.setHorizontalHeaderItem(0,header)
#            else:
#                header = QTableWidgetItem(str("Percent(%)"))
#                vtable.setHorizontalHeaderItem(0,header)                
#            vtable.setRowCount(len(self.err2))
#            for i in range(len(self.err2)):
#                temp = self.err1[i]
#                temp = labelsdict[temp]
#                header = QTableWidgetItem(str(temp))
#                vtable.setVerticalHeaderItem(i,header)
#                values = QTableWidgetItem(str(self.err2[i]))
#                vtable.setItem(i,0,values)
#                
#            self.makeTableTab(vtable)

    def colors(self, index):
        colorpool = ['#0000FF','#FFFF00','#7B68EE','#FF4500','#1E90FF','#F0E68C','#87CEFA','#FFFACD',
                     '#FFD700','#4169E1','#FFA500','#6495ED','#BDB76B','#00BFFF','#FF6347','#B0E0E6',
                     '#ADFF2F','#808080','#32CD32','#C0C0C0','#00FA9A','#DCDCDC','#228B22','#006400',
                     '#696969','#00FF00','#A9A9A9','#98FB98','#D3D3D3','#3CB371']
        return colorpool[index]

    def x_axe_new(self):
        table = ""
        if self.tripradio.isChecked():
            table = "trips_r"
        else:
            table = "schedule_final_r"
        
        column1 = self.choicevar1.currentText()
        column2 = self.choicevar2.currentText()
        try:
            cond = self.time_categroy(column2)
            for key in cond.keys():
                
                filter = ""
                socio = str(self.socio_sql())
                if socio != "": 
                    if self.segment1.isChecked():
                        filter = " AND A.houseid = B.houseid"
                    else:
                        filter = " AND A.houseid = B.houseid AND A.personid = B.personid"
                        
                lowhigh = cond[key]
                sql = ""
                if len(lowhigh) > 1:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s >= %d AND A.%s < %d AND A.%s >= 0%s" %(table,socio,column2,lowhigh[0],column2,lowhigh[1],column1,filter)
                else:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s = %d AND A.%s >= 0%s" %(table,socio,column2,lowhigh[0],column1,filter)
                    
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                for j in data:
                    self.err1.append(key)
                    self.err2.append(j[0])
            
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
            
        if self.x_axe_new():
            self.progresslabel.setText("Processing....")
            self.repaint()
            
            table = ""
            if self.tripradio.isChecked():
                table = "trips_r"
            else:
                table = "schedule_final_r"
            
            category2 = self.time_categroy(self.choicevar1.currentText())
            
            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]
            
            axes.clear()
            axes.grid(True)
            axes.set_title(self.plot_title())
            N=len(self.err1)
            ind = np.arange(N)
            
            bars = []
            cumulate = []
            for j in range(len(self.err1)):
                cumulate.append(0)
            
            i = 0       
            for key in category2.keys():
                lowhigh1 = category2[key]
                column1 = self.choicevar1.currentText()
                column2 = self.choicevar2.currentText()
                
                value1 = []
                previous = []
                for j in range(len(self.err1)):
                    value1.append(0)
                    previous.append(cumulate[j])
                    
                try:
                    category1 = self.time_categroy(column2)
                    for k in category1.keys():
                        
                        filter = ""
                        socio = str(self.socio_sql())
                        if socio != "": 
                            if self.segment1.isChecked():
                                filter = " AND A.houseid = B.houseid"
                            else:
                                filter = " AND A.houseid = B.houseid AND A.personid = B.personid"
                        
                        lowhigh2 = category1[k]
                        sql = ""
                        if len(lowhigh1) > 1 and len(lowhigh2) > 1:
                            sql = "SELECT count(*) FROM %s AS A %sWHERE (A.%s >= %d AND A.%s < %d) AND A.%s >= %d AND A.%s < %d%s" %(table,socio,column1,lowhigh1[0],column1,lowhigh1[1],column2,lowhigh2[0],column2,lowhigh2[1],filter)
                        elif len(lowhigh1) > 1 and len(lowhigh2) < 2:
                            sql = "SELECT count(*) FROM %s AS A %sWHERE (A.%s >= %d AND A.%s < %d) AND A.%s = %d%s" %(table,socio,column1,lowhigh1[0],column1,lowhigh1[1],column2,lowhigh2[0],filter)
                        elif len(lowhigh1) < 2 and len(lowhigh2) > 1:
                            sql = "SELECT count(*) FROM %s AS A %sWHERE (A.%s = %d) AND A.%s >= %d AND A.%s < %d%s" %(table,socio,column1,lowhigh1[0],column2,lowhigh2[0],column2,lowhigh2[1],filter)                             
                        else:
                            sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s = %d AND A.%s = %d%s" %(table,socio,column1,lowhigh1[0],column2,lowhigh2[0],filter)
                        
                        self.cursor.execute(sql)
                        data = self.cursor.fetchall()
                        for t in data:
                            index = self.err1.index(k)
                            if self.err2[index] <> 0:
                                value1[index] = 100*float(t[0])/self.err2[index]
                                cumulate[index] = cumulate[index] + value1[index]
                            else:
                                value1[index] = 0                   

                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e
    
                colors = self.colors(i)
                if i == 0:
                    temp = axes.bar(ind, value1, color=colors, align='center')
                    bars.append(temp[0])
                else:
                    temp = axes.bar(ind, value1, color=colors, align='center', bottom=previous)
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

                
            axes.set_xticks(ind)
            if len(labels) >= 13:
                axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_xticklabels(labels, size='x-small')
            else:
                axes.set_xticklabels(labels)
            
            legenddict = self.labelsdict[str(self.choicevar1.currentText())]
            legendlabel = []
            for label in category2:
                temp = label
                if label in legenddict.keys():
                    temp = legenddict[label]
                legendlabel.append(temp)

                
            axes.legend(bars,legendlabel,prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
            axes.set_xlabel(str(self.x_label()))
            axes.set_ylabel("Percent (%)")
            axes.set_ylim(0,100)
                    
            Canvas.draw()
            self.makePlotTab(Canvas)
            self.progresslabel.setText("")

    def gohome(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            tool = self.toolbars[index]
            tool.home()

    def zoom(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            tool = self.toolbars[index]
            tool.zoom()

    def panzoom(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            tool = self.toolbars[index]
            tool.pan()




def main():
    app = QApplication(sys.argv)
    diag = MakeResultPlot(None, None)
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
