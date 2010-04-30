from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *
from spec_abstract_dialog import *



class Model_Manager_Treewidget(QTreeWidget):
    def __init__(self, parent = None):
        super(Model_Manager_Treewidget, self).__init__(parent)
        self.models = Models(parent)

# Define long term models
        
        long_term_models = QTreeWidgetItem(self)
        long_term_models.setText(0, "Long Term Choices")


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


# Define fixed activity location choice generator
        
        fixed_activity_models = QTreeWidgetItem(self)
        fixed_activity_models.setText(0, "Fixed Activity Location Choice Generator")

        workers = QTreeWidgetItem(fixed_activity_models)
        workers.setText(0, "Workers")

        work_location = QTreeWidgetItem(workers)
        work_location.setText(0, "Identify a primary work location")

        children_adult = QTreeWidgetItem(fixed_activity_models)
        children_adult.setText(0, "Children + Adult")

        school_location_choice = QTreeWidgetItem(children_adult)
        school_location_choice.setText(0, "School location choice")

        children_1 = QTreeWidgetItem(fixed_activity_models)
        children_1.setText(0, "Children")

        preschool_location_choice = QTreeWidgetItem(children_1)
        preschool_location_choice.setText(0, "Preschool location choice")
        
        fixed_activity_locations = QTreeWidgetItem(fixed_activity_models)
        fixed_activity_locations.setText(0, "Fixed activity locations")
        
# Define Vehicle Ownership Model

        vehicle_ownership_models = QTreeWidgetItem(self)
        vehicle_ownership_models.setText(0, "Vehicle Ownership Model")

        count_vehicles = QTreeWidgetItem(vehicle_ownership_models)
        count_vehicles.setText(0, "Count of Vehicles")

        Vehicle_body_fuel_type  = QTreeWidgetItem(vehicle_ownership_models)
        Vehicle_body_fuel_type.setText(0, "Vehicle body/fuel type")

# Define Fixed Activity Prism Models       

        fixed_activity_prism_models = QTreeWidgetItem(self)
        fixed_activity_prism_models.setText(0, "Fixed Activity Prism Generator")

        earliest_start_day = QTreeWidgetItem(fixed_activity_prism_models)
        earliest_start_day.setText(0, "Earliest start of day")

        latest_end_day = QTreeWidgetItem(fixed_activity_prism_models)
        latest_end_day.setText(0, "Latest end of day")

        worker = QTreeWidgetItem(fixed_activity_prism_models)
        worker.setText(0, "Worker")

        number_school_episodes = QTreeWidgetItem(worker)
        number_school_episodes.setText(0, "Number of school episodes")

        latest_arrival_work= QTreeWidgetItem(worker)
        latest_arrival_work.setText(0, "Latest arrival at work")

        earliest_departure_work = QTreeWidgetItem(worker)
        earliest_departure_work.setText(0, "Earliest departure from work")

        nonworker = QTreeWidgetItem(fixed_activity_prism_models)
        nonworker.setText(0, "Non-worker")


        children_adults = QTreeWidgetItem(fixed_activity_prism_models)
        children_adults.setText(0, "children adults")


        number_school_episodes = QTreeWidgetItem(children_adults)
        number_school_episodes.setText(0, "Number of school episodes")


        latest_arrival_school = QTreeWidgetItem(children_adults)
        latest_arrival_school.setText(0, "Latest arrival at school")


        earliest_departure_school = QTreeWidgetItem(children_adults)
        earliest_departure_school.setText(0, "Earliest departure from school")


        children_2 = QTreeWidgetItem(fixed_activity_prism_models)
        children_2.setText(0, "Children")

        arrival_departure_time_preschool = QTreeWidgetItem(children_2)
        arrival_departure_time_preschool.setText(0, "The arrival and departure time from Pre-school")

        time_space_prism_vertices = QTreeWidgetItem(fixed_activity_prism_models)
        time_space_prism_vertices.setText(0, "Time-space prism vertices")

