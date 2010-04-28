'''
Created on Apr 19, 2010

@author: bsana
'''

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.gui.env import *
from spec_model_widgets import *

class AbtractSpecDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        super(AbtractSpecDialog, self).__init__(parent)
        
        self.glayout = QGridLayout()
        self.setLayout(self.glayout)
        
        self.modeltypegb = QGroupBox("Model Type")
        modeltypegblayout = QVBoxLayout()
        self.modeltypegb.setLayout(modeltypegblayout)
        self.modeltypecb = QComboBox()
        self.modeltypecb.addItems([QString(PROB_MODEL), QString(NEGBIN_MODEL),
                                   QString(SF_MODEL), QString(LOGREG_MODEL),
                                   QString(MNL_MODEL), QString(OP_MODEL),
                                   QString(NL_MODEL)])
        modeltypegblayout.addWidget(self.modeltypecb)
        self.glayout.addWidget(self.modeltypegb,0,0)

        self.subpopgb = QGroupBox("Sub-Population")
        subpoplayout = QGridLayout()
        self.subpopgb.setLayout(subpoplayout)
        tablelabel = QLabel("Table")
        subpoplayout.addWidget(tablelabel,0,0)
        self.subpoptab = QComboBox()
        self.subpoptab.addItems([QString("Table 1"), QString("Table 2")])
        subpoplayout.addWidget(self.subpoptab,1,0)
        varlabel = QLabel("Column")  
        subpoplayout.addWidget(varlabel,0,1)          
        self.subpopvar = QComboBox()
        self.subpopvar.addItems([QString("Var 1"), QString("Var 2")])
        subpoplayout.addWidget(self.subpopvar,1,1)
        oplabel = QLabel("Operator")  
        subpoplayout.addWidget(oplabel,0,2)          
        self.subpopop = QComboBox()
        self.subpopop.addItems([QString(OP_EQUAL), QString(OP_NOTEQUAL),
                                QString(OP_GT), QString(OP_LT),
                                QString(OP_GTE), QString(OP_LTE)])
        subpoplayout.addWidget(self.subpopop,1,2)
        vallabel = QLabel("Value")  
        subpoplayout.addWidget(vallabel,0,3)          
        self.subpopval = LineEdit()
        subpoplayout.addWidget(self.subpopval,1,3)
        self.glayout.addWidget(self.subpopgb,1,0)
        
        self.modwidget = QWidget()
        self.glayout.addWidget(self.modwidget,2,0)
        
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.glayout.addWidget(self.dialogButtonBox,3,0)
        
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.storeSpec)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))
        self.connect(self.modeltypecb, SIGNAL("currentIndexChanged(int)"), self.changeModelWidget)
        
        self.changeModelWidget()
    
    def changeModelWidget(self, idx=0):
        self.modwidget.setParent(None)
        if self.modeltypecb.currentText() == PROB_MODEL:
            self.modwidget = ProbModWidget(self)
        elif self.modeltypecb.currentText() == NEGBIN_MODEL:
            self.modwidget = NegBinModWidget(self)
        elif self.modeltypecb.currentText() == MNL_MODEL:
            self.modwidget = MNLogitModWidget(self)
        elif self.modeltypecb.currentText() == SF_MODEL:
            self.modwidget = SFModWidget(self)
        elif self.modeltypecb.currentText() == LOGREG_MODEL:
            self.modwidget = LogRegModWidget(self)
        elif self.modeltypecb.currentText() == OP_MODEL:
            self.modwidget = OProbitModWidget(self)
        elif self.modeltypecb.currentText() == NL_MODEL:
            self.modwidget = NLogitModWidget(self)
        
        self.glayout.addWidget(self.modwidget,2,0)
        self.update()
    
    def storeSpec(self):
        pass
    
        
def main():
    app = QApplication(sys.argv)
    diag = AbtractSpecDialog()
    diag.show()
    app.exec_()

if __name__=="__main__":
    main()        
        