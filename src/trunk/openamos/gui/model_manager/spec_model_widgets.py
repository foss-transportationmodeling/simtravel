'''
Created on Apr 19, 2010

@author: bsana
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

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
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.choicetable.setSizePolicy(sizePolicy)
        self.choicelayout.addWidget(self.choicetable,)
        
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
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)


        self.varslayout.addWidget(self.varstable)
        
        self.mainlayout.addWidget(self.varswidget,x,y,1,3)
        self.mainlayout.setColumnStretch(1,3)
        
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)

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
        self.choicetable.setItem(0,1,QTableWidgetItem(0))
        disableitem = self.choicetable.item(0, 1)

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

class MNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(MNLogitModWidget, self).__init__(parent)
        self.makeChoiceWidget() 
        self.makeVarsWidget() 
        
class SFModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SFModWidget, self).__init__(parent) 
        self.makeVarsWidget() 

class LogRegModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(LogRegModWidget, self).__init__(parent) 
        self.makeVarsWidget() 

class OProbitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(OProbitModWidget, self).__init__(parent) 
        self.makeOProbitChoiceWidget()
        self.makeVarsWidget()  

class NLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NLogitModWidget, self).__init__(parent) 
        self.makeNestWidget()
        self.makeChoiceWidget(0, 1)
        self.makeVarsWidget(0, 2)    
