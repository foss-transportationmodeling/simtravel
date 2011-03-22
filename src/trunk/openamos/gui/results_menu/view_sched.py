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


class MakeSchedPlot(QDialog):
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
        self.makeVarsWidget2()
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
        self.segment1 = QRadioButton("Households")
        self.segment1.setChecked(True)
        self.segment2 = QRadioButton("Persons")
        addsegment.addWidget(self.segment1)
        addsegment.addWidget(self.segment2)
        radiolayout.addWidget(segment)
        basedgroup = QGroupBox(self)
        basedlayout = QHBoxLayout()
        basedgroup.setLayout(basedlayout)
        self.based1 = QRadioButton("Based on Socio-Economics")
        self.based1.setChecked(True)
        self.based2 = QRadioButton("Based on ID")
        basedlayout.addWidget(self.based1)
        basedlayout.addWidget(self.based2)
        radiolayout.addWidget(basedgroup)

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
#        movebuttons = self.movebuttons()
#        self.stablelayout.addWidget(movebuttons)
        substablewidget = QWidget(self)
        substablelayout = QHBoxLayout()
        substablewidget.setLayout(substablelayout)
        stablelabel = QLabel('Schedule Type')
        substablelayout.addWidget(stablelabel)
        self.stablecombo = QComboBox()
        self.hasTables()
        self.stablecombo.setFixedWidth(250)
        substablelayout.addWidget(self.stablecombo)
        substablelayout.setAlignment(Qt.AlignLeft)
        stablelayout.addWidget(substablewidget) 
        self.resetbutton = QPushButton('Reset')
        self.resetbutton.setFixedWidth(80)
        stablelayout.addWidget(self.resetbutton)      
        self.showbutton = QPushButton('Show Chart')
        self.showbutton.setFixedWidth(80)
        stablelayout.addWidget(self.showbutton)
        stablelayout.setContentsMargins(0,0,0,0)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(radiowidget)
        self.vbox.addWidget(self.varswidget1)
        self.vbox.addWidget(self.varswidget2)
        self.vbox.addWidget(stablewidget)
        self.vbox.addWidget(self.tabs)
        self.vbox.addWidget(self.dialogButtonBox)
        self.vbox.setStretch(4,1)
        self.setLayout(self.vbox)
        
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.disconnects)
        self.connect(self.segment1, SIGNAL("clicked(bool)"), self.initTables)
        self.connect(self.segment2, SIGNAL("clicked(bool)"), self.initTables)
        self.connect(self.based1, SIGNAL("clicked(bool)"), self.showGroupBox)
        self.connect(self.based2, SIGNAL("clicked(bool)"), self.showGroupBox)
        self.connect(self.showbutton, SIGNAL("clicked(bool)"), self.on_draw1)
        self.connect(self.resetbutton, SIGNAL("clicked(bool)"), self.reset_all)
        
        if self.stablecombo.count < 1:  
            msg = "There is no simulation output"
            QMessageBox.information(self,"Warning",msg,QMessageBox.Ok)
            self.showbutton.setDisabled(True)


    def makeVarsWidget1(self):
        self.varswidget1 = QGroupBox("")
        self.varslayout = QGridLayout()
        self.varswidget1.setLayout(self.varslayout)
        self.varswidget1.setContentsMargins(0,0,0,0)
                
        tableslabel = QLabel('Columns')
        self.varslayout.addWidget(tableslabel,0,0)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        if self.columnName() <> None:
            self.colswidget.addItems(self.columnName())
        self.colswidget.setMaximumWidth(180)
        self.colswidget.setMaximumHeight(150)
        self.varslayout.addWidget(self.colswidget,1,0)
        
        varslabel = QLabel('Values')
        self.varslayout.addWidget(varslabel,0,1)
        
        self.valwidget = QListWidget()
        self.valwidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.valwidget.setMaximumWidth(180)
        self.valwidget.setMaximumHeight(150)
        self.varslayout.addWidget(self.valwidget,1,1)        
        
        buttonwidget1 = QWidget(self)
        buttonlayout1 = QVBoxLayout()
        buttonwidget1.setLayout(buttonlayout1)
        self.selbutton1 = QPushButton('>>')
        self.selbutton1.setFixedWidth(60)
        buttonlayout1.addWidget(self.selbutton1)
        self.delbutton = QPushButton('<<')
        self.delbutton.setFixedWidth(60)
        buttonlayout1.addWidget(self.delbutton)
        self.varslayout.addWidget(buttonwidget1,1,2)

        self.varstable = QTableWidget(0,2,self)
        self.varstable.setHorizontalHeaderLabels(['Column', 'Value'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.setMaximumWidth(360)
        self.varstable.setMaximumHeight(150)
        self.varslayout.addWidget(self.varstable,1,3)

        self.selbutton2 = QPushButton('Populate')
        self.selbutton2.setFixedWidth(75)
        self.varslayout.addWidget(self.selbutton2,1,4)

        self.personlabel1 = QLabel('Household ID')
        self.varslayout.addWidget(self.personlabel1,0,5)
        self.idwidget = QListWidget()
        self.idwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.idwidget.setMaximumWidth(180)
        self.idwidget.setMaximumHeight(150)
        self.varslayout.addWidget(self.idwidget,1,5)
        #self.varslayout.setContentsMargins(11,0,11,0)

        self.connect(self.colswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateValues)
        self.connect(self.selbutton1, SIGNAL("clicked(bool)"), self.selValue)
        self.connect(self.selbutton2, SIGNAL("clicked(bool)"), self.retrieveID1)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delValue)


    def makeVarsWidget2(self):
        self.varswidget2 = QGroupBox("")
        varslayout = QGridLayout()
        self.varswidget2.setLayout(varslayout)
        self.varswidget2.setContentsMargins(0,0,0,0)
        self.personlabel2 = QLabel('Household ID')
        varslayout.addWidget(self.personlabel2,0,0)
        self.idwidget2 = QListWidget()
        self.idwidget2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.idwidget2.setMaximumWidth(180)
        self.idwidget2.setMaximumHeight(150)
        varslayout.addWidget(self.idwidget2,1,0)
        varslayout.setAlignment(Qt.AlignLeft)
        self.varswidget2.setVisible(False)


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
    

    def hasTables(self):
#        isExist = False
#        if self.new_obj.check_if_table_exists("schedule_r"):
#            isExist = True
#        
#        return isExist

        tables = []
        if self.new_obj.check_if_table_exists("schedule_r"):
            tables.append("Schedules: Non-reconciled")
        if self.new_obj.check_if_table_exists("schedule_ltrec_r"):
            tables.append("Schedules: Reconciled without Travel Episodes")
        if self.new_obj.check_if_table_exists("schedule_cleanfixedactivityschedule_r"):
            tables.append("Schedules: Daily Patterns Including Full Child Episodes")
        if self.new_obj.check_if_table_exists("schedule_childreninctravelrec_r"):
            tables.append("Schedules: Reconciled Including Travel Episodes")
        if self.new_obj.check_if_table_exists("schedule_dailyallocrec_r"):
            tables.append("Schedules: Daily Pattern with Child Allocation")
        if self.new_obj.check_if_table_exists("schedule_inctravelrec_r"):
            tables.append("Schedules: Reconciled Daily Pattern Skeleton with Child Allocation")
        if self.new_obj.check_if_table_exists("schedule_final_r"):
            tables.append("Schedules: Final Schedules")
            
        self.stablecombo.addItems(tables)


    def on_context_menu(self,point):
        menubar = QMenu(self)
        one = menubar.addAction("Show Chart")
        two = menubar.addAction("Remove Current Tab")
        three = menubar.addAction("Save Plot as PNG")
        
        if self.stablecombo.count() > 0: 
            self.connect(one, SIGNAL("triggered()"),self.on_draw1)
        self.connect(two, SIGNAL("triggered()"),self.removeTab)
        self.connect(three,SIGNAL("triggered()"),self.saveimg)
        menubar.popup(self.tabs.mapToGlobal(point))

    def saveimg(self):
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(self,"Save Image","","PNG image (*.png)")
        if str(filename) != "":
            index = self.tabs.currentIndex()
            fig = self.figs[index]
            fig.savefig(str(filename))

    def makeTabs(self,chart):
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

    def removeTab(self):
        index = self.tabs.currentIndex()
        reply = QMessageBox.information(self,"Warning","Do you really want to remove?",QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
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
            
            if self.based2.isChecked():
                self.idwidget2.clear()
                self.retrieveID2()
            else:
                self.colswidget.clear()
                self.valwidget.clear()
                self.idwidget.clear()
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
            self.idwidget.clear()
            self.idwidget2.clear()
            self.delRow()
            self.table = 'households'
            self.personlabel1.setText("Household ID")
            self.personlabel2.setText("Household ID")
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())
        if self.segment2.isChecked() and self.table != 'persons':
            self.colswidget.clear()
            self.valwidget.clear()
            self.idwidget.clear()
            self.idwidget2.clear()
            self.delRow()
            self.table = 'persons'
            self.personlabel1.setText("Person ID")
            self.personlabel2.setText("Person ID")
            if self.columnName() <> None:
                self.colswidget.addItems(self.columnName())
        if self.based2.isChecked():
            if self.table == 'households':
                self.retrieveID2()
            else:
                self.retrieveID2()
                

    def showGroupBox(self):
        if self.based1.isChecked():
            self.varswidget1.setVisible(True)
            self.varswidget2.setVisible(False)
            self.idwidget2.clear()
        if self.based2.isChecked():
            self.varswidget1.setVisible(False)
            self.varswidget2.setVisible(True)
            self.valwidget.clear()
            self.delRow()
            self.idwidget.clear()
            self.retrieveID2()


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

#    def resetID(self):
#        self.idwidget2.clear()
#        self.retrieveID2()
#    def on_draw(self):
#        """ Redraws the figure
#        """
#        
##        data = [[100,0,395,300,396,332,100,729,710],
##                [100,0,325,300,326,213,415,568,34,100,669,770],
##                [100,0,149,513,159,18,101,182,5,300,258,484,100,743,696],
##                [100,0,172,101,173,1,513,199,20,416,266,49,300,367,388,412,797,41,100,885,554],
##                [100,0,302,300,303,435,101,742,10,514,775,61,101,840,0,101,841,1,100,897,542],
##                [100,0,285,300,286,312,101,602,51,101,654,59,101,714,2,412,732,68,100,879,560],
##                [100,0,158,300,237,518,101,759,0,514,799,15,412,839,15,415,887,3,100,906,533]
##                ]
#        
#        sdata = self.selectedResults()
#        if sdata != None:
#            rows = len(sdata)
#            self.axes.clear()
#            ticks = np.arange(rows+1)
#            ind = 1
#            height = 0.4
#
#
#            for row in sdata:
#                rowlen = len(row)
#                for i in range(2,rowlen,3):
#                    self.axes.barh(ind, row[i], height, left=row[i-1],color=self.colors(row[i-2]))
#                ind = ind + 1
#            
#            bars=[]
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(100)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(200)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(300)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(411)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(412)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(415)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(416)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(513)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(514)))
#            bars.append(barh(0, 1, 1, left=0,color=self.colors(900)))
#            
#            prop = matplotlib.font_manager.FontProperties(size=8)   
#            self.axes.legend(bars,('In-home','Work','School','Pers Buss',
#                              'Shopping','Meal','Srv Passgr','Social',
#                              'Sports/Rec','Other'),prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
#            self.axes.set_xlabel("Time")
#            self.axes.set_ylabel("Persons")
#            self.axes.set_xlim(0,1440)
#            
#            
#            sindex = self.idwidget.selectedIndexes()
#            labels = []
#            labels.append('')
#            for i in sindex:
#                labels.append(self.idwidget.item(i.row()).text())
#                
#            self.axes.set_yticks(ticks)
#            if len(labels) >= 13:
#                self.axes.set_yticklabels(labels, size='xx-small')
#            elif (len(labels) >= 7):
#                self.axes.set_yticklabels(labels, size='x-small')
#            else:
#                self.axes.set_yticklabels(labels)
#
#            self.canvas.draw()


#    def retrieveResults(self):
#        
#        numrows = self.varstable.rowCount()
#        if numrows > 0:
#            try:
#                self.idwidget.clear()
#                self.data = []
#                pid = []
#                temp = None
#                SQL = self.stateSQL()
#                if SQL != "" and SQL != None:
#                    #self.cursor.execute("""SELECT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order))
#                    self.cursor.execute(SQL)
#                    temp = self.cursor.fetchall()
#                    
#                    prior_id = '0'
#                    id = ""
#                    aschedule = []
#                    for i in temp:
#                        if self.segment1.isChecked():
#                            id = str(i[0])
#                        else:
#                            id = '%s,%s'%(str(i[0]),str(i[1]))
#                            
#                        if prior_id <> id:
#                            prior_id = id
#                            
#                            self.data.append(aschedule)
#                            
#                            aschedule = []
#                            pid.append(id)
#                            aschedule.append(i[2])
#                            aschedule.append(i[3])
#                            aschedule.append(i[4])
#                        else:
#                            aschedule.append(i[2])
#                            aschedule.append(i[3])
#                            aschedule.append(i[4])
#    
#                    self.data.append(aschedule)
#                    self.data.pop(0)
#                    self.fixedFifty(pid)
#                    self.idwidget.addItems(pid)
#    
#                #return data
#            
#            except Exception, e:
#                print '\tError while unloading data from the table %s'%self.table
#                print e
#                #return None
#            
#            #return None
#        else:
#            msg = "Please insert a Column and a Value after selecting"
#            QMessageBox.information(self, "Warning",
#                                    msg,
#                                    QMessageBox.Ok)


    def retrieveResults(self):
        
        pid = []
        pid.append("")