# Define Child Daily Status and Allocation Model

        child_model = QTreeWidgetItem(self)
        child_model.setText(0, "Child Daily Status and Allocation Model")

        children_3 = QTreeWidgetItem(child_model)
        children_3.setText(0, "Children (0-17 years old)")

        children_school_1 = QTreeWidgetItem(child_model)
        children_school_1.setText(0, "Children (Status \55 School)")

        children_preschool_1 = QTreeWidgetItem(child_model)
        children_preschool_1.setText(0, "Children (Status \55 Pre-school)")

        children_stay_home = QTreeWidgetItem(child_model)
        children_stay_home.setText(0, "Children (Status \55 Stay home)")

        school_preschool = QTreeWidgetItem(child_model)
        school_preschool.setText(0, "Is the child going to School or Pre-school today?")

        engage_activities_independently = QTreeWidgetItem(child_model)
        engage_activities_independently.setText(0, "Can the child engage in activities independently?")
 
        engage_activities_like_adults = QTreeWidgetItem(child_model)
        engage_activities_like_adults.setText(0, "Child can engage in activities independently like adults")

        assign_child_household = QTreeWidgetItem(child_model)
        assign_child_household.setText(0, "Assign the child to household")

        children_school_2 = QTreeWidgetItem(child_model)
        children_school_2.setText(0, "Children (Status \55 School)")

        children_preschool_2 = QTreeWidgetItem(child_model)
        children_preschool_2.setText(0, "Children (Status \55 Pre-school)")

        travel_independently_to_school = QTreeWidgetItem(child_model)
        travel_independently_to_school.setText(0, "Does the child travel independently to school?")

        travel_mode_to_School = QTreeWidgetItem(child_model)
        travel_mode_to_School.setText(0, "Travel Mode to School")

        assign_drop_off_event = QTreeWidgetItem(child_model)
        assign_drop_off_event.setText(0, "Assign a drop-off event to household")

        travel_independently_from_school = QTreeWidgetItem(child_model)
        travel_independently_from_school.setText(0, "Does the child travel independently from school?")

        travel_mode_from_School = QTreeWidgetItem(child_model)
        travel_mode_from_School.setText(0, "Travel Mode from School")

        assign_pick_up_event = QTreeWidgetItem(child_model)
        assign_pick_up_event.setText(0, "Assign a pick-up event to household")

        activity_pursued_independently = QTreeWidgetItem(child_model)
        activity_pursued_independently.setText(0, "Activity pursued independently after school?")

        treat_child_like_adult = QTreeWidgetItem(child_model)
        treat_child_like_adult.setText(0, "Treat the child like an adult and generate activity-travel patterns")

        after_school_activity = QTreeWidgetItem(child_model)
        after_school_activity.setText(0, "Is there time to engage in an after school CHILD activity?")

        choice = QTreeWidgetItem(child_model)
        choice.setText(0, "Activity Type\Choice Destination Choice\Activity Duration Choice")

        activity_with_adult = QTreeWidgetItem(child_model)
        activity_with_adult.setText(0, "Flag the child as a dependent and the child engages in activity with an adult")

        more_activity = QTreeWidgetItem(child_model)
        more_activity.setText(0, "More activities")

        return_home = QTreeWidgetItem(child_model)
        return_home.setText(0, "Return Home")

        to_adult = QTreeWidgetItem(child_model)
        to_adult.setText(0, "Move to Adult Daily Status")

        
# Define Adult Daily Status Model

        adult_model = QTreeWidgetItem(self)
        adult_model.setText(0, "Adult Daily Status Model")

        children_assigned = QTreeWidgetItem(adult_model)
        children_assigned.setText(0, "Is a dependent child/children assigned to household including stay home and chauffeuring activities?")

        children_stay_home = QTreeWidgetItem(adult_model)
        children_stay_home.setText(0, "Child/Children with staying home activities")

        children_chauffeuring = QTreeWidgetItem(adult_model)
        children_chauffeuring.setText(0, "Child/Children with chauffeuring activities")

        all_working_adult = QTreeWidgetItem(children_stay_home)
        all_working_adult.setText(0, "Households with all working adults")

        assign_children_1 = QTreeWidgetItem(children_stay_home)
        assign_children_1.setText(0, "Assign all dependent children to a working adult")

        adult_work = QTreeWidgetItem(children_stay_home)
        adult_work.setText(0, "This adult works from home")

        nonworking_adult = QTreeWidgetItem(children_stay_home)
        nonworking_adult.setText(0, "Households with at least one non-working adult")

        assign_children_2 = QTreeWidgetItem(children_stay_home)
        assign_children_2.setText(0, "Assign all dependent children to one non-working adult")

        assign_children_3 = QTreeWidgetItem(children_chauffeuring)
        assign_children_3.setText(0, "Assign each dependent child to a household adult subject to the fixed activity schedule of the adult")

        check_adult = QTreeWidgetItem(adult_model)
        check_adult.setText(0, "For all other adults, check to see if the adult is worker?")

        work_today = QTreeWidgetItem(adult_model)
        work_today.setText(0, "Is an employed adult going to work today?")

        work_from_home = QTreeWidgetItem(adult_model)
        work_from_home.setText(0, "Work from home")

        go_to_work = QTreeWidgetItem(adult_model)
        go_to_work.setText(0, "Go to Work")

        no_work_episodes = QTreeWidgetItem(adult_model)
        no_work_episodes.setText(0, "No Work Episodes")


# Define Activity Skeleton Reconciliation System        

        skeleton_reconciliation_system = QTreeWidgetItem(self)
        skeleton_reconciliation_system.setText(0, "Activity Skeleton Reconciliation System")
        
        skeleton_reconciliation = QTreeWidgetItem(skeleton_reconciliation_system)
        skeleton_reconciliation.setText(0, "Activity Skeleton Reconciliation")
        
        person_constraints_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        person_constraints_1.setText(0, "Within person constraints")
        
        adjustment_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        adjustment_1.setText(0, "Adjustments to the activity skeleton based on expected Travel Time from previous day")
        

        
