'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.core.run.simulation_manager_cursor import SimulationManager

from openamos.gui.env import *

from subprocess import Popen,PIPE,STDOUT
import sys

class SimDialog(QDialog):

    def __init__(self, proconfig, parent=None):
        super(SimDialog, self).__init__(parent)

        self.setWindowTitle("Run Simulation")
        self.setWindowIcon(QIcon("./images/run.png"))
        self.setMinimumSize(800,500)

        self.proconfig = proconfig

        vLayout = QVBoxLayout()
        self.setLayout(vLayout)

        self.gLayout = QGridLayout()
        self.complist = ['VehicleOwnershipModel','VehicleAttributeModels','WorkEpisodes']
        
        for comp in self.complist:
            compwidget = CompStatWidget(comp,self.proconfig)
            vLayout.addWidget(compwidget)
            
        outputLabel = QLabel("Output Window")
        vLayout.addWidget(outputLabel)
        self.outputWindow = QTextEdit()
        vLayout.addWidget(self.outputWindow)
        
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        vLayout.addWidget(self.dialogButtonBox)


        #runWarning = QLabel("""<font color = blue>Note: Select geographies by clicking on the <b>Select Geographies</b> button """
        #                    """and then click on <b>Run Synthesizer</b> to start synthesizing population.</font>""")
        #runWarning.setWordWrap(True)

#        self.thread = Worker()
#        self.connect(self.thread, SIGNAL("output(QString)"), self.update)
#        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        
        
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        
        self.proc = QProcess()
        self.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self.sendOutput)
        self.connect(self.proc, SIGNAL("readyReadStandardError()"), self.sendError)
        self.connect(self.proc, SIGNAL("finished(int)"), self.updateUi)

    def update(self,out):
        self.outputWindow.append(out)

    def updateUi(self,ec):
        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.outputWindow.append('Process finished with exit code - %s' %ec)

    def sendOutput(self):
        self.outputWindow.append(QString(self.proc.readAllStandardOutput()))        

    def sendError(self):
        self.outputWindow.append(QString(self.proc.readAllStandardError()))  

    def accept(self):
        self.outputWindow.clear()
        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
        pname = self.proconfig.getConfigElement(PROJECT,NAME)
        cmd = "python ../core/openamos_run.py %s/%s.xml" %(fileloc,pname)
#        self.process = Popen(cmd, shell = True,
#                  stdout = PIPE,
#                  stderr = PIPE)
        
        self.proc.start(QString(cmd))
        #print self.proc.started()
        #self.thread.initiate(cmd)
        print "Started..."
        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(False)
#        if not self.process.startDetached (QString(cmd)):
#            self.outputWindow.setText(QString("*** Failed to run ***"))
#            return

#        stdout, stderr= subprocess.Popen(cmd, shell = True, 
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.PIPE ).communicate()
                                         
#        p = subprocess.Popen(cmd, shell = True, 
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT )
#        p = subprocess.Popen(cmd)
#        while True:
#            line = p.stdout.readline()
#            if not line: break
#            self.outputWindow.append(QString(line))
#            sys.stdout.flush()
            
            


    def reject(self):
        QDialog.accept(self)

class CompStatWidget(QWidget):
    def __init__(self, compname, proconfig, parent=None):
        super(CompStatWidget, self).__init__(parent)
        hlayout = QHBoxLayout()
        self.setLayout(hlayout)
        complabel = QLabel(compname)
        hlayout.addWidget(complabel)
        compsimstat = proconfig.getCompSimStatus(compname)
        completedlabel = QLabel()
        self.skipbox = QCheckBox()
        if compsimstat != None:
            completedlabel.setPixmap(QPixmap("./images/%s" %(compsimstat[0])))
            self.skipbox.setCheckState(compsimstat[1])
            self.skipbox.setEnabled(compsimstat[0]) 
        else:
            completedlabel.setPixmap(QPixmap("./images/false"))
            self.skipbox.setCheckState(False)
            self.skipbox.setEnabled(False)          
        hlayout.addWidget(completedlabel)
        hlayout.addWidget(self.skipbox)
             
class Worker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        #self.process = QProcess()
        #self.connect(self.process, SIGNAL("readyReadStdout()"), self.sendOutput)
        #self.connect(self.process, SIGNAL("readyReadStderr()"), self.sendErrors)
     
        
    def initiate(self,cmd):
        self.cmd = cmd
        self.start()

    def run(self):

#        stdout,stderr = subprocess.Popen(self.cmd, shell = False,bufsize=0, 
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT ).communicate()
        print 'before process'
#        p = Popen(self.cmd, shell = True,
#                                         stdout = PIPE,
#                                         stderr = STDOUT)


#        while True:
#            print 'in loop'
#            line = self.proc.stdout.readline()
#            print 'after read'
#            if not line: break
#            self.emit(SIGNAL("output(QString)"),QString(line))
#            sys.stdout.flush()

#        while self.proc.poll() is None:
#            print 'in loop'
#            line = self.proc.stdout.readline()
#            self.emit(SIGNAL("output(QString)"),QString(line)) 
#            self.proc.stdout.flush()          
        self.proc = QProcess()
        print "created a QProcess"
        self.connect(self.proc, SIGNAL("readyReadStdout()"), self.sendOutput)
        #self.connect(self.proc, SIGNAL("readyReadStderr()"), self.sendErrors)
        print "created connections"
        self.proc.start(QString(self.cmd))
        print "started process..."

    def sendOutput(self):
        print "someoutput from thread"
        self.emit(SIGNAL("output(QString)"),QString(self.process.readStdout()))

    def sendErrors(self):
        print "someerror from thread"
        self.emit(SIGNAL("output(QString)"),QString(self.process.readLineStderr()))     