from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *



class Model_Manager_Treewidget(QWidget):
    def __init__(self, parent = None):
        super(Model_Manager_Treewidget, self).__init__(parent)
        self.models = Models(parent)

#Define long term models
        
        long_term_models = QTreeWidgetItem(parent)
        long_term_models.setText(0, "Long Term Choices")
        #self.connect(long_term_models, SIGNAL('clicked()'),
        #            qApp, self.models.long_term_models)

        generate_synthetic_population = QTreeWidgetItem(long_term_models)
        generate_synthetic_population.setText(0, "Generate Synthetic Population")

        labor_force_participation_model = QTreeWidgetItem(long_term_models)
        labor_force_participation_model.setText(0, "Labor Force Participation Model")

        number_of_jobs = QTreeWidgetItem(long_term_models)
        number_of_jobs.setText(0, "Identify the number of jobs")

        primary_worker = QTreeWidgetItem(long_term_models)
        primary_worker.setText(0, "Primary worker in the household")

        school_status = QTreeWidgetItem(long_term_models)
        school_status.setText(0, "School status of everyone")

        residential_location_choice = QTreeWidgetItem(long_term_models)
        residential_location_choice.setText(0, "Residential Location Choice")


#Define fixed activity location choice generator
        
        fixed_activity_models = QTreeWidgetItem(parent)
        fixed_activity_models.setText(0, "Fixed Activity Location Choice Generator")

        vehicle_ownership_models = QTreeWidgetItem(parent)
        vehicle_ownership_models.setText(0, "Vehicle Ownership Model")

        fixed_activity_prism_models = QTreeWidgetItem(parent)
        fixed_activity_prism_models.setText(0, "Fixed Activity Prism Generator")
        

        child_model = QTreeWidgetItem(parent)
        child_model.setText(0, "Child Daily Status and Allocation Model")
        

        adult_model = QTreeWidgetItem(parent)
        adult_model.setText(0, "Adult Daily Status Model")
        

        skeleton_reconciliation_system = QTreeWidgetItem(parent)
        skeleton_reconciliation_system.setText(0, "Activity Skeleton Reconciliation System")
        

        activity_travel_pattern_simulator = QTreeWidgetItem(parent)
        activity_travel_pattern_simulator.setText(0, "Activity Travel Pattern Simulator")
        

        travel_reconciliation_system = QTreeWidgetItem(parent)
        travel_reconciliation_system.setText(0, "Activity Travel Reconciliation System")
        

        time_use_utility_calculator = QTreeWidgetItem(parent)
        time_use_utility_calculator.setText(0, "Time Use Utility Calculator")
        

        
        
