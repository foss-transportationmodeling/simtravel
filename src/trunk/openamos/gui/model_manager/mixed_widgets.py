'''
Created on May 30, 2011

@author: dhyou
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

class AbstractMixedWidget(QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(AbstractMixedWidget, self).__init__(parent)
        self.setTitle("Specification")
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)