import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from model_manager.models import *
from model_manager.model_manager_treewidget import *

from file_menu.newproject import *
from file_menu.openproject import *
from file_menu.saveproject import *
from file_menu.databaseconfig import *


from openamos.core.config import *
from openamos.core.run.simulation_manager import ComponentManager

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("OpenAMOS: Version-1.0")
        self.showMaximized()
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon('images/run.png'))


        # Variable for a project properties; can be used to see if a project is open or not
        self.proconfig = None
        
        # Defining central widget
        self.centralwidgetscroll = QScrollArea()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidgetscroll)
        self.centralwidget.setFixedSize(1140, 1200)
        self.centralwidgetscroll.setWidget(self.centralwidget)

        # Defining status bar        
        self.sizelabel = QLabel()
        self.sizelabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizelabel)
        status.showMessage("Ready", 5000)

        
        # Defining manager widget
        # Setting all_manager_dock_widget
        all_manager_dock_widget = QDockWidget(self.centralwidget)
        splitter = QSplitter(Qt.Vertical)
        all_manager_dock_widget.setWidget(splitter)
        all_manager_dock_widget.setObjectName("all_manager_dock_widget")
        all_manager_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, all_manager_dock_widget)


        # Defining model_management as a QTreeWidget
        self.model_management = Model_Manager_Treewidget()
        self.model_management.setObjectName("model_management")
        self.model_management.headerItem().setText(0, "Model Management")
        self.model_management.setMinimumSize(50,50)
        self.connect(self.model_management, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.showflowchart)


        # Defining data_management as a QTreeWidget
        self.data_management = QTreeWidget()
        self.data_management.setObjectName("data_management")
        self.data_management.headerItem().setText(0, "Data Management")
        self.data_management.setMinimumSize(50,50)


        # Adding model_management and data_management to all_manager_dock_widget
        splitter.addWidget(self.model_management)
        splitter.addWidget(self.data_management)


        # Call the class Models
        self.models = Models(self.centralwidget)
        
        #Method to disable menus and graphics based on whether a project is open or not
        self.checkProject()


