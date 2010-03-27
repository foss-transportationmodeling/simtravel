from PyQt4.QtGui import *
from PyQt4.QtCore import *



class Wizard(QWizard):
    def __init__(self, parent = None):
        super(Wizard, self).__init__(parent)
        self.setWindowTitle("Project Setup Wizard")
        
        
