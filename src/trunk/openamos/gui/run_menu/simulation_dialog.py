'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.gui.env import *

import subprocess
import sys, time, threading


class SimDialog(QDialog):

    def __init__(self, proconfig, parent=None):
        super(SimDialog, self).__init__(parent)

        self.setWindowTitle("Run Simulation")
        self.setWindowIcon(QIcon("./images/run.png"))
        self.setMinimumSize(800,600)

        self.proconfig = proconfig

        alllayout = QHBoxLayout()
        self.setLayout(alllayout)
        
        self.splitter = QSplitter(Qt.Horizontal)

        self.treewidget = QTreeWidget()
        self.treewidget.setColumnCount(3)
        self.treewidget.setHeaderLabels(["Component", "Completed", "Skip"])
        self.treewidget.setColumnWidth(0, 230)
        self.treewidget.setColumnWidth(1, 60)
        self.treewidget.setColumnWidth(2, 25)
        self.treewidget.setMinimumSize(330,50)
        self.setTreeWidget()
        
        self.splitter.addWidget(self.treewidget)
        alllayout.addWidget(self.splitter)
        
        leftwidget = QGroupBox("")
        leftlayout = QVBoxLayout()
        leftwidget.setLayout(leftlayout)
        
        

#        self.gLayout = QGridLayout()
#        self.complist = ['VehicleOwnershipModel','VehicleAttributeModels','WorkEpisodes']
#        
#        for comp in self.complist:
#            compwidget = CompStatWidget(comp,self.proconfig)
#            vLayout.addWidget(compwidget)
            
        outputLabel = QLabel("Simulation Outputs")
        leftlayout.addWidget(outputLabel)
        self.outputWindow = QTextEdit()
        leftlayout.addWidget(self.outputWindow)
        
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        leftlayout.addWidget(self.dialogButtonBox)
        
        self.splitter.addWidget(leftwidget)
        self.splitter.setStretchFactor(0,0)
        self.splitter.setStretchFactor(1,1)
        alllayout.addWidget(self.splitter)


        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))


#        self.index = 0
#        
        #runWarning = QLabel("""<font color = blue>Note: Select geographies by clicking on the <b>Select Geographies</b> button """
        #                    """and then click on <b>Run Synthesizer</b> to start synthesizing population.</font>""")
        #runWarning.setWordWrap(True)

#        self.thread = Worker()
#        self.connect(self.thread, SIGNAL("output(QString)"), self.update)
#        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        
#        self.proc = QProcess()
#        self.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self.sendOutput)
#        self.connect(self.proc, SIGNAL("readyReadStandardError()"), self.sendError)
#        self.connect(self.proc, SIGNAL("finished(int)"), self.updateUi)


    def setTreeWidget(self):
        if self.proconfig != None:
            compelts = self.proconfig.getComponents()
            for comp in compelts:

                comtitle = str(comp.get(NAME))
                if comtitle in COMPONENTMAP.keys():
                    compname = COMPONENTMAP[comp.get(NAME)][0]
                else:
                    compname = comtitle
                component_term = QTreeWidgetItem(self.treewidget)
                component_term.setText(0, compname)
                component_term.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                
                for key in comp.keys():
                    if key == "skip" or key == "completed":
                        attr = "%s"%(comp.get(key))
                        if key == "skip":
                            if attr == "True":
                                component_term.setCheckState(2, Qt.Checked)
                            else:
                                component_term.setCheckState(2, Qt.Unchecked)                     
                        else:
                            component_term.setIcon(1, QIcon("./images/%s" %(attr)))


    def reject(self):
        QDialog.accept(self)
          
    def accept(self):
        self.outputWindow.clear()
#        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
#        pname = self.proconfig.getConfigElement(PROJECT,NAME)
#        cmd = "python ../core/openamos_run.py %s/%s.xml" %(fileloc,pname)
        fileloc1 = self.proconfig.fileloc
        cmd = "python ../core/openamos_run.py %s" %(fileloc1)
        print fileloc1
        print cmd
        
        mythread = Worker(self,cmd)
        mythread.progress.connect(self.write_meg)
        mythread.start()
        
    def write_meg(self,s):
        self.outputWindow.append(s)

#    def update(self,out):
#        self.outputWindow.append(out)
#
#    def updateUi(self,ec):
#        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(True)
#        self.outputWindow.append('Process finished with exit code - %s' %ec)

