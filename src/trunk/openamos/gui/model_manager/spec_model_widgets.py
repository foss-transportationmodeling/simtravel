'''
Created on Apr 19, 2010

@author: bsana
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

class AbstractModWidget(QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(AbstractModWidget, self).__init__(parent)
        self.setTitle("Specification")
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)

    def makeProbChoiceWidget(self):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebutton = QPushButton('Add Alternative')
        self.choicelayout.addWidget(self.choicebutton)
        
        self.choicetable = QTableWidget(0,2,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Probability'])
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,0,0,1,1)
        
        self.connect(self.choicebutton, SIGNAL("clicked(bool)"), self.addChoice) 

    def addChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
    
    def makeChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebutton = QPushButton('Add Alternative')
        self.choicelayout.addWidget(self.choicebutton)
        
        self.choicetable = QTableWidget(self)
        self.choicetable.setRowCount(0)
        self.choicetable.setColumnCount(1)
        self.choicetable.setHorizontalHeaderLabels(['Alternatives'])
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.choicetable.setSizePolicy(sizePolicy)
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choicebutton, SIGNAL("clicked(bool)"), self.addChoice)


    def makeVarsWidget(self,x=0,y=1):
        self.varswidget = QWidget(self)
        self.varslayout = QGridLayout()
        self.varswidget.setLayout(self.varslayout)
        
        tableslabel = QLabel('Tables')
        self.varslayout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        parentdialog = self.parent()
        self.tableswidget.addItems(parentdialog.tablelist)
        self.varslayout.addWidget(self.tableswidget,1,0)
        
        varslabel = QLabel('Columns')
        self.varslayout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.varslayout.addWidget(self.colswidget,1,1)        
        
        self.varsbutton = QPushButton('>>')
        self.varslayout.addWidget(self.varsbutton,1,2)

        self.delbutton = QPushButton('Delete Row')
        self.varslayout.addWidget(self.delbutton,0,3)
        
        self.varstable = QTableWidget(0,3,self)
        self.varstable.setHorizontalHeaderLabels(['Table', 'Column', 'Coefficient'])
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varslayout.addWidget(self.varstable,1,3)
        
        self.mainlayout.addWidget(self.varswidget,x,y,1,10)
        self.mainlayout.setColumnStretch(y,5)
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateColumns)
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delVariable)

    def populateColumns(self, item):
        self.colswidget.clear()
        seltab = str(item.text())
        parentdialog = self.parent()
        self.colswidget.addItems(parentdialog.coldict[seltab])          

    def addVariable(self):     
        if (self.tableswidget.currentItem() != None) & (self.colswidget.currentItem() != None):
            self.varstable.insertRow(self.varstable.rowCount())
            currtable = (self.tableswidget.currentItem()).text()
            tableitem = QTableWidgetItem()
            tableitem.setText(currtable)
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
            
            currvar = (self.colswidget.currentItem()).text()
            varitem = QTableWidgetItem()
            varitem.setText(currvar)
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
        else:
            msg = "Please select a Table and a Column"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)            

    def delVariable(self):
        self.varstable.removeRow(self.varstable.currentRow())

    def makeOrdChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebutton = QPushButton('Add Alternative')
        self.choicelayout.addWidget(self.choicebutton)
        
        self.choicetable = QTableWidget(0,2,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Threshold'])
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choicebutton, SIGNAL("clicked(bool)"), self.addOrdChoice)  

    def addOrdChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
        self.choicetable.setItem(0,1,QTableWidgetItem())
        disableitem = self.choicetable.item(0, 1)
        disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
        disableitem.setBackgroundColor(Qt.darkGray)
        

    def makeNestWidget(self):
        self.nestwidget = QWidget(self)
        self.nestlayout = QVBoxLayout()
        self.nestwidget.setLayout(self.nestlayout)
        
        self.nestbutton = QPushButton('Add Nest')
        self.nestlayout.addWidget(self.nestbutton)
        
        self.nesttable = QTableWidget(0,2,self)
        self.nesttable.setHorizontalHeaderLabels(['Nest', 'IV Parameter'])
        self.nestlayout.addWidget(self.nesttable)
        
        self.mainlayout.addWidget(self.nestwidget,0,0,1,1)
        
        self.connect(self.nestbutton, SIGNAL("clicked(bool)"), self.addNest) 

    def addNest(self):
        self.nesttable.insertRow(self.nesttable.rowCount())
    
    def makeSFVarianceWidget(self):
        self.variancevwidget = QWidget(self)
        self.varianceuwidget = QWidget(self)
        self.variancevlayout = QHBoxLayout()
        self.varianceulayout = QHBoxLayout()
        self.variancevwidget.setLayout(self.variancevlayout)
        self.varianceuwidget.setLayout(self.varianceulayout)
        
        self.variancevlabel = QLabel('Variance (v) - Normal')
        self.varianceulabel = QLabel('Variance (u) - Half Normal')
        self.variancevlayout.addWidget(self.variancevlabel)
        self.varianceulayout.addWidget(self.varianceulabel)
        
        self.variancevline = LineEdit()
        self.variancevline.setFixedWidth(100)
        self.varianceuline = LineEdit()
        self.varianceuline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.variancevline)
        self.varianceulayout.addWidget(self.varianceuline)
        
        self.mainlayout.addWidget(self.variancevwidget,0,0,1,1,Qt.AlignLeft)
        self.mainlayout.addWidget(self.varianceuwidget,0,1,1,1,Qt.AlignLeft)

    def makeCountTypeWidget(self):
        self.poiradio = QRadioButton(POI_MODEL)
        self.nbradio = QRadioButton(NEGBIN_MODEL)
        self.nbradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.poiradio)
        buttonlayout.addWidget(self.nbradio)
        self.counttypewidget = QWidget(self)
        self.counttypewidget.setLayout(buttonlayout)
        
        self.odwidget = QWidget(self)
        odlayout = QHBoxLayout()
        self.odwidget.setLayout(odlayout)
        self.odlabel = QLabel("Overdispersion")
        odlayout.addWidget(self.odlabel)
        self.odline = LineEdit()
        self.odline.setFixedWidth(100) 
        odlayout.addWidget(self.odline)
               
        self.mainlayout.addWidget(self.counttypewidget,0,0,1,1,Qt.AlignLeft)
        self.mainlayout.addWidget(self.odwidget,0,1,1,1,Qt.AlignLeft)
        
        self.connect(self.nbradio, SIGNAL("toggled(bool)"), self.ctypeAction)

    def makeOrdTypeWidget(self):
        self.logradio = QRadioButton(LOGIT)
        self.probradio = QRadioButton(PROBIT)
        self.logradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.logradio)
        buttonlayout.addWidget(self.probradio)
        self.ordtypewidget = QWidget(self)
        self.ordtypewidget.setLayout(buttonlayout)
               
        self.mainlayout.addWidget(self.ordtypewidget,0,0,1,1,Qt.AlignLeft)
    
    def genChecks(self):
        res = True
        return res
        

class ProbModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(ProbModWidget, self).__init__(parent)
        self.makeProbChoiceWidget()
    
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class CountModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(CountModWidget, self).__init__(parent) 
        self.makeCountTypeWidget()
        self.makeChoiceWidget(1,0) 
        self.makeVarsWidget(1,1) 
         
    def ctypeAction(self, checked):
        if checked:
            self.odline.setEnabled(True) 
        else:
            self.odline.setEnabled(False)
        self.emit(SIGNAL("completeChanged()"))  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class OrderedModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(OrderedModWidget, self).__init__(parent) 
        self.makeOrdTypeWidget()
        self.makeOrdChoiceWidget(1,0)
        self.makeVarsWidget(1,1) 

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res
        
class SFModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SFModWidget, self).__init__(parent) 
        self.makeSFVarianceWidget()
        self.makeVarsWidget(1,0)  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res    

class MNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(MNLogitModWidget, self).__init__(parent)
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeChoiceWidget() 
        self.makeVarsWidget() 
        self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable)
        #self.connect(self.varstable, SIGNAL("cellChanged (int,int)"), self.storeVarsTable)
        
    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(MNLogitModWidget,self).addVariable()

    def showVarsTable(self,curritem,previtem):
        self.storeVarsTable(previtem)
        print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass    

    def storeVarsTable(self,storeitem):
        print 'store var table'
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class GCMNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(GCMNLogitModWidget, self).__init__(parent) 
        self.makeChoiceWidget()
        self.makeVarsWidget() 
        
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class LogRegModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(LogRegModWidget, self).__init__(parent) 
        self.makeVarsWidget() 

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class NLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NLogitModWidget, self).__init__(parent) 
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeNestWidget()
        self.makeChoiceWidget(0, 1)
        self.makeVarsWidget(0, 2) 
        self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable)  

    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(NLogitModWidget,self).addVariable()

    def showVarsTable(self,curritem,previtem):
        self.storeVarsTable(previtem)
        print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass    

    def storeVarsTable(self,storeitem):
        print 'store var table'
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        
        ivnests = []
        cnests = []
        i = 0
        while i < self.nesttable.rowCount():
            ivnests.append(str((self.nesttable.item(i, 0)).text()))
            i = i + 1         
        print ivnests
        i = 0
        while i < self.choicetable.rowCount():
            ch = (self.choicetable.item(i, 0)).text()
            chdet = ch.split('/')
            if len(chdet)>1:
                for j in range(len(chdet)-1):
                    cnests.append(str(chdet[j]))
            i = i + 1
        print cnests
        
        if len(cnests) == 0:
            self.errmsg = 'The choices do not have a nested structure\n'
            return False   
                
        badn = []
        for cn in cnests:
            if cn not in ivnests:
                badn.append(cn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the IV parameters for the following nests:\n' + str(badn) + '\n'
            return False

        badn = []
        for ivn in ivnests:
            if ivn not in cnests:
                badn.append(ivn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the following nests in the alternatives table:\n' + str(badn) + '\n'
            return False

        return res    
    
    