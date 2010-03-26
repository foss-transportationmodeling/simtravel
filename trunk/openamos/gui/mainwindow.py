import os, sys, pickle, re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Long_Term_Choices import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
      
        self.setWindowTitle("OpenAMOS-1.0")
        self.workingWindow = QLabel()
        self.showMaximized()
        self.setMinimumSize(800,600)
        self.workingWindow.setAlignment(Qt.AlignCenter)

        #self.setCentralWidget(self.workingWindow)
        bkground = QPixmap("./images/background.png")
        self.setWindowIcon(QIcon('images/run.png'))
        #self.workingWindow.setPixmap(bkground)
        #self.workingWindow.setScaledContents(True)



        
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        

             
        
        allManagerDockWidget = QDockWidget("All Manager", self.centralwidget)
        splitter1 = QSplitter(Qt.Vertical)

        allManagerDockWidget.setWidget(splitter1)

        

        
        allManagerDockWidget.setObjectName("AllManagerDockWidget")
        allManagerDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, allManagerDockWidget)
        
        self.model_management = QTreeWidget()
        self.model_management.setObjectName("model_management")
        self.model_management.headerItem().setText(0, "Model Management")
        self.model_management.setMinimumSize(50,50)
        #self.model_management.setGeometry(0,0,(size.width())/2,size.height()/2)
        #self.verticalLayout.addWidget(self.model_management)

        self.data_management = QTreeWidget()
        self.data_management.setObjectName("data_management")
        self.data_management.headerItem().setText(0, "Data Management")
        self.data_management.setMinimumSize(50,50)
        #self.verticalLayout.addWidget(self.data_management)

        splitter1.addWidget(self.model_management)
        splitter1.addWidget(self.data_management)        



        #self.treeWidgetlefttop = QTreeWidget(self.centralwidget)
        #self.treeWidgetlefttop.setGeometry(QRect(40, 50, 256, 192))
        #self.treeWidgetlefttop.setObjectName("Model Management")
        #self.treeWidgetlefttop.headerItem().setText(0, "Model Management")
        #self.treeWidgetleftbottom = QTreeWidget(self.centralwidget)

        #self.treeWidgetleftbottom.setGeometry(QRect(40, 280, 256, 192))
        #self.treeWidgetleftbottom.setObjectName("Data Management")
        #self.treeWidgetleftbottom.headerItem().setText(0, "Data Management")
        

        









        #self.addworkingWindow(splitter2)
        #self.setLayout(hbox)



        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)