# FILE MENU
# Defining menu
    # Defining File
        self.fileMenu = self.menuBar().addMenu("&File")
        project_new_action = self.createaction("&New Project", self.projectnew, QKeySequence.New, 
                                            "projectnew", "Create a new OpenAMOS project.")

        project_open_action = self.createaction("&Open Project", self.projectopen, QKeySequence.Open, 
                                            "projectopen", "Open a new OpenAMOS project.")

        project_save_action = self.createaction("&Save Project", self.projectsave, QKeySequence.Save, 
                                              "projectsave", "Save the current OpenAMOS project.")

        project_save_as_action = self.createaction("Save Project &As...", self.projectSaveAs, "Ctrl+Shift+S",
                                                icon="projectsaveas", tip="Save the current OpenAMOS project with a new name.")

        project_close_action = self.createaction("&Close Project", self.projectClose, QKeySequence.Close,
                                                tip="Close the current OpenAMOS project.")

        project_print_action = self.createaction("&Print", None , QKeySequence.Print,
                                                tip="Print the current OpenAMOS project.")

        project_quit_action = self.createaction("&Quit", self.projectQuit, "Ctrl+Q",icon="Quit",
                                                tip="Quit OpenAMOS.")

        self.addActions(self.fileMenu, (project_new_action,project_open_action,None,project_save_action,project_save_as_action,
                                        project_print_action,None,project_close_action,project_quit_action, ))
      
    # Defining Models
        self.models_menu = self.menuBar().addMenu("&Models")

        models_interactive_ui_action = self.createaction("&Interactive UI", None, None, 
                                            None, "Chose a model in a visual form.")
        component_long_term_choices_action = self.createaction("Long Term Choices", self.models.show_long_term_models, None, 
                                            None, None)
        component_fixed_activity_location_choice_generator_action = self.createaction("Fixed Activity Location Choice Generator", self.models.show_fixed_activity_models, None, 
                                            None, None)
        component_vehicle_ownership_model_action = self.createaction("Vehicle Ownership Model", self.models.show_vehicle_ownership_models, None, 
                                            None, None)
        component_fixed_activity_prism_generator_action = self.createaction("Fixed Activity Prism Generator", self.models.show_fixed_activity_prism_models, None, 
                                            None, None)
        component_child_daily_status_and_allocation_model_action = self.createaction("Child Daily Status and Allocation Model", self.models.show_child_model, None, 
                                            None, None)
        component_adult_daily_status_model_action = self.createaction("Adult Daily Status Model", self.models.show_adult_model, None, 
                                            None, None)
        component_activity_skeleton_reconciliation_system_action = self.createaction("Activity Skeleton Reconciliation System", self.models.show_skeleton_reconciliation_system, None, 
                                            None, None)
        component_activity_travel_pattern_simulator_action = self.createaction("Activity Travel Pattern Simulator", self.models.show_activity_travel_pattern_simulator, None, 
                                            None, None)
        component_activity_travel_reconciliation_system_action = self.createaction("Activity Travel Reconciliation System", self.models.show_travel_reconciliation_system, None, 
                                            None, None)
        component_time_use_utility_calculator_action = self.createaction("Time Use Utility Calculator", None, None, 
                                            None, None)

        self.modelsComponentSubMenu = self.models_menu.addMenu("&Component")
        self.addActions(self.models_menu, (models_interactive_ui_action, ))
        self.addActions(self.modelsComponentSubMenu, (component_long_term_choices_action, component_fixed_activity_location_choice_generator_action,
                                                      component_vehicle_ownership_model_action, component_fixed_activity_prism_generator_action,
                                                       component_child_daily_status_and_allocation_model_action, component_adult_daily_status_model_action,
                                                      component_activity_skeleton_reconciliation_system_action,component_activity_travel_pattern_simulator_action,
                                                      component_activity_travel_reconciliation_system_action,component_time_use_utility_calculator_action))

    # Defining Data
        self.data_menu = self.menuBar().addMenu("&Data")
        data_import_action = self.createaction("Import data", None, None,
                                            "import", "Import data.")
        data_export_action = self.createaction("Export data", None, None,
                                            "export", "Export data.")
        data_dataconfig_action = self.createaction("Database Configuration", self.databaseconfiguration, None,
                                                 None, "Database Configuration", False, True)
        self.addActions(self.data_menu, (data_import_action, data_export_action,data_dataconfig_action,))

    # Defining Display
        self.display_menu = self.menuBar().addMenu("D&isplay")
        display_zoom_in_action = self.createaction("Zoom &In",None,None,
                                               "viewmag+", "Zoom in.")
        display_zoom_out_action = self.createaction("Zoom &Out",None,None,
                                               "viewmag-", "Zoom out.")
        self.addActions(self.display_menu, (display_zoom_in_action,display_zoom_out_action,))

    # Defining Run
        self.run_menu = self.menuBar().addMenu("&Run")
        run_simulation_action = self.createaction("&Simulation", self.run_simulation, None, 
                                            "run", "Implement the model.", False, True)        
        setting_preference_action = self.createaction("&Preference", None, None, 
                                            "preferences", "Make a configuration.")        
        self.addActions(self.run_menu, (setting_preference_action, ))
        self.addActions(self.run_menu, (run_simulation_action, ))

    # Defining help        
        self.help_menu = self.menuBar().addMenu("&Help")
        help_about_action = self.createaction("&About OpenAMOS", None, None, 
                                            None, "Display software information.")        
        help_documentation_action = self.createaction("&Documentation", None, None, 
                                            None, "Quick reference for important parameters.")        
        self.addActions(self.help_menu, (help_documentation_action,None,help_about_action,  ))
 
# Defining toolbar
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("FileToolBar")
        self.addActions(self.fileToolBar, (project_new_action, project_open_action,
                                           project_save_action, display_zoom_in_action,
                                           display_zoom_out_action,))

