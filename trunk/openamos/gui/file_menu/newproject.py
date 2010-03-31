from PyQt4.QtGui import *
from PyQt4.QtCore import *



class NewProject(QWizard):
    def __init__(self, parent = None):
        super(NewProject, self).__init__(parent)
        self.setWindowTitle("Project Setup Wizard")
        
        