# FILE MENU
# Defining menu
    # Defining File
        self.fileMenu = self.menuBar().addMenu("&File")
        projectNewAction = self.createAction("&New Project", self.projectNew, QKeySequence.New, 
                                            "projectnew", "Create a new OpenAMOS project.")

        projectOpenAction = self.createAction("&Open Project", self.projectNew, QKeySequence.Open, 
                                            "projectopen", "Open a new OpenAMOS project.")

        projectSaveAction = self.createAction("&Save Project", self.projectSave, QKeySequence.Save, 
                                              "projectsave", "Save the current OpenAMOS project.")

        projectSaveAsAction = self.createAction("Save Project &As...", self.projectSaveAs, "Ctrl+Shift+S",
                                                icon="projectsaveas", tip="Save the current OpenAMOS project with a new name.")

        projectCloseAction = self.createAction("&Close Project", self.projectClose, QKeySequence.Close,
                                                tip="Close the current OpenAMOS project.")

        projectPrintAction = self.createAction("&Print", None , QKeySequence.Print,
                                                tip="Print the current OpenAMOS project.")

        projectQuitAction = self.createAction("&Quit", self.projectQuit, "Ctrl+Q",icon="Quit",
                                                tip="Quit OpenAMOS.")

        self.addActions(self.fileMenu, (projectNewAction,projectOpenAction,None,projectSaveAction,projectSaveAsAction,
                                        projectPrintAction,None,projectCloseAction,projectQuitAction, ))
      
    # Defining Models
        self.modelsMenu = self.menuBar().addMenu("&Models")

        modelsInteractiveUIAction = self.createAction("&Interactive UI", None, None, 
                                            None, "Chose a model in a visual form.")
        componentLong_Term_ChoicesAction = self.createAction("Long Term Choices", self.Long_Term_Choices, None, 
                                            None, None)
        componentFixed_Activity_Prism_GeneratorAction = self.createAction("Fixed Activity Location Choice Generator", None, None, 
                                            None, None)
        componentVehicle_Ownership_ModelAction = self.createAction("Vehicle Ownership Model", None, None, 
                                            None, None)
        componentFixed_Activity_Prism_GeneratorAction = self.createAction("Fixed Activity Prism Generator", None, None, 
                                            None, None)
        componentChild_Daily_Status_and_Allocation_ModelAction = self.createAction("Child Daily Status and Allocation Model", None, None, 
                                            None, None)
        componentAdult_Daily_Status_ModelAction = self.createAction("Adult Daily Status Model", None, None, 
                                            None, None)
        componentActivity_Skeleton_Reconciliation_SystemAction = self.createAction("Activity Skeleton Reconciliation System", None, None, 
                                            None, None)
        componentActivity_Travel_Pattern_SimulatorAction = self.createAction("Activity Travel Pattern Simulator", None, None, 
                                            None, None)
        componentActivity_Travel_Reconciliation_SystemAction = self.createAction("Activity Travel Reconciliation System", None, None, 
                                            None, None)
        componentTime_Use_Utility_CalculatorAction = self.createAction("Time Use Utility Calculator", None, None, 
                                            None, None)

        
        self.modelsComponentSubMenu = self.modelsMenu.addMenu("&Component")
        self.addActions(self.modelsMenu, (modelsInteractiveUIAction, ))
        self.addActions(self.modelsComponentSubMenu, (componentLong_Term_ChoicesAction, componentFixed_Activity_Prism_GeneratorAction,
                                                      componentVehicle_Ownership_ModelAction, componentFixed_Activity_Prism_GeneratorAction,
                                                       componentChild_Daily_Status_and_Allocation_ModelAction, componentAdult_Daily_Status_ModelAction,
                                                      componentActivity_Skeleton_Reconciliation_SystemAction,componentActivity_Travel_Pattern_SimulatorAction,
                                                      componentActivity_Travel_Reconciliation_SystemAction,componentTime_Use_Utility_CalculatorAction))


    # Defining Data
        self.dataMenu = self.menuBar().addMenu("&Data")
        dataImportAction = self.createAction("Import data", None, None,
                                            "import", "Import data.")
        dataExportAction = self.createAction("Export data", None, None,
                                            "export", "Export data.")
        self.addActions(self.dataMenu, (dataImportAction, dataExportAction,))





    # Defining Display
        self.displayMenu = self.menuBar().addMenu("D&isplay")
        displayZoomInAction = self.createAction("Zoom &In",None,None,
                                               "viewmag+", "Zoom in.")
        displayZoomOutAction = self.createAction("Zoom &Out",None,None,
                                               "viewmag-", "Zoom out.")
        self.addActions(self.displayMenu, (displayZoomInAction,displayZoomOutAction,))


    # Defining Run
        self.runMenu = self.menuBar().addMenu("&Run")
        runSimulationAction = self.createAction("&Simulation", None, None, 
                                            "run", "Implement the model.")        
        settingPreferenceAction = self.createAction("&Preference", None, None, 
                                            "preferences", "Make a configuration.")        

        self.addActions(self.runMenu, (settingPreferenceAction, ))
        self.addActions(self.runMenu, (runSimulationAction, ))
    # Defining help        
        self.helpMenu = self.menuBar().addMenu("&Help")
        helpAboutAction = self.createAction("&About OpenAMOS", None, None, 
                                            None, "Display software information.")        
        helpDocumentationAction = self.createAction("&Documentation", None, None, 
                                            None, "Quick reference for important parameters.")        
        
        self.addActions(self.helpMenu, (helpDocumentationAction,None,helpAboutAction,  ))
 