# Define Action
    def createaction(self, text, slot=None, shortcut=None, icon=None, 
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

# Show flowcharts from model management tree widget
    def showflowchart(self,selitem,col):
        if selitem.text(col) == 'Long Term Choices':
            self.models.show_long_term_models()
        if selitem.text(col) == 'Fixed Activity Location Choices':
            self.models.show_fixed_activity_models()
        if selitem.text(col) == 'Vehicle Ownership Model':
            self.models.show_vehicle_ownership_models()
        if selitem.text(col) == 'Fixed Activity Prism Generator':
            self.models.show_fixed_activity_prism_models()
        if selitem.text(col) == 'Child Daily Status and Allocation Model':
            self.models.show_child_model()
        if selitem.text(col) == 'Adult Daily Status Model':
            self.models.show_adult_model()
        if selitem.text(col) == 'Activity Skeleton Reconciliation System':
            self.models.show_skeleton_reconciliation_system()
        if selitem.text(col) == 'Activity Travel Pattern Simulator':
            self.models.show_activity_travel_pattern_simulator()
        if selitem.text(col) == 'Activity Travel Reconciliation System':
            self.models.show_travel_reconciliation_system()



# Call file functions
    def projectnew(self):
        project_new = NewProject()
        project_new.exec_()
        if project_new.configtree != None:
            if self.proconfig <> None:
                Temp = self.model_management.currentItem()
                if Temp <> None:
                    Temp.setSelected(False)
                self.proconfig = None
                self.models = None
                self.centralwidget = None
                self.centralwidget = QWidget()
                self.centralwidget.setObjectName("centralwidget")        
                self.centralwidget.setFixedSize(1140, 1200)
                self.centralwidgetscroll.setWidget(self.centralwidget)
                self.models = Models(self.centralwidget)

            
            self.proconfig = ConfigObject(configtree=project_new.configtree)
            self.checkProject()
            self.data_menu.actions()[2].setEnabled(True)
            self.run_menu.actions()[1].setEnabled(True)
            

    def projectopen(self):
        if self.proconfig <> None:
            reply = QMessageBox.warning(self, "Save Existing Project...",
                                        QString("""Would you like to save the project?"""), 
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.proconfig.write()
            
        self.project_open = OpenProject()
        #print self.project_open.file
        if self.project_open.file != '':
            Temp = self.model_management.currentItem()
            if Temp <> None:
                Temp.setSelected(False)
            self.proconfig = None
            self.models = None
            self.centralwidget = None
            self.centralwidget = QWidget()
            self.centralwidget.setObjectName("centralwidget")        
            self.centralwidget.setFixedSize(1140, 1200)
            self.centralwidgetscroll.setWidget(self.centralwidget)
            self.models = Models(self.centralwidget)

            
            self.proconfig = ConfigObject(configfileloc=str(self.project_open.file))
            self.checkProject()
            self.data_menu.actions()[2].setEnabled(True)
            self.run_menu.actions()[1].setEnabled(True)
            

    def projectsave(self):
        self.proconfig.write()



    def projectSaveAs(self):
        file = QFileDialog.getSaveFileName(self, QString("Save As..."), 
                                                             "%s" %self.proconfig.getConfigElement(PROJECT_HOME), 
                                                             "XML File (*.xml)")
        
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
        self.proconfig = None
        self.checkProject()
        self.data_menu.actions()[2].setDisabled(True)
        self.run_menu.actions()[1].setDisabled(True)
        

    def projectQuit(self):
        reply = QMessageBox.question(None, 'Quit', "Are you sure to quit?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.proconfig.write()
            self.close()
            
    def checkProject(self):
        actpro = bool(self.proconfig)
        if actpro:
            self.setWindowTitle("OpenAMOS: Version-1.0 (%s)" %self.proconfig.getConfigElement(PROJECT,NAME))
        self.centralwidget.setEnabled(actpro)
        self.model_management.setConfigObject(self.proconfig)
        self.models.setConfigObject(self.proconfig)
        
    def databaseconfiguration(self):
        if self.proconfig <> None:
            project_database = DatabaseConfig(self.proconfig)
            project_database.exec_()
            
    def run_simulation(self):
        fileloc = self.proconfig.getConfigElement(PROJECT,LOCATION)
        pname = self.proconfig.getConfigElement(PROJECT,NAME)
        if fileloc <> None and fileloc <> "" and pname <> None and pname <> "":
            componentManager = ComponentManager(fileLoc = "%s/%s.xml" %(fileloc,pname))
            componentManager.establish_databaseConnection()
            componentManager.establish_cacheDatabase(fileloc, 'w')
            componentManager.run_components()
            componentManager.db.close()
#        else:
#            print "Something Wrong"
        
        
        

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SimTRAVEL")
    form = MainWindow()
    form.show()
    app.exec_()

if __name__=="__main__":
    main()
