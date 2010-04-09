from long_term_models import *
from fixed_activity_models import *
from vehicle_ownership_models import *
from fixed_activity_prism_models import *
from activity_skeleton_reconciliation_system import *
from activity_travel_reconciliation_system import *
from child_daily_status_and_allocation_model import *
from adult_daily_status_model import *
from activity_travel_pattern_simulator import *

class Models(QWidget):
    def __init__(self, parent = None):
        super(Models, self).__init__(parent)
        # Define a global var named "model_widget" to ues in the each function as a parent widget
        global model_widget
        model_widget = parent
        
    def long_term_models(self):
        self.long_term_models = LongTermModels(model_widget)
        self.long_term_models.show()

    def fixed_activity_models(self):
        self.fixed_activity_models = FixedActivityModels(model_widget)
        self.fixed_activity_models.show()

    def vehicle_ownership_models(self):
        self.vehicle_ownership_models = VehicleOwnershipModels(model_widget)
        self.vehicle_ownership_models.show()

    def fixed_activity_prism_models(self):
        self.fixed_activity_prism_models = FixedActivityPrismModels(model_widget)
        self.fixed_activity_prism_models.show()

    def skeleton_reconciliation_system(self):
        self.skeleton_reconciliation_system = Skeleton_Reconciliation_System(model_widget)
        self.skeleton_reconciliation_system.show()

    def travel_reconciliation_system(self):
        self.travel_reconciliation_system = Travel_Reconciliation_System(model_widget)
        self.travel_reconciliation_system.show()

    def child_model(self):
        self.child_model = Child_Model(model_widget)
        self.child_model.show()

    def adult_model(self):
        self.adult_model = Adult_Model(model_widget)
        self.adult_model.show()

    def activity_travel_pattern_simulator(self):
        self.activity_travel_pattern_simulator = Activity_Travel_Pattern_Simulator(model_widget)
        self.activity_travel_pattern_simulator.show()
