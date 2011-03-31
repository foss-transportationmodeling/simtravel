'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, time
import random
import numpy as np
from copy import deepcopy
from openamos.gui.env import *
from openamos.core.database_management.cursor_database_connection import *
from openamos.core.database_management.database_configuration import *
from openamos.core.database_management.cursor_query_browser import *

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
        self.connect(self.choicevar1, SIGNAL("currentIndexChanged(int)"), self.manage_combo)
        self.connect(self.choicevar2, SIGNAL("currentIndexChanged(int)"), self.set_disable)


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
        two = menubar.addAction("Remove Plot")
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
            index = index//2
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
            numtab = int(tabtitle.split(" ")[1])
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
            tabtitle = self.tabs.tabText(index)
            name = str(tabtitle.split(" ")[0])
            if name == "Table":
                self.tabs.removeTab(index)
                self.tabs.removeTab(index-1)
            else:
                self.tabs.removeTab(index+1)
                self.tabs.removeTab(index)
                
            i = index//2                
            self.figs.pop(i)
            self.sketches.pop(i)
            self.axes.pop(i)
            self.toolbars.pop(i)
    
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
        self.qb_obj = QueryBrowser(self.database_config_object)
        self.new_obj.new_connection()
 
        #assigning the connection and cursor to the qb_obj
        self.qb_obj.dbcon_obj.connection = self.new_obj.connection
        self.qb_obj.dbcon_obj.cursor = self.new_obj.cursor


        
    def disconnects(self):
        self.new_obj.close_connection()
        self.close()

    def fill_vari(self):
        self.choicevar1.clear()
        self.choicevar2.clear()
        vars = [""]
        if self.tripradio.isChecked():
            temp = ["trippurpose","starttime","endtime","tripmode","miles","occupancy","duration"]
            for i in temp:
                if self.checkColumnExists("trips_r",i):
                    vars.append(i)
        else:
            temp = ["activitytype","starttime","endtime","duration"]
            for i in temp:
                if self.checkColumnExists("schedule_final_r",i):
                    vars.append(i)

        self.choicevar1.addItems(vars)
        
    def manage_combo(self):
        self.choicevar2.clear()
        vars = [""]
        if self.tripradio.isChecked():
            text = self.choicevar1.currentText()
            if text == "trippurpose":
                temp = ["tripmode","starttime","endtime","miles","occupancy","duration"]
                for i in temp:
                    if self.checkColumnExists("trips_r",i):
                        vars.append(i)
            elif text != "trippurpose" and text != "":
                temp = ["trippurpose"]
                for i in temp:
                    if self.checkColumnExists("trips_r",i):
                        vars.append(i)
        else:
            text = self.choicevar1.currentText()
            if text == "activitytype":
                temp = ["starttime","endtime","duration"]
                for i in temp:
                    if self.checkColumnExists("schedule_final_r",i):
                        vars.append(i)
            elif text != "activitytype" and text != "":
                temp = ["activitytype"]
                for i in temp:
                    if self.checkColumnExists("schedule_final_r",i):
                        vars.append(i)
        
        self.choicevar2.addItems(vars) 
            
        
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
            
            self.cursor.execute("""SELECT %s FROM %s GROUP BY %s ORDER BY %s"""%(vars,tablename,order,order))
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
        xtitle_trip = {'trippurpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
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
        xtitle_trip = {'trippurpose':'Trip Purpose','starttime':'Trip Start Time','endtime':'Trip End Time',
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
    
#    def stateSQL(self,id):
#        tablename = '%s AS A' %(self.schedule_table())
#        vars = 'A.houseid, A.personid, A.activitytype, A.starttime, (A.endtime - A.starttime)' #A.duration'
#        order = 'A.houseid, A.personid, A.starttime'
#        filter = 'A.starttime >= 0'
#        
#        if self.segment1.isChecked():
#            filter = filter + " AND A.houseid = '%s'" %(id)
#        else:
#            ids = id.split(',')
#            filter = filter + " AND A.houseid = '%s' AND A.personid = '%s'" %(ids[0],ids[1])
#            
#        state = """SELECT DISTINCT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order)
#
#        return state


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
        col_list = []
        numrows = self.varstable.rowCount()
        if numrows < 1:
#            filter = "age < 18"
#            state = ", (SELECT %s FROM %s WHERE %s) AS B " %(vars,table1,filter)
            return ""
        
        for i in range(numrows):
            column = str((self.varstable.item(i,0)).text())
            col = str(column)
            col_list.append(col)
            value = str((self.varstable.item(i,1)).text())
            filter = filter + "%s = '%s' AND " %(column,value)
        filter = filter[0:len(filter)-5]
        #filter = "wrkr = 1 AND age >= 18"
        state = ", (SELECT %s FROM %s WHERE %s) AS B " %(vars,table1,filter)

        #create an index on the col lit
        index_name = 'socio_sql_index'
        print col_list
        t1 = time.time()
        #self.qb_obj.create_index(table1, col_list, index_name)
        t2 = time.time()
        print 'time taken to create index --> %s'%(t2-t1)
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


    
    def time_categroy(self,column):
        #time = {1:[0,120],2:[120,300],3:[300,480],4:[480,660],5:[660,900],6:[900,1440]}
        time = {1:[0,60],2:[60,120],3:[120,180],4:[180,240],5:[240,300],6:[300,360],
                7:[360,420],8:[420,480],9:[480,540],10:[540,600],11:[600,660],12:[660,720],
                13:[720,780],14:[780,840],15:[840,900],16:[900,960],17:[960,1020],18:[1020,1440]}
        mode = {1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],11:[11]}
        duration = {1:[0,10],2:[10,20],3:[20,30],4:[30,50],5:[50,70],
                    6:[70,100],7:[100,150],8:[150,200],9:[200,250],10:[250,1440]}
        miles = {1:[0,5],2:[5,10],3:[10,15],4:[15,20],5:[20,25],
                 6:[25,30],7:[30,40],8:[40,50],9:[50,30000]}
        occupancy = {0:[0],1:[1],2:[2],3:[3],4:[4],5:[5,30000]}
        activitytype = {100:[100],101:[101],150:[150],151:[151],200:[200],201:[201],300:[300],301:[301],411:[411],
                        412:[412],415:[415],416:[416],461:[461],462:[462],465:[465],466:[466],513:[513],514:[514],
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
        elif column == "activitytype" or column == "trippurpose":
            return activitytype


    def trip_labels(self, column):
        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn',151:'IH-Dependent',200:'OH-Work',201:'Work',300:'OH-School',
                        301:'Shcool',411:'OH-Pers Buss',
                        412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',
                        465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',513:'OH-Social Visit',514:'OH-Sports/Rec',900:'Other',
                        600:'Pick-up',601:'Drop-off'}                
        modedict = {1:'Car',2:'Van',3:'SUV',4:'Pickup Truck',5:'Bus',6:'Train',7:'School Bus',8:'Bike',9:'Walk',
                    10:'Taxi',11:'Other'}
        starttime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                    7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                    13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        endtime = {1:'4am-5am',2:'5am-6am',3:'6am-7am',4:'7am-8am',5:'8am-9am',6:'9am-10am',
                   7:'10am-11am',8:'11am-12pm',9:'12pm-1pm',10:'1pm-2pm',11:'2pm-3pm',12:'3pm-4pm',
                   13:'4pm-5pm',14:'5pm-6pm',15:'6pm-7pm',16:'7pm-8pm',17:'8pm-9pm',18:'After 9pm'}
        occupancy = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5 or more'}
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

    def checkColumnExists(self, tablename, columnname):
        columns = self.new_obj.get_column_list(tablename)
        try:
            columns.index(columnname)
        except:
            return False
        return True
        
    def retrieveResult(self):
        tablename = ""
        if self.tripradio.isChecked():
            tablename = "trips_r"
        else:
            tablename = "schedule_final_r"
        
        column = self.choicevar1.currentText()
        if column == "":
            return False
        
        t1 = time.time()
        filter = ""
        socio = str(self.socio_sql())
        if socio != "": 
            if self.segment1.isChecked():
                filter = " AND A.houseid = B.houseid"
            else:
                filter = " AND A.houseid = B.houseid AND A.personid = B.personid"
                        
        try:
            total = 0.0
            col_list = []
            cond = self.time_categroy(column)
                        
            #convert the column into list
            col = str(column)
            col_list.append(col)
            
            #create index name
            index_name = col + '_index'
            
            #create an index on the column
            ts = time.time() 
            #self.qb_obj.create_index(tablename, col_list, index_name)
            te = time.time()
            print 'time taken to create second index --> %s'%(te-ts)
            #create the cluster on index
            
            temp = cond.keys()
            temp.sort()
            for key in temp: #cond.keys():
                lowhigh = cond[key]
                    
                sql = ""   
                if len(lowhigh) > 1:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s >= %d AND A.%s < %d%s" %(tablename,socio,column,lowhigh[0],column,lowhigh[1],filter)
                else:
                    sql = "SELECT count(*) FROM %s AS A %sWHERE A.%s = %d%s" %(tablename,socio,column,lowhigh[0],filter)
                
                print sql
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                for j in data:
                    self.err1.append(key)
                    self.err2.append(j[0])
                    total = total + j[0]
                
            if self.percent.isChecked():
                for i in range(len(self.err1)):
                    self.err2[i] = round(100*float(self.err2[i])/total,2)
            #self.qb_obj.delete_index(tablename, index_name)
            index_name1 = 'socio_sql_index'
            #self.qb_obj.delete_index('households', index_name1)
            t2 = time.time()
            print 'time taken --> %s'%(t2-t1)
            return True
        except Exception, e:
            print '\tError while fetching the columns from the table'
            print e
            
        return False

    def on_draw1(self):
        """ Redraws the figure
        """     
        #if not self.selectvar2.isChecked() and int(self.choicevar1.currentIndex())>0:
        self.progresslabel.setText("Processing....")
        self.repaint()
            
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
            axes.bar(ind, self.err2, 0.4, color='green', align='center')
            axes.set_xlabel(str(self.x_label()))
            if self.percent.isChecked():
                axes.set_ylabel("Percent (%)")
            else:
                axes.set_ylabel("Frequencies")
            #axes.set_ylim(0,100)
            
            labelsdict = self.trip_labels(str(self.choicevar1.currentText()))
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
        
        self.progresslabel.setText("")
            
        vtable = CustomTable(self)
        #vtable.setSelectionMode(QAbstractItemView.MultiSelection)
        vtable.setColumnCount(2)
        header = QTableWidgetItem(str(self.choicevar1.currentText()))
        vtable.setHorizontalHeaderItem(0,header)
        if self.freq.isChecked():
            header = QTableWidgetItem(str("Frequency"))
            vtable.setHorizontalHeaderItem(1,header)
        else:
            header = QTableWidgetItem(str("Percent(%)"))
            vtable.setHorizontalHeaderItem(1,header)                
        vtable.setRowCount(len(self.err2))
        for i in range(len(self.err2)):
            temp = self.err1[i]
            temp = labelsdict[temp]
            header = QTableWidgetItem(str(temp))
            vtable.setItem(i,0,header)
            values = QTableWidgetItem(str(self.err2[i]))
            vtable.setItem(i,1,values)
            
        self.makeTableTab(vtable)

    def colors(self, index):
        colorpool = ['#0000FF','#FFFF00','#7B68EE','#FF4500','#1E90FF','#F0E68C','#87CEFA','#FFFACD',
                     '#FFD700','#4169E1','#FFA500','#6495ED','#BDB76B','#00BFFF','#FF6347','#B0E0E6',
                     '#ADFF2F','#808080','#32CD32','#C0C0C0','#00FA9A','#DCDCDC','#228B22','#006400',
                     '#696969','#00FF00','#A9A9A9','#98FB98','#D3D3D3','#3CB371']
        return colorpool[index]
        

    def on_draw2(self):
        """ Redraws the figure
        """
        
        self.progresslabel.setText("Processing....")
        self.repaint()
        
        column1 = self.choicevar1.currentText()
        column2 = self.choicevar2.currentText()
            
        isExchange = False
        if column1 == "activitytype" or column1 == "trippurpose":
            temp = column1
            column1 = column2
            column2 = temp
            isExchange = True
            
        category2 = []
        cond = self.time_categroy(column2)
        for key in cond.keys():
            category2.append(key)
        
        category2.sort()    
        if len(category2) > 0:
            
            table = ""
            if self.tripradio.isChecked():
                table = "trips_r"
            else:
                table = "schedule_final_r"
            
            category1 = self.time_categroy(column1)
            
            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]
            
            axes.clear()
            axes.grid(True)
            axes.set_title(self.plot_title())
            
            bars = []
            cumulate = []
            if isExchange == False:
                for j in range(len(category2)):
                    cumulate.append(0)
            
            filter = ""
            socio = str(self.socio_sql())
            if socio != "": 
                if self.segment1.isChecked():
                    filter = " AND A.houseid = B.houseid"
                else:
                    filter = " AND A.houseid = B.houseid AND A.personid = B.personid"
                            
            yvalue = []
            previous = []  
            t1 = time.time()
            for key in category1.keys():
                
                lowhigh1 = category1[key]
                xvalue = []
                for j in range(len(category2)):
                    xvalue.append(0)
                    
                try:
                   
                    sql = ""
                    if len(lowhigh1) > 1:
                        sql = "SELECT count(*), A.%s FROM %s AS A %sWHERE (A.%s >= %d AND A.%s < %d)%s GROUP BY A.%s ORDER BY A.%s" %(column2,table,socio,column1,lowhigh1[0],column1,lowhigh1[1],filter,column2,column2)
                    else:
                        sql = "SELECT count(*), A.%s FROM %s AS A %sWHERE (A.%s = %d)%s GROUP BY A.%s ORDER BY A.%s" %(column2,table,socio,column1,lowhigh1[0],filter,column2,column2)                             
                    
                    print sql
                    #index_name = column1 + '_index'
                    #print index_name, list(column1)
                    #self.qb_obj.dbcon_obj.connection = self.new_obj.connection
                    #self.qb_obj.dbcon_obj.cursor = self.new_obj.cursor
                    #self.qb_obj.create_index(table, column1, index_name)
                    self.cursor.execute(sql)
                    data = self.cursor.fetchall()
                    #self.qb_obj.delete_index(table, index_name)
                    if isExchange:
                        total = 0
                        for t in data:
                            index = category2.index(int(t[1]))
                            xvalue[index] = int(t[0])
                            total = total+int(t[0])
                        
                        cumulate.append(total)
                        yvalue.append(xvalue)
                    else:    
                        for t in data:
                            index = category2.index(int(t[1]))
                            xvalue[index] = int(t[0])
                            cumulate[index] = cumulate[index] + xvalue[index]
    
                        yvalue.append(xvalue)
                        previous.append(deepcopy(cumulate))

                except Exception, e:
                    print '\tError while fetching the columns from the table'
                    print e

            t2 = time.time()
            print 'time taken is ---> %s'%(t2-t1)
            if isExchange:
                cum = []
                N=len(yvalue)
                ind = np.arange(N)
                for i in range(len(yvalue)):
                    cum.append(0)
                for i in range(len(yvalue[0])):
                    xvalue = []
                    temp = deepcopy(cum)
                    for j in range(len(yvalue)):
                        if cumulate[j] != 0:
                            value= 100.0*yvalue[j][i]/cumulate[j]
                            xvalue.append(value)
                            cum[j] = cum[j]+value
                        else:
                            xvalue.append(0)
                            cum[j]=0
                      
                    colors = self.colors(i)
                    if i == 0:
                        temp = axes.bar(ind, xvalue, 0.5, color=colors, align='center')
                        bars.append(temp[0])
                    else:
                        temp = axes.bar(ind, xvalue, 0.5, color=colors, align='center', bottom=temp)
                        bars.append(temp[0])
            else:
                N=len(yvalue[0])
                ind = np.arange(N)
                for i in range(len(yvalue)):
                    for j in range(len(yvalue[i])):
                        if cumulate[j] != 0:
                            yvalue[i][j] = 100.0*yvalue[i][j]/cumulate[j]
                            previous[i][j] = 100.0*previous[i][j]/cumulate[j]
                        
                    colors = self.colors(i)
                    if i == 0:
                        temp = axes.bar(ind, yvalue[i], 0.5, color=colors, align='center')
                        bars.append(temp[0])
                    else:
                        temp = axes.bar(ind, yvalue[i], 0.5, color=colors, align='center', bottom=previous[i-1])
                        bars.append(temp[0])

            
            prop = matplotlib.font_manager.FontProperties(size=8)
            labels = []
            if isExchange:
                labels = self.plot_legend(category1.keys(),str(self.choicevar2.currentText()))
            else:
                labels = self.plot_legend(category2,str(self.choicevar2.currentText()))
                
            axes.set_xticks(ind)
            if len(labels) >= 13:
                axes.set_xticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_xticklabels(labels, size='x-small')
            else:
                axes.set_xticklabels(labels)
            
            legendlabel = []
            if isExchange:
                legendlabel = self.plot_legend(category2,str(self.choicevar1.currentText()))
            else:
                legendlabel = self.plot_legend(category1.keys(),str(self.choicevar1.currentText()))
            
            axes.legend(bars,legendlabel,prop=prop,bbox_to_anchor=(1.01, 1),loc=2,borderaxespad=0.)
            axes.set_xlabel(str(self.x_label()))
            axes.set_ylabel("Percent (%)")
            axes.set_ylim(0,100)
                    
            Canvas.draw()
            self.makePlotTab(Canvas)
            
            vtable = CustomTable(self)
            #vtable.setSelectionMode(QAbstractItemView.MultiSelection)
            vtable.setColumnCount(len(yvalue[0]))               
            vtable.setRowCount(len(yvalue))
            for i in range(len(yvalue)):
                xvalue = yvalue[i]
                for j in range(len(xvalue)):
                    temp = 0.0
                    if isExchange:
                        if cumulate[i] != 0:
                            temp = 100.0*xvalue[j]/cumulate[i]
                        else:
                            temp = 0.0
                    else:
                        temp = xvalue[j]
                    if i==0:
                        if isExchange:
                            header = QTableWidgetItem(str(legendlabel[j]))
                            vtable.setHorizontalHeaderItem(j,header)
                        else:
                            header = QTableWidgetItem(str(labels[j]))
                            vtable.setHorizontalHeaderItem(j,header)
                    if j==0:
                        if isExchange:
                            header = QTableWidgetItem(str(labels[i]))
                            vtable.setVerticalHeaderItem(i,header)
                        else:
                            header = QTableWidgetItem(str(legendlabel[i]))
                            vtable.setVerticalHeaderItem(i,header)                        
                    value = QTableWidgetItem(str(round(temp,2)))
                    vtable.setItem(i,j,value)
                
            self.makeTableTab(vtable)
        
            
        self.progresslabel.setText("")

    def plot_legend(self,category,column):
        legenddict = self.trip_labels(str(column))
        legendlabel = []
        category.sort()
        for label in category:
            temp = label
            if label in legenddict.keys():
                temp = legenddict[label]
            legendlabel.append(temp)
                
        return legendlabel

            


    def gohome(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.home()

    def zoom(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.zoom()

    def panzoom(self):
        index = self.tabs.currentIndex()
        index = index//2
        if index >= 0:
            tool = self.toolbars[index]
            tool.pan()



class CustomTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        self.__initActions__()
        self.__initContextMenus__()

    def __initActions__(self):
        self.copyAction = QAction("Copy",  self) 
        self.copyAction.setShortcut("Ctrl+C") 
        self.addAction(self.copyAction) 
        self.connect(self.copyAction, SIGNAL("triggered()"), self.copyCells) 

    def __initContextMenus__(self): 
        self.setContextMenuPolicy(Qt.CustomContextMenu) 
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.tableWidgetContext) 

    def tableWidgetContext(self, point): 
        '''Create a menu for the tableWidget and associated actions''' 
        tw_menu = QMenu("Menu", self)  
        tw_menu.addAction(self.copyAction) 
        tw_menu.exec_(self.mapToGlobal(point)) 
        
    def copyCells(self):
        selRange  = self.selectedRanges()[0]#just take the first range 
        topRow = selRange.topRow() 
        bottomRow = selRange.bottomRow() 
        rightColumn = selRange.rightColumn() 
        leftColumn = selRange.leftColumn() 
        #item = self.tableWidget.item(topRow, leftColumn) 
        clipStr = QString() 
        for row in xrange(topRow, bottomRow+1): 
            for col in xrange(leftColumn, rightColumn+1): 
                cell = self.item(row, col) 
                if cell: 
                    clipStr.append(cell.text()) 
                else: 
                    clipStr.append(QString("")) 
                clipStr.append(QString("\t")) 
            clipStr.chop(1) 
            clipStr.append(QString("\r\n")) 
        
        cb = QApplication.clipboard() 
        cb.setText(clipStr)      


def main():
    app = QApplication(sys.argv)
    diag = MakeResultPlot(None, None)
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