#        numrows = self.varstable.rowCount()
#        if numrows > 0:
        try:
            self.data = []
            temp = None
            
            sindex = None  #self.idwidget.selectedItems()
            if self.based1.isChecked():
                sindex = self.idwidget.selectedItems()
            else:
                sindex = self.idwidget2.selectedItems()
                
            for i in sindex:
                id = i.text()
                SQL = self.stateSQL(id)
        
                if SQL != "" and SQL != None:
                    self.cursor.execute(SQL)
                    temp = self.cursor.fetchall()
                    
                    prior_id = '0'
                    aschedule = []
                    for i in temp:
                        id = '%s,%s' %(str(i[0]),str(i[1]))
                            
                        if prior_id <> id:
                            if prior_id <> '0':
                                self.data.append(aschedule)
                            prior_id = id
                            
                            aschedule = []
                            pid.append(id)
                            aschedule.append(i[2])
                            aschedule.append(i[3])
                            aschedule.append(i[4])
                        else:
                            aschedule.append(i[2])
                            aschedule.append(i[3])
                            aschedule.append(i[4])
    
                    self.data.append(aschedule)

        
        except Exception, e:
            print '\tError while unloading data from the table %s'%self.table
            print e

#        else:
#            msg = "Please insert a Column and a Value after selecting"
#            QMessageBox.information(self, "Warning",
#                                    msg,
#                                    QMessageBox.Ok)
        
        return pid
            

    def retrieveID1(self):
        
        numrows = self.varstable.rowCount()
        if numrows > 0:
            try:
                self.idwidget.clear()
                self.data = []
                pid = []
                temp = None
                
                SQL = self.SQL_ID1()
                if SQL != "" and SQL != None:
                    #self.cursor.execute("""SELECT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order))
                    self.cursor.execute(SQL)
                    temp = self.cursor.fetchall()
                    
                    id = ""
                    for i in temp:
                        if self.segment1.isChecked():
                            id = str(i[0])
                        else:
                            id = '%s,%s'%(str(i[0]),str(i[1]))
                        
                        pid.append(id)
                        
                    self.fixedFifty(pid)
                    self.idwidget.addItems(pid)

            
            except Exception, e:
                print '\tError while unloading data from the table %s'%self.table
                print e

        else:
            msg = "Please insert a Column and a Value after selecting"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)

    def retrieveID2(self):
        
        try:
            self.idwidget2.clear()
            self.data = []
            pid = []
            temp = None

            SQL = self.SQL_ID2()  
            if SQL != "" and SQL != None:
                #self.cursor.execute("""SELECT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order))
                self.cursor.execute(SQL)
                temp = self.cursor.fetchall()
                
                id = ""
                for i in temp:
                    if self.segment1.isChecked():
                        id = str(i[0])
                    else:
                        id = '%s,%s'%(str(i[0]),str(i[1]))
                    
                    pid.append(id)
                    
                #self.fixedFifty(pid)
                self.idwidget2.addItems(pid)
        
        except Exception, e:
            print '\tError while unloading data from the table %s'%self.table
            print e




    def fixedFifty(self, pid):
        length = len(pid) #len(self.data)
        while length > 50:
            index = randint(0, length-1)
            pid.pop(index)
            #self.data.pop(index)
            length = len(pid) #len(self.data)
        