# Defining toolbar
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("FileToolBar")
        self.addActions(self.fileToolBar, (projectNewAction, projectOpenAction,
                                           projectSaveAction, displayZoomInAction,
                                           displayZoomOutAction,))

        






    def projectNew(self):
        print "a"


# Define Action
    def createAction(self, text, slot=None, shortcut=None, icon=None, 
                     tip=None, checkable=False, disabled = None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        if disabled:
            action.setDisabled(True)

        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)



    def projectSave(self):
        if self.project:
            self.project.save()


    def projectSaveAs(self):
        file = QFileDialog.getSaveFileName(self, QString("Save As..."), 
                                                             "%s" %self.project.location, 
                                                             "OpenAMOS (*.pop)")
        
        file = re.split("[/.]", file)
        filename = file[-2]
        if not filename.isEmpty():
            reply = QMessageBox.warning(self, "Save Existing Project As...",
                                        QString("""Would you like to continue?"""), 
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.project.filename = filename
                self.project.save()
                self.setWindowTitle("OpenAMOS: Version-1.0 (%s)" %self.project.name)

    
    def projectClose(self):
        self.fileManager.clear()
        self.fileManager.setEnabled(False)
        self.enableFunctions(False)
        self.project = None

    def projectQuit(self):
        reply = QMessageBox.question(None, 'Quit', "Are you sure to quit?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.deleteLater()
        else:
            event.ignore()



    def Long_Term_Choices(self):
        Long_Term_Choiceswidget = QWidget(self.centralwidget)
        #self.setGeometry(300, 300, 600, 600)
        Long_Term_Choiceswidget.setWindowTitle('Long_Term_Choices')
        #screen = QDesktopWidget().screenGeometry()
        size =  self.centralwidget.geometry()

        Generate_Synthetic_Population = QPushButton('Generate Synthetic Population', Long_Term_Choiceswidget)
        Generate_Synthetic_Population.setGeometry((size.width())/2-100, 20,200, 50)


        line = QTextEdit('a',Long_Term_Choiceswidget)
        line.setGeometry(QRect((size.width())/2, 70, 1, 20))

        self.connect(Generate_Synthetic_Population, SIGNAL('clicked()'),
                     qApp, SLOT('deleteLater()'))


        
        Labor_Force_Participation_Model = QPushButton('If worker status was not \n generated then run a Labor \n Force Participation Model to \n simulate the worker status \n individuals', Long_Term_Choiceswidget)
        Labor_Force_Participation_Model.setGeometry((size.width())/2-100, 90, 200, 90)

        line = QTextEdit('a',Long_Term_Choiceswidget)
        line.setGeometry(QRect((size.width())/2, 180, 1, 20))
        
        number_of_jobs = QPushButton('For each worker identify \n the number of jobs', Long_Term_Choiceswidget)
        number_of_jobs.setGeometry((size.width())/2-100, 200, 200, 50)

        line = QTextEdit('a',Long_Term_Choiceswidget)
        line.setGeometry(QRect((size.width())/2, 250, 1, 20))

        number_of_jobs = QPushButton('Primary worker in the \nhousehold \n\nIn the absence of data \nidentified based on personal \nincome', Long_Term_Choiceswidget)
        number_of_jobs.setGeometry((size.width())/2-100, 270, 200, 110)

        line = QTextEdit('a',Long_Term_Choiceswidget)
        line.setGeometry(QRect((size.width())/2, 380, 1, 20))

        School_status  = QPushButton('School status of everyone \nincluding those individuals \nthat are workers', Long_Term_Choiceswidget)
        School_status.setGeometry((size.width())/2-100, 400, 200, 70)

        line = QTextEdit('a',Long_Term_Choiceswidget)
        line.setGeometry(QRect((size.width())/2, 470, 1, 20))

        School_status  = QPushButton('Residential Location Choice', Long_Term_Choiceswidget)
        School_status.setGeometry((size.width())/2-100, 490, 200, 50)





        Long_Term_Choiceswidget.show()
 



        #self.deleteLater()
        #self.connect(a, SIGNAL('triggered()'), SLOT('close()'))







def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SimTRAVEL")
    form = MainWindow()
    form.show()
    app.exec_()



if __name__=="__main__":
    main()
