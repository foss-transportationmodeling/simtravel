'''
Created on Apr 19, 2010

@author: bsana
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *

class AbstractModWidget(QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(AbstractModWidget, self).__init__(parent)
        self.setTitle("Specification")
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)
        
        self.tablelist = [QString("Table1"), QString("Table2")]
        self.varlist1 = [QString("Var1"), QString("Var2")]
        self.varlist2 = [QString("Var3"), QString("Var4")]
        self.coldict = {}
        self.coldict["Table1"] = self.varlist1
        self.coldict["Table2"] = self.varlist2
    
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
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choicebutton, SIGNAL("clicked(bool)"), self.addChoice)

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

    def makeVarsWidget(self,x=0,y=1):
        self.varswidget = QWidget(self)
        self.varslayout = QVBoxLayout()
        self.varswidget.setLayout(self.varslayout)
        
        self.varsbutton = QPushButton('Add Variable')
        self.varslayout.addWidget(self.varsbutton)
        
        self.varstable = QTableWidget(0,3,self)
        self.varstable.setHorizontalHeaderLabels(['Table', 'Column', 'Coefficient'])
        self.varslayout.addWidget(self.varstable)
        
        self.mainlayout.addWidget(self.varswidget,x,y,1,3)
        self.mainlayout.setColumnStretch(1,3)
          

    def addVariable(self):
        self.varstable.insertRow(self.varstable.rowCount())
        tablebox = QComboBox()
        tablebox.addItems([QString("Table1"), QString("Table2")])
        self.varstable.setCellWidget(self.varstable.rowCount()-1, 0, tablebox)
        varbox = QComboBox()
        varbox.addItems([QString("Var1"), QString("Var2")])
        self.varstable.setCellWidget(self.varstable.rowCount()-1, 1, varbox)       


    def makeOProbitChoiceWidget(self):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebutton = QPushButton('Add Alternative')
        self.choicelayout.addWidget(self.choicebutton)
        
        self.choicetable = QTableWidget(0,2,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Threshold'])
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,0,0,1,1)
        
        self.connect(self.choicebutton, SIGNAL("clicked(bool)"), self.addOPChoice)  

    def addOPChoice(self):
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

class ProbModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(ProbModWidget, self).__init__(parent)
        self.makeProbChoiceWidget()

class NegBinModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NegBinModWidget, self).__init__(parent) 
        self.makeChoiceWidget() 
        self.makeVarsWidget() 
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)

class MNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(MNLogitModWidget, self).__init__(parent)
        self.alternatives = []
        self.specs = {}
        self.makeChoiceWidget() 
        self.makeVarsWidget() 
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addMNLVariable)
        self.connect(self.varstable, SIGNAL("cellChanged (int,int)"), self.storeVarsTable)
        self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable)

    def addMNLVariable(self):
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
                self.varstable.insertRow(self.varstable.rowCount())
                #self.specs[selalt] = copy.deepcopy(self.varstable)
                
        tablebox = QComboBox()
        tablebox.addItems([QString("Table1"), QString("Table2")])
        self.varstable.setCellWidget(self.varstable.rowCount()-1, 0, tablebox)
        varbox = QComboBox()
        varbox.addItems([QString("Var1"), QString("Var2")])
        self.varstable.setCellWidget(self.varstable.rowCount()-1, 1, varbox) 
    
    def storeVarsTable(self,x,y):
        print 'store var table'
        sellist = self.choicetable.selectedIndexes()
        selaltitem = self.choicetable.itemFromIndex(sellist[0])
        selalt = selaltitem.text()
        if selalt not in self.alternatives:
            self.alternatives.append(selalt)
        altspecs = []
        i = 0
        while i < self.varstable.rowCount():
            var = []
            tab = (self.varstable.cellWidget(i, 0)).currentIndex()
            col = (self.varstable.cellWidget(i, 1)).currentIndex()
            coeff = (self.varstable.item(i, 2)).text()
            var.append(tab)
            var.append(col)
            var.append(coeff)
            altspecs.append(var)
            i = i + 1
        self.specs[selalt] = altspecs


    def showVarsTable(self,curritem,previtem):
        print 'change var table'
        self.varstable.clearContents()
        if curritem != None:
            selalt = curritem.text()
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                tablebox = QComboBox()
                tablebox.addItems(self.tablelist)
                print altspecs[0]
                tablebox.setCurrentIndex(altspecs[0])
                self.varstable.setCellWidget(i,0,tablebox)
                colbox = QComboBox()
                colbox.addItems(self.coldict[tablebox.currentText()])
                colbox.setCurrentIndex(altspecs[1])
                self.varstable.setCellWidget(i,1,colbox)
                coeffitem = QTableWidget()
                coeffitem.setText(altspecs[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass
            #self.makeVarsWidget()
            
        #self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addMNLVariable)
        #self.connect(self.varstable, SIGNAL("cellChanged (int,int)"), self.storeVarsTable)

        
class SFModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SFModWidget, self).__init__(parent) 
        self.makeVarsWidget() 
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)

class LogRegModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(LogRegModWidget, self).__init__(parent) 
        self.makeVarsWidget() 
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)

class OProbitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(OProbitModWidget, self).__init__(parent) 
        self.makeOProbitChoiceWidget()
        self.makeVarsWidget() 
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable) 

class NLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NLogitModWidget, self).__init__(parent) 
        self.makeNestWidget()
        self.makeChoiceWidget(0, 1)
        self.makeVarsWidget(0, 2)   
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable) 