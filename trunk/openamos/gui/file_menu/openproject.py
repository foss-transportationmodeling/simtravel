from PyQt4.QtGui import *
from PyQt4.QtCore import *



class OpenProject(QWizard):
    def __init__(self, parent = None):
        super(OpenProject, self).__init__(parent)
        self.setWindowTitle("Open a peoject")
        self.showdialog()

    def showdialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                    '/home')
        file=open(filename)