#    def stateSQL1(self):
#        tablename = 'schedule_r AS A, %s AS B' %(self.table)
#        vars = 'A.houseid, A.personid, A.activitytype, A.starttime, A.duration'
#        filter = '(A.starttime >= 0'
#        order = 'A.houseid, A.personid, A.starttime'
#        
#        numrows = self.varstable.rowCount()
#        for i in range(numrows):
#            filter = filter + " AND "
#            column = str((self.varstable.item(i,0)).text())
#            value = str((self.varstable.item(i,1)).text())
#            filter = filter + "B.%s = '%s'" %(column,value)
#            
#        filter = filter + ') AND A.houseid = B.houseid'
#        if self.table == 'persons':
#            filter = filter + ' AND A.personid = B.personid'
#        state = """SELECT DISTINCT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order)
#
#        return state

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


    def SQL_ID1(self):
        tablename = '%s AS A, %s AS B' %(self.schedule_table(),self.table)
        vars = ''
        if self.segment1.isChecked():
            vars = 'A.houseid'
        else:
            vars = 'A.houseid, A.personid'
        filter = '(A.starttime >= 0'
        order = ''
        if self.segment1.isChecked():
            order = 'A.houseid'
        else:
            order = 'A.houseid, A.personid'
        
        numrows = self.varstable.rowCount()
        for i in range(numrows):
            filter = filter + " AND "
            column = str((self.varstable.item(i,0)).text())
            value = str((self.varstable.item(i,1)).text())
            filter = filter + "B.%s = '%s'" %(column,value)
            
        filter = filter + ') AND A.houseid = B.houseid'
        if self.table == 'persons':
            filter = filter + ' AND A.personid = B.personid'
        state = """SELECT DISTINCT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order)

        return state

    def SQL_ID2(self):
        tablename = '%s AS A' %(self.schedule_table())
        vars = ''
        if self.segment1.isChecked():
            vars = 'A.houseid'
        else:
            vars = 'A.houseid, A.personid'
        filter = 'A.starttime >= 0'
        order = ''
        if self.segment1.isChecked():
            order = 'A.houseid'
        else:
            order = 'A.houseid, A.personid'
        
        state = """SELECT DISTINCT %s FROM %s WHERE %s ORDER BY %s"""%(vars,tablename,filter,order)

        return state


    def colors(self, index):
        colorpooldict = {100:'#191970',101:'#6495ED',150:'#66FFEE', 151:'#00FFFF', # Blue Shades
			 200:'#B03060',
			 300:'#7B68EE',
			 411:'#FF0000',412:'#B30000',415:'#FFBFBF',416:'#FF8080', # Red Shades
                         461:'#2f4f4f',462:'#696969',465:'#708090',466:'#bebebe',
	                 513:'#FF8000',514:'#B35A00', # Brown shades
                         600:'#006400',601:'#7CFC00', # Green shades
			 900:'#000000'}

        return colorpooldict[index]




    def schedule_labels(self, index):
        xtitle = {'activitytype':'Activity Type','strttime_rec':'Start Time','endtime_rec':'End Time',
                  'duration_rec':'Activity Duration (mins)'}
        activitytype = {100:'IH-Sojourn',101:'IH',150:'IH-Dependent Sojourn', 151:'IH-Dependent',
			200:'OH-Work',
			300:'OH-School',
			411:'OH-Pers Buss',412:'OH-Shopping',415:'OH-Meal',416:'OH-Serve Passgr',
			461:'OH-Dependent Pers Buss',462:'OH-Dependent Shopping',465:'OH-Dependent Meal',466:'OH-Dependent Serve Passgr',
			513:'OH-Social Visit',514:'OH-Sports/Rec',
                        600:'Pick Up',601:'Drop Off',
			900:'OH-Other'}
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
        
    def schedule_table(self):
        cur_text = self.stablecombo.currentText()
        if cur_text == "Schedules: Non-reconciled":
            return "schedule_r"
        elif cur_text == "Schedules: Reconciled without Travel Episodes":
            return "schedule_ltrec_r"
        elif cur_text == "Schedules: Daily Patterns Including Full Child Episodes":
            return "schedule_cleanfixedactivityschedule_r"
        elif cur_text == "Schedules: Reconciled Including Travel Episodes":
            return "schedule_childreninctravelrec_r"
        elif cur_text == "Schedules: Daily Pattern with Child Allocation":
            return "schedule_dailyallocrec_r"
        elif cur_text == "Schedules: Reconciled Daily Pattern Skeleton with Child Allocation":
            return "schedule_inctravelrec_r"
        else:
            return "schedule_final_r"

            

    def on_draw1(self):
        """ Redraws the figure
        """
        
        #sdata = self.selectedResults()
        pid = self.retrieveResults()
        if len(self.data) > 0 : #len(sdata) > 0:
            Sketch = self.createCanvas()
            Canvas = Sketch[0]
            axes = Sketch[1]
            rows = len(self.data) #len(sdata)
            axes.clear()
            ticks = np.arange(rows+1)
            ind = 0.75
            height = 0.4

            if self.segment1.isChecked():
                axes.set_title("Household Schedule")
            else:
                axes.set_title("Person Schedule")
            
            for row in self.data: #sdata:
                rowlen = len(row)
                for i in range(2,rowlen,3):
                    axes.barh(ind, row[i], height, left=row[i-1],color=self.colors(row[i-2]), picker=True)
                ind = ind + 1
            
            bars=[]
            bars.append(barh(0, 1, 1, left=0,color=self.colors(100)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(101)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(150)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(151)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(200)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(300)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(411)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(412)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(415)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(416)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(461)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(462)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(465)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(466)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(513)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(514)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(600)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(601)))
            bars.append(barh(0, 1, 1, left=0,color=self.colors(900)))
            
            prop = matplotlib.font_manager.FontProperties(size=8)   
            axes.legend(bars,('IH-Sojourn','IH', 'IH-Dependent Sojourn', 'IH-Dependent', 
			      'OH-Work','OH-School','OH-Pers Buss',
                              'OH-Shopping','OH-Meal','OH-Srv Passgr','OH-Social',
				'OH-Dependent Pers Buss','OH-Dependent Shopping','OH-Dependent Meal','OH-Dependent Serve Passgr',
                              'OH-Sports/Rec','Pick Up','Drop Off','OH-Other'),prop=prop,bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
            axes.set_xlabel("Time (mins)")
            axes.set_ylabel("Persons")
            axes.set_xlim(-1,1441)


            labels = pid                
            axes.set_yticks(ticks)
            if len(labels) >= 13:
                axes.set_yticklabels(labels, size='xx-small')
            elif (len(labels) >= 7):
                axes.set_yticklabels(labels, size='x-small')
            else:
                axes.set_yticklabels(labels)

            Canvas.draw()
#            Canvas.mpl_connect('pick_event', self.temp)
#            Canvas.mpl_connect('button_press_event', self.zooming)
            self.makeTabs(Canvas)
            
        else:
            msg = "Please select person or household ID"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)


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

#    def movedown(self):
#        index = self.tabs.currentIndex()
#        Canvas = self.sketches[index]
#        axes = self.axes[index]
#        ymin, ymax = axes.get_ylim()
#        axes.set_ylim(ymin-0.1,ymax-0.1)
#        Canvas.draw()



def main():
    app = QApplication(sys.argv)
    diag = MakeSchedPlot(None, None)
    diag.show()
    app.exec_()

if __name__ == "__main__":
    main()
