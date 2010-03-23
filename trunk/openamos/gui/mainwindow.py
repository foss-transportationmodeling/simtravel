import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
      
        self.setWindowTitle("OpenAMOS-1.0")
        self.workingWindow = QLabel()
        self.showMaximized()
        self.setMinimumSize(800,600)
        self.workingWindow.setAlignment(Qt.AlignCenter)
        self.workingWindow.setScaledContents(True)
        self.setCentralWidget(self.workingWindow)
        self.setWindowIcon(QIcon('images/run.png'))
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
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
        projectSaveAction = self.createAction("&Save Project", self.projectNew, QKeySequence.Save, 
                                              "projectsave", "Save the current OpenAMOS project.")
        projectSaveAsAction = self.createAction("Save Project &As...", self.projectSaveAs, "Ctrl+Shift+S",
                                                icon="projectsaveas", tip="Save the current OpenAMOS project with a new name.")
        projectCloseAction = self.createAction("&Close Project", self.projectClose, QKeySequence.Close,
                                                tip="Close the current OpenAMOS project.")
        projectPrintAction = self.createAction("&Print", None, QKeySequence.Print,
                                                tip="Print the current OpenAMOS project.")
        projectQuitAction = self.createAction("&Quit", self.projectQuit, "Ctrl+Q",icon="Quit",
                                                tip="Quit OpenAMOS.")

        self.addActions(self.fileMenu, (projectNewAction,projectOpenAction,None,projectSaveAction,projectSaveAsAction,
                                        projectPrintAction,None,projectCloseAction,projectQuitAction, ))
      
    # Defining Models
        self.modelsMenu = self.menuBar().addMenu("&Models")

        modelsInteractiveUIAction = self.createAction("&Interactive UI", None, None, 
                                            None, "Chose a model in a visual form.")
        componentLong_Term_ChoicesAction = self.createAction("Long Term Choices", None, None, 
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
    # Defining Setting
        self.settingMenu = self.menuBar().addMenu("&Setting")
        settingPreferenceAction = self.createAction("&Preference", None, None, 
                                            "preference", "Make a configuration.")        

        self.addActions(self.settingMenu, (settingPreferenceAction, ))
    # Defining Simulation
        self.simulationMenu = self.menuBar().addMenu("S&imulation")
        simulationRunAction = self.createAction("&Run", None, None, 
                                            "run", "Implement the model.")        
        self.addActions(self.simulationMenu, (simulationRunAction, ))
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
        self.addActions(self.fileToolBar, (projectNewAction, projectOpenAction,projectSaveAction,projectQuitAction,))

        
 


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
                                                             "PopGen File (*.pop)")
        
        file = re.split("[/.]", file)
        filename = file[-2]
        if not filename.isEmpty():
            reply = QMessageBox.warning(self, "Save Existing Project As...",
                                        QString("""Would you like to continue?"""), 
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.project.filename = filename
                self.project.save()
                self.setWindowTitle("PopGen: Version-1.1 (%s)" %self.project.name)

    
    def projectClose(self):
        self.fileManager.clear()
        self.fileManager.setEnabled(False)
        self.enableFunctions(False)
        self.project = None

    def projectQuit(self):
        self.fileManager.clear()
        self.fileManager.setEnabled(False)
        self.enableFunctions(False)
        self.project = None


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SimTRAVEL")
    form = MainWindow()
    form.show()
    app.exec_()



if __name__=="__main__":
    main()