# Define Activity Travel Pattern Simulator
        activity_travel_pattern_simulator = QTreeWidgetItem(self)
        activity_travel_pattern_simulator.setText(0, "Activity Travel Pattern Simulator")
        
        time_slice = QTreeWidgetItem(activity_travel_pattern_simulator)
        time_slice.setText(0, "Within a time slice")
        
        children_with_activity = QTreeWidgetItem(activity_travel_pattern_simulator)
        children_with_activity.setText(0, "Children with after school dependent activities")

        activity_pursued_1 = QTreeWidgetItem(children_with_activity)
        activity_pursued_1.setText(0, "Can activity be pursued jointly with a Household member?")
        
        assign_to_non_hhold = QTreeWidgetItem(children_with_activity)
        assign_to_non_hhold.setText(0, "Activity assigned to a Non-household member comprising Joint Activity with Non-household member")
        
        assign_to_hhold = QTreeWidgetItem(children_with_activity)
        assign_to_hhold.setText(0, "Assign the activity to Household member comprising Joint Activity with household member")
        
        mode_choice_model = QTreeWidgetItem(children_with_activity)
        mode_choice_model.setText(0, "Mode choice model for intra-household joint trips with children")
        
        all_other_individuals = QTreeWidgetItem(activity_travel_pattern_simulator)
        all_other_individuals.setText(0, "All other individuals")
        
        adult_individuals = QTreeWidgetItem(all_other_individuals)
        adult_individuals.setText(0, "Adult individuals, children with independent activities")
        
        travel_time = QTreeWidgetItem(all_other_individuals)
        travel_time.setText(0, "Is travel time to next fixed activity \74 time available in the prism?")
        
        activity_choice = QTreeWidgetItem(all_other_individuals)
        activity_choice.setText(0, "Activity Type Choice; Mode-Destination Choice")
        
        actual_start_time = QTreeWidgetItem(all_other_individuals)
        actual_start_time.setText(0, "Actual start time for the activity")
        
        time_in_activity = QTreeWidgetItem(all_other_individuals)
        time_in_activity.setText(0, "Is there enough time to engage in the activity?")
        
        proceed_next_activity = QTreeWidgetItem(all_other_individuals)
        proceed_next_activity.setText(0, "Proceed to next fixed activity")
        
        mode_choice_next_activity = QTreeWidgetItem(all_other_individuals)
        mode_choice_next_activity.setText(0, "Mode Choice to the next fixed activity")
        
        hov = QTreeWidgetItem(all_other_individuals)
        hov.setText(0, "Is the mode of the trip HOV?")
        
        activity_pursued_2 = QTreeWidgetItem(all_other_individuals)
        activity_pursued_2.setText(0, "Can activity be pursued jointly with Household members?")
        
        check_if_join_activity = QTreeWidgetItem(all_other_individuals)
        check_if_join_activity.setText(0, "For each available household member, check to see if he/she will join the activity?")
        
        activity_non_hhold = QTreeWidgetItem(all_other_individuals)
        activity_non_hhold.setText(0, "Joint Activity with Non-household member")
        
        activity_hhold = QTreeWidgetItem(all_other_individuals)
        activity_hhold.setText(0, "Joint Activity with household member")
        
        sov_hov = QTreeWidgetItem(activity_travel_pattern_simulator)
        sov_hov.setText(0, "If mode is SOV or HOV Driver identify vehicle")
        
        activity_travel_pattern = QTreeWidgetItem(activity_travel_pattern_simulator)
        activity_travel_pattern.setText(0, "Activity-travel patterns for all individuals within the time-slice")
        
# Define Activity Travel Reconciliation System
        travel_reconciliation_system = QTreeWidgetItem(self)
        travel_reconciliation_system.setText(0, "Activity Travel Reconciliation System")

        pattern_reconciliation = QTreeWidgetItem(travel_reconciliation_system)
        pattern_reconciliation.setText(0, "Activity-travel Pattern Reconciliation")
        
        person_constraints_2 = QTreeWidgetItem(travel_reconciliation_system)
        person_constraints_2.setText(0, "Within person constraints")
        
        hhold_constraints = QTreeWidgetItem(travel_reconciliation_system)
        hhold_constraints.setText(0, "Within household constraints")
        
        adjustment_2 = QTreeWidgetItem(travel_reconciliation_system)
        adjustment_2.setText(0, "Duration adjustment after arrival")

        

        time_use_utility_calculator = QTreeWidgetItem(self)
        time_use_utility_calculator.setText(0, "Time Use Utility Calculator")

        self.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.dothis)

    def dothis(self,item,col):
        if item.text(col) == 'Generate Synthetic Population':
            main()
        if item.text(col) == 'Labor Force Participation Model':
            main()
        if item.text(col) == 'Identify the number of jobs':
            main()
        if item.text(col) == 'Primary worker in the household':
            main()
        if item.text(col) == 'School status of everyone':
            main()
        if item.text(col) == 'Residential Location Choice':
            main()

        

        
        