#    def sendOutput(self):
#        self.index = self.index + 1
#        self.outputWindow.append(QString(self.proc.readAllStandardOutput()))        
#
#    def sendError(self):
#        self.outputWindow.append(QString(self.proc.readAllStandardError()))  

    

#    def accept(self):
#        self.outputWindow.clear()
#        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
#        pname = self.proconfig.getConfigElement(PROJECT,NAME)
#        cmd = "python ../core/openamos_run.py %s/%s.xml" %(fileloc,pname)
#        
##        self.process = Popen(cmd, shell = True,
##                  stdout = PIPE,
##                  stderr = PIPE)
#        #"python ../core/openamos_run.py C:/mag_zone/mag_zone.xml"
#        
#        #self.proc.start(QString(cmd))
#        #print self.proc.started()
#        #self.thread.initiate(cmd)
#        
#        self.dialogButtonBox.button(QDialogButtonBox.Ok).setEnabled(False)
#
##        if not self.process.startDetached (QString(cmd)):
##            self.outputWindow.setText(QString("*** Failed to run ***"))
##            return
#        
##        stdout, stderr= subprocess.Popen(cmd, shell = True, 
##                                         stdout = subprocess.PIPE,
##                                         stderr = subprocess.PIPE).communicate()
#
#        p = subprocess.Popen(cmd, shell = True,
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT)
#
#        while True:
#            line = p.stdout.readline()
#            if not line: break
#            self.outputWindow.append(QString(line))
#            sys.stdout.flush()

        
#    def enqueue_output(self, out, queue):
#        for line in iter(out.readline, ''):
#            queue.put(line)
#        out.close()



class Worker(QThread):
    progress = pyqtSignal(QString)
    
    def __init__(self, parent = None, cmd=None):
        QThread.__init__(self, parent)
        self.cmd = cmd
        #self.process = QProcess()
        #self.connect(self.process, SIGNAL("readyReadStdout()"), self.sendOutput)
        #self.connect(self.process, SIGNAL("readyReadStderr()"), self.sendErrors)
     
        
    def initiate(self,cmd,output):
        self.cmd = cmd
        self.outputWindow = output
#        self.start()

    def run(self):

#        stdout,stderr = subprocess.Popen(self.cmd, shell = False,bufsize=0, 
#                                         stdout = subprocess.PIPE,
#                                         stderr = subprocess.STDOUT ).communicate()

        p = subprocess.Popen(self.cmd, shell = True, 
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.STDOUT )

        while True:
            line = p.stdout.readline()
            if not line: break
            self.progress.emit(line)
            sys.stdout.flush()

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
#        self.proc = QProcess()
#        print "created a QProcess"
#        self.connect(self.proc, SIGNAL("readyReadStdout()"), self.sendOutput)
#        #self.connect(self.proc, SIGNAL("readyReadStderr()"), self.sendErrors)
#        print "created connections"
#        self.proc.start(QString(self.cmd))
#        print "started process..."
#
#    def sendOutput(self):
#        print "someoutput from thread"
#        self.emit(SIGNAL("output(QString)"),QString(self.process.readStdout()))
#
#    def sendErrors(self):
#        print "someerror from thread"
#        self.emit(SIGNAL("output(QString)"),QString(self.process.readLineStderr()))    
        


#class CompStatWidget(QWidget):
#    def __init__(self, compname, proconfig, parent=None):
#        super(CompStatWidget, self).__init__(parent)
#        hlayout = QHBoxLayout()
#        self.setLayout(hlayout)
#        complabel = QLabel(compname)
#        hlayout.addWidget(complabel)
#        compsimstat = proconfig.getCompSimStatus(compname)
#        completedlabel = QLabel()
#        self.skipbox = QCheckBox()
#        if compsimstat != None:
#            completedlabel.setPixmap(QPixmap("./images/%s" %(compsimstat[0])))
#            self.skipbox.setCheckState(compsimstat[1])
#            self.skipbox.setEnabled(compsimstat[0]) 
#        else:
#            completedlabel.setPixmap(QPixmap("./images/false"))
#            self.skipbox.setCheckState(False)
#            self.skipbox.setEnabled(False)          
#        hlayout.addWidget(completedlabel)
#        hlayout.addWidget(self.skipbox)


