import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from model_manager.long_term_models import *
from model_manager.fixed_activity_models import *
from model_manager.vehicle_ownership_models import *
from model_manager.fixed_activity_prism_models import *
from model_manager.activity_skeleton_reconciliation_system import *
from model_manager.activity_travel_reconciliation_system import *

from file_menu.newproject import *
from file_menu.openproject import *
from file_menu.saveproject import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("OpenAMOS-1.0")
        self.showMaximized()
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon('images/run.png'))

        # Defining central widget

        self.centralwidgetscroll = QScrollArea()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")        
        self.setCentralWidget(self.centralwidgetscroll)
        self.centralwidget.setFixedSize(1140, 903)

        self.centralwidgetscroll.setWidget(self.centralwidget)
        #size1 = self.centralwidgetscroll.geometry(self.centralwidget)
        #print size1




        # Defining status bar        
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)





        
        # Ddfining manager widget
        allManagerDockWidget = QDockWidget(self.centralwidget)
        splitter1 = QSplitter(Qt.Vertical)
        allManagerDockWidget.setWidget(splitter1)
        allManagerDockWidget.setObjectName("AllManagerDockWidget")
        allManagerDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, allManagerDockWidget)
        self.model_management = QTreeWidget()
        self.model_management.setObjectName("model_management")
        self.model_management.headerItem().setText(0, "Model Management")
        self.model_management.setMinimumSize(50,50)
        self.data_management = QTreeWidget()
        self.data_management.setObjectName("data_management")
        self.data_management.headerItem().setText(0, "Data Management")
        self.data_management.setMinimumSize(50,50)
        splitter1.addWidget(self.model_management)
        splitter1.addWidget(self.data_management)        


# FILE MENU
# Defining menu
    # Defining File
        self.fileMenu = self.menuBar().addMenu("&File")
        projectNewAction = self.createAction("&New Project", self.projectnew, QKeySequence.New, 
                                            "projectnew", "Create a new OpenAMOS project.")

        projectOpenAction = self.createAction("&Open Project", self.projectopen, QKeySequence.Open, 
                                            "projectopen", "Open a new OpenAMOS project.")

        projectSaveAction = self.createAction("&Save Project", self.projectsave, QKeySequence.Save, 
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
        componentlong_term_choicesAction = self.createAction("Long Term Choices", self.longtermmodels, None, 
                                            None, None)
        componentfixed_activity_prism_generatorAction = self.createAction("Fixed Activity Location Choice Generator", self.fixedactivitymodels, None, 
                                            None, None)
        componentvehicle_ownership_modelAction = self.createAction("Vehicle Ownership Model", self.vehicleownershipmodels, None, 
                                            None, None)
        componentFixed_Activity_Prism_GeneratorAction = self.createAction("Fixed Activity Prism Generator", self.fixedactivityprismmodels, None, 
                                            None, None)
        componentChild_Daily_Status_and_Allocation_ModelAction = self.createAction("Child Daily Status and Allocation Model", None, None, 
                                            None, None)
        componentAdult_Daily_Status_ModelAction = self.createAction("Adult Daily Status Model", None, None, 
                                            None, None)
        componentActivity_Skeleton_Reconciliation_SystemAction = self.createAction("Activity Skeleton Reconciliation System", self.skeletonreconciliationsystem, None, 
                                            None, None)
        componentActivity_Travel_Pattern_SimulatorAction = self.createAction("Activity Travel Pattern Simulator", None, None, 
                                            None, None)
        componentActivity_Travel_Reconciliation_SystemAction = self.createAction("Activity Travel Reconciliation System", self.travelreconciliationsystem, None, 
                                            None, None)
        componentTime_Use_Utility_CalculatorAction = self.createAction("Time Use Utility Calculator", None, None, 
                                            None, None)

        self.modelsComponentSubMenu = self.modelsMenu.addMenu("&Component")
        self.addActions(self.modelsMenu, (modelsInteractiveUIAction, ))
        self.addActions(self.modelsComponentSubMenu, (componentlong_term_choicesAction, componentfixed_activity_prism_generatorAction,
                                                      componentvehicle_ownership_modelAction, componentFixed_Activity_Prism_GeneratorAction,
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


    def projectnew(self):
        newwiz = NewProject()
        newwiz.exec_()
    def projectopen(self):
        newwiz = OpenProject()
        newwiz.exec_()

        

    def projectsave(self):
        newwiz = SaveProject()
        newwiz.exec_()


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


    def longtermmodels(self):
        self.longtermmodels = LongTermModels(self.centralwidget)
        self.longtermmodels.show()

    def fixedactivitymodels(self):
        self.fixedactivitymodels = FixedActivityModels(self.centralwidget)
        self.fixedactivitymodels.show()

    def vehicleownershipmodels(self):
        self.vehicleownershipmodels = VehicleOwnershipModels(self.centralwidget)
        self.vehicleownershipmodels.show()

    def fixedactivityprismmodels(self):
        self.fixedactivityprismmodels = FixedActivityPrismModels(self.centralwidget)
        self.fixedactivityprismmodels.show()

    def skeletonreconciliationsystem(self):
        self.reconciliationsystem = Skeleton_Reconciliation_System(self.centralwidget)
        self.reconciliationsystem.show()


    def travelreconciliationsystem(self):
        self.reconciliationsystem = Travel_Reconciliation_System(self.centralwidget)
        self.reconciliationsystem.show()
        

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SimTRAVEL")
    form = MainWindow()
    form.show()
    app.exec_()

if __name__=="__main__":
    main()
