from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class Model_Manager_Treewidget(QTreeWidget):
    def __init__(self, parent = None):
        super(Model_Manager_Treewidget, self).__init__(parent)
        self.models = Models(parent)

# Define long term models
        
        long_term_models = QTreeWidgetItem(self)
        long_term_models.setText(0, COMP_LONGTERM)                          #"Long Term Choices")


        generate_synthetic_population = QTreeWidgetItem(long_term_models)
        generate_synthetic_population.setText(0, COMPMODEL_SYNTHPOP)        #"Generate Synthetic Population")

        labor_force_participation_model = QTreeWidgetItem(long_term_models)
        labor_force_participation_model.setText(0, COMPMODEL_WORKSTAT)      #"Labor Force Participation Model")

        number_of_jobs = QTreeWidgetItem(long_term_models)
        number_of_jobs.setText(0, COMPMODEL_NUMJOBS)                        #"Identify the number of jobs")

        primary_worker = QTreeWidgetItem(long_term_models)
        primary_worker.setText(0, COMPMODEL_PRIMWORK)                       #"Primary worker in the household")

        school_status = QTreeWidgetItem(long_term_models)
        school_status.setText(0, COMPMODEL_SCHSTAT)                         #"School status of everyone")

        residential_location_choice = QTreeWidgetItem(long_term_models)
        residential_location_choice.setText(0, COMPMODEL_RESLOC)            #"Residential Location Choice")


# Define fixed activity location choice generator
        
        fixed_activity_models = QTreeWidgetItem(self)
        fixed_activity_models.setText(0, COMP_FIXEDACTLOCATION)     #"Fixed Activity Location Choice Generator")

        workers = QTreeWidgetItem(fixed_activity_models)
        workers.setText(0, "Workers")

        work_location = QTreeWidgetItem(workers)
        work_location.setText(0, COMPMODEL_WORKLOC)                 #"Identify a primary work location")

        children_adult = QTreeWidgetItem(fixed_activity_models)
        children_adult.setText(0, "Children + Adult")

        school_location_choice = QTreeWidgetItem(children_adult)
        school_location_choice.setText(0, COMPMODEL_SCHLOC1)        #"School location choice")

        children_1 = QTreeWidgetItem(fixed_activity_models)
        children_1.setText(0, "Children")

        preschool_location_choice = QTreeWidgetItem(children_1)
        preschool_location_choice.setText(0, COMPMODEL_PRESCHLOC)   #"Preschool location choice"
        
        fixed_activity_locations = QTreeWidgetItem(fixed_activity_models)
        fixed_activity_locations.setText(0, "Fixed activity locations")
        
# Define Vehicle Ownership Model

        vehicle_ownership_models = QTreeWidgetItem(self)
        vehicle_ownership_models.setText(0, COMP_VEHOWN)            #"Vehicle Ownership Model")

        count_vehicles = QTreeWidgetItem(vehicle_ownership_models)
        count_vehicles.setText(0, COMPMODEL_NUMVEHS)                #"Count of Vehicles")

        Vehicle_body_fuel_type  = QTreeWidgetItem(vehicle_ownership_models)
        Vehicle_body_fuel_type.setText(0, COMPMODEL_NUMTYPES )      #"Vehicle body/fuel type")

# Define Fixed Activity Prism Models       

        fixed_activity_prism_models = QTreeWidgetItem(self)
        fixed_activity_prism_models.setText(0, COMP_FIXEDACTPRISM)

        earliest_start_day = QTreeWidgetItem(fixed_activity_prism_models)
        earliest_start_day.setText(0, COMPMODEL_DAYSTART)

        latest_end_day = QTreeWidgetItem(fixed_activity_prism_models)
        latest_end_day.setText(0, COMPMODEL_DAYEND)

        worker = QTreeWidgetItem(fixed_activity_prism_models)
        worker.setText(0, "Worker")

        number_work_episodes = QTreeWidgetItem(worker)
        number_work_episodes.setText(0, COMPMODEL_NUMWRKEPISODES)

        latest_arrival_work= QTreeWidgetItem(worker)
        latest_arrival_work.setText(0, COMPMODEL_WORKSTART1)

        earliest_departure_work = QTreeWidgetItem(worker)
        earliest_departure_work.setText(0, COMPMODEL_WORKEND1)

        nonworker = QTreeWidgetItem(fixed_activity_prism_models)
        nonworker.setText(0, COMPMODEL_NONWORKER)


        children_adults = QTreeWidgetItem(fixed_activity_prism_models)
        children_adults.setText(0, "children adults")


        number_school_episodes = QTreeWidgetItem(children_adults)
        number_school_episodes.setText(0, COMPMODEL_NUMSCHEPISODES)


        latest_arrival_school = QTreeWidgetItem(children_adults)
        latest_arrival_school.setText(0, COMPMODEL_SCHSTART1)


        earliest_departure_school = QTreeWidgetItem(children_adults)
        earliest_departure_school.setText(0, COMPMODEL_SCHEND1)


        children_2 = QTreeWidgetItem(fixed_activity_prism_models)
        children_2.setText(0, "Children")

        arrival_departure_time_preschool = QTreeWidgetItem(children_2)
        arrival_departure_time_preschool.setText(0, COMPMODEL_ARRIVALDEPARTPRESCH)  #"The arrival and departure time from Pre-school")

        time_space_prism_vertices = QTreeWidgetItem(fixed_activity_prism_models)
        time_space_prism_vertices.setText(0, COMPMODEL_TIMESPACE)                   #"Time-space prism vertices")

# Define Child Daily Status and Allocation Model

        child_model = QTreeWidgetItem(self)
        child_model.setText(0, "Child Daily Status and Allocation Model")

        children_3 = QTreeWidgetItem(child_model)
        children_3.setText(0, COMPMODEL_CSCHILD017)                 #"Children (0-17 years old)")

        children_school_1 = QTreeWidgetItem(child_model)
        children_school_1.setText(0, COMPMODEL_SCHDAILYSTATUS1)         #"Children (Status \55 School)")

        children_preschool_1 = QTreeWidgetItem(child_model)
        children_preschool_1.setText(0, COMPMODEL_PRESCHDAILYSTATUS1)      #"Children (Status \55 Pre-school)")

        children_stay_home = QTreeWidgetItem(child_model)
        children_stay_home.setText(0, COMPMODEL_CSCHILDSTA)         #"Children (Status \55 Stay home)")

        school_preschool = QTreeWidgetItem(child_model)
        school_preschool.setText(0, COMPMODEL_CSSCHPRE)             #"Is the child going to School or Pre-school today?")

        engage_activities_independently = QTreeWidgetItem(child_model)
        engage_activities_independently.setText(0, COMPMODEL_CSINDCHILD)    #"Can the child engage in activities independently?")
 
        engage_activities_like_adults = QTreeWidgetItem(child_model)
        engage_activities_like_adults.setText(0, COMPMODEL_CSCHILDIND)  #"Child can engage in activities independently like adults")

        assign_child_household = QTreeWidgetItem(child_model)
        assign_child_household.setText(0, COMPMODEL_CSASSIGN)       #"Assign the child to household")

        children_school_2 = QTreeWidgetItem(child_model)
        children_school_2.setText(0, COMPMODEL_SCHDAILYSTATUS2)         #"Children (Status \55 School)")

        children_preschool_2 = QTreeWidgetItem(child_model)
        children_preschool_2.setText(0, COMPMODEL_PRESCHDAILYSTATUS2)      #"Children (Status \55 Pre-school)")

        travel_independently_to_school = QTreeWidgetItem(child_model)
        travel_independently_to_school.setText(0, COMPMODEL_SCHDAILYINDEPENDENCE)  #"Does the child travel independently to school?")

        travel_mode_to_School = QTreeWidgetItem(child_model)
        travel_mode_to_School.setText(0, COMPMODEL_CSMODETOSCH)     #"Travel Mode to School")

        assign_drop_off_event = QTreeWidgetItem(child_model)
        assign_drop_off_event.setText(0, COMPMODEL_CSDROPOFF)       #"Assign a drop-off event to household")

        travel_independently_from_school = QTreeWidgetItem(child_model)
        travel_independently_from_school.setText(0, COMPMODEL_AFTSCHDAILYINDEPENDENCE)  #"Does the child travel independently from school?")

        travel_mode_from_School = QTreeWidgetItem(child_model)
        travel_mode_from_School.setText(0, COMPMODEL_CSMODEFROMSCH)         #"Travel Mode from School")

        assign_pick_up_event = QTreeWidgetItem(child_model)
        assign_pick_up_event.setText(0, COMPMODEL_CSPICKUP)                 #"Assign a pick-up event to household")

        activity_pursued_independently = QTreeWidgetItem(child_model)
        activity_pursued_independently.setText(0, COMPMODEL_AFTSCHACTSTATUS)      #"Activity pursued independently after school?")

        treat_child_like_adult = QTreeWidgetItem(child_model)
        treat_child_like_adult.setText(0, COMPMODEL_CSTREAT)                #"Treat the child like an adult and generate activity-travel patterns")

        after_school_activity = QTreeWidgetItem(child_model)
        after_school_activity.setText(0, COMPMODEL_CSISTHERE)               #"Is there time to engage in an after school CHILD activity?")

        choice = QTreeWidgetItem(child_model)
        choice.setText(0, COMPMODEL_CSACTTYPE)                              #"Activity Type\Choice Destination Choice\Activity Duration Choice")

        activity_with_adult = QTreeWidgetItem(child_model)
        activity_with_adult.setText(0, COMPMODEL_CSWORKSTAT)                #"Flag the child as a dependent and the child engages in activity with an adult")

        more_activity = QTreeWidgetItem(child_model)
        more_activity.setText(0, COMPMODEL_CSMOREACT)                       #"More activities")

        return_home = QTreeWidgetItem(child_model)
        return_home.setText(0, COMPMODEL_CSRETURNH)                         #"Return Home")

        to_adult = QTreeWidgetItem(child_model)
        to_adult.setText(0, COMPMODEL_CSMOVEADULT)                          #"Move to Adult Daily Status")

        
# Define Adult Daily Status Model

        adult_model = QTreeWidgetItem(self)
        adult_model.setText(0, "Adult Daily Status Model")

        children_assigned = QTreeWidgetItem(adult_model)
        children_assigned.setText(0, COMPMODEL_ASISDEPEND)      #"Is a dependent child/children assigned to household including stay home and chauffeuring activities?")

        children_stay_home = QTreeWidgetItem(adult_model)
        children_stay_home.setText(0, "Child/Children with staying home activities")

        children_chauffeuring = QTreeWidgetItem(adult_model)
        children_chauffeuring.setText(0, "Child/Children with chauffeuring activities")

        all_working_adult = QTreeWidgetItem(children_stay_home)
        all_working_adult.setText(0, COMPMODEL_ASHOUSEWORKER)     #"Households with all working adults")

        assign_children_1 = QTreeWidgetItem(children_stay_home)
        assign_children_1.setText(0, "Assign all dependent children to a working adult")

        adult_work = QTreeWidgetItem(children_stay_home)
        adult_work.setText(0, COMPMODEL_ASADULTHOME)        #"This adult works from home")

        nonworking_adult = QTreeWidgetItem(children_stay_home)
        nonworking_adult.setText(0, COMPMODEL_ASONENWORKER)    #"Households with at least one non-working adult")

        assign_children_2 = QTreeWidgetItem(children_stay_home)
        assign_children_2.setText(0, COMPMODEL_ASDEPENDNONWORK) #"Assign all dependent children to one non-working adult")

        assign_children_3 = QTreeWidgetItem(children_chauffeuring)
        assign_children_3.setText(0, COMPMODEL_ASASSIGNHOUSE)   #"Assign each dependent child to a household adult subject to the fixed activity schedule of the adult")

        check_adult = QTreeWidgetItem(adult_model)
        check_adult.setText(0, COMPMODEL_ASISWORKER)            #"For all other adults, check to see if the adult is worker?")

        work_today = QTreeWidgetItem(adult_model)
        work_today.setText(0, COMPMODEL_ASEMPLOYWORK)           #"Is an employed adult going to work today?")

        work_from_home = QTreeWidgetItem(adult_model)
        work_from_home.setText(0, COMPMODEL_WORKATHOME)         #"Work from home")

        go_to_work = QTreeWidgetItem(adult_model)
        go_to_work.setText(0, COMPMODEL_ASGOTOWORK)             #"Go to Work")

        no_work_episodes = QTreeWidgetItem(adult_model)
        no_work_episodes.setText(0, COMPMODEL_ASNWORKEPISO)     #"No Work Episodes")


# Define Activity Skeleton Reconciliation System        

        skeleton_reconciliation_system = QTreeWidgetItem(self)
        skeleton_reconciliation_system.setText(0, "Activity Skeleton Reconciliation System")
        
        skeleton_reconciliation = QTreeWidgetItem(skeleton_reconciliation_system)
        skeleton_reconciliation.setText(0, COMPMODEL_ASRECONCIL)    #"Activity Skeleton Reconciliation")
        
        person_constraints_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        person_constraints_1.setText(0, COMPMODEL_ASCONST)          #"Within person constraints")
        
        adjustment_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        adjustment_1.setText(0, COMPMODEL_ASADJUST )                #"Adjustments to the activity skeleton based on expected Travel Time from previous day")
        

        
# Define Activity Travel Pattern Simulator
        activity_travel_pattern_simulator = QTreeWidgetItem(self)
        activity_travel_pattern_simulator.setText(0, "Activity Travel Pattern Simulator")
        
        time_slice = QTreeWidgetItem(activity_travel_pattern_simulator)
        time_slice.setText(0, COMPMODEL_SMSLICE)                    #"Within a time slice")
        
        children_with_activity = QTreeWidgetItem(activity_travel_pattern_simulator)
        children_with_activity.setText(0, "Children with after school dependent activities")

        activity_pursued_1 = QTreeWidgetItem(children_with_activity)
        activity_pursued_1.setText(0, COMPMODEL_SMACTIVEPURSUE)     #"Can activity be pursued jointly with a Household member?")
        
        assign_to_non_hhold = QTreeWidgetItem(children_with_activity)
        assign_to_non_hhold.setText(0, COMPMODEL_SMACTIVEASSIGNED)  #"Activity assigned to a Non-household member comprising Joint Activity with Non-household member")
        
        assign_to_hhold = QTreeWidgetItem(children_with_activity)
        assign_to_hhold.setText(0, COMPMODEL_SMASSIGNACTIVE)        #"Assign the activity to Household member comprising Joint Activity with household member")
        
        mode_choice_model = QTreeWidgetItem(children_with_activity)
        mode_choice_model.setText(0, COMPMODEL_AFTSCHACTIVITYMODE)       #"Mode choice model for intra-household joint trips with children")
        
        all_other_individuals = QTreeWidgetItem(activity_travel_pattern_simulator)
        all_other_individuals.setText(0, "All other individuals")
        
        adult_individuals = QTreeWidgetItem(all_other_individuals)
        adult_individuals.setText(0, COMPMODEL_SMINDIVIDUAL)        #"Adult individuals, children with independent activities")
        
        travel_time = QTreeWidgetItem(all_other_individuals)
        travel_time.setText(0, COMPMODEL_SMTRIPTIME)                #"Is travel time to next fixed activity \74 time available in the prism?")
        
        activity_choice = QTreeWidgetItem(all_other_individuals)
        activity_choice.setText(0, COMPMODEL_ACTIVITYTYPE)             #"Activity Type Choice; Mode-Destination Choice")
        
        actual_start_time = QTreeWidgetItem(all_other_individuals)
        actual_start_time.setText(0, COMPMODEL_SMSTARTTIME)         #"Actual start time for the activity")
        
        time_in_activity = QTreeWidgetItem(all_other_individuals)
        time_in_activity.setText(0, COMPMODEL_ACTIVITYDURATION)         #"Is there enough time to engage in the activity?")
        
        proceed_next_activity = QTreeWidgetItem(all_other_individuals)
        proceed_next_activity.setText(0, COMPMODEL_SMPROCEED)       #"Proceed to next fixed activity")
        
        mode_choice_next_activity = QTreeWidgetItem(all_other_individuals)
        mode_choice_next_activity.setText(0, COMPMODEL_FIXEDACTIVITYMODE)   #"Mode Choice to the next fixed activity")
        
        hov = QTreeWidgetItem(all_other_individuals)
        hov.setText(0, COMPMODEL_SMISHOV)                           #"Is the mode of the trip HOV?")
        
        activity_pursued_2 = QTreeWidgetItem(all_other_individuals)
        activity_pursued_2.setText(0, COMPMODEL_SMACTIVEPURSED)     #"Can activity be pursued jointly with Household members?")
        
        check_if_join_activity = QTreeWidgetItem(all_other_individuals)
        check_if_join_activity.setText(0, COMPMODEL_JOINTACTIVITY)   #"For each available household member, check to see if he/she will join the activity?")
        
        activity_non_hhold = QTreeWidgetItem(all_other_individuals)
        activity_non_hhold.setText(0, COMPMODEL_SMACTIVENON)        #"Joint Activity with Non-household member")
        
        activity_hhold = QTreeWidgetItem(all_other_individuals)
        activity_hhold.setText(0, COMPMODEL_SMACTIVEHOUSE)          #"Joint Activity with household member")
        
        sov_hov = QTreeWidgetItem(activity_travel_pattern_simulator)
        sov_hov.setText(0, COMPMODEL_TRIPVEHICLE)                      #"If mode is SOV or HOV Driver identify vehicle")
        
        activity_travel_pattern = QTreeWidgetItem(activity_travel_pattern_simulator)
        activity_travel_pattern.setText(0, COMPMODEL_SMPATTERN)     #"Activity-travel patterns for all individuals within the time-slice")
        
# Define Activity Travel Reconciliation System
        travel_reconciliation_system = QTreeWidgetItem(self)
        travel_reconciliation_system.setText(0, "Activity Travel Reconciliation System")

        pattern_reconciliation = QTreeWidgetItem(travel_reconciliation_system)
        pattern_reconciliation.setText(0, COMPMODEL_ATRECONCIL)             #"Activity-travel Pattern Reconciliation")
        
        person_constraints_2 = QTreeWidgetItem(travel_reconciliation_system)
        person_constraints_2.setText(0, COMPMODEL_ATPERCONST)               #"Within person constraints")
        
        hhold_constraints = QTreeWidgetItem(travel_reconciliation_system)
        hhold_constraints.setText(0, COMPMODEL_ATHOUCONST)                  #"Within household constraints")
        
        adjustment_2 = QTreeWidgetItem(travel_reconciliation_system)
        adjustment_2.setText(0, COMPMODEL_ATADJUST)                         #"Duration adjustment after arrival")

        

        time_use_utility_calculator = QTreeWidgetItem(self)
        time_use_utility_calculator.setText(0, "Time Use Utility Calculator")

        self.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.treeItemSelected)

    def setConfigObject(self,co):
        self.configobject = co
    
    def treeItemSelected(self,item,col):
        diagtitle = None
        diag = None
        modelkey = None
        if item.text(col) == COMPMODEL_RESLOC:
            diagtitle = COMPMODEL_RESLOC
            modelkey = MODELKEY_RESLOC
        elif item.text(col) == COMPMODEL_SYNTHPOP:
            diagtitle = COMPMODEL_SYNTHPOP
            modelkey = MODELKEY_SYNTHPOP
        elif item.text(col) == COMPMODEL_WORKSTAT:
            diagtitle = COMPMODEL_WORKSTAT
            modelkey = MODELKEY_WORKSTAT
        elif item.text(col) == COMPMODEL_NUMJOBS:
            diagtitle = COMPMODEL_NUMJOBS
            modelkey = MODELKEY_NUMJOBS
        elif item.text(col) == COMPMODEL_PRIMWORK:
            diagtitle = COMPMODEL_PRIMWORK
            modelkey = MODELKEY_PRIMWORK
        elif item.text(col) == COMPMODEL_SCHSTAT:
            diagtitle = COMPMODEL_SCHSTAT
            modelkey = MODELKEY_SCHSTAT
        elif item.text(col) == COMPMODEL_DAYSTART:
            diagtitle = COMPMODEL_DAYSTART
            modelkey = MODELKEY_DAYSTART
        elif item.text(col) == COMPMODEL_DAYEND:
            diagtitle = COMPMODEL_DAYEND
            modelkey = MODELKEY_DAYEND
        elif item.text(col) == COMPMODEL_NUMWRKEPISODES:
            diagtitle = COMPMODEL_NUMWRKEPISODES
            modelkey = MODELKEY_NUMWRKEPISODES
        elif item.text(col) == COMPMODEL_WORKSTART1:
            diagtitle = COMPMODEL_WORKSTART1
            modelkey = MODELKEY_WORKSTART1
        elif item.text(col) == COMPMODEL_WORKEND1:
            diagtitle = COMPMODEL_WORKEND1
            modelkey = MODELKEY_WORKEND1
        elif item.text(col) == COMPMODEL_NUMSCHEPISODES:
            diagtitle = COMPMODEL_NUMSCHEPISODES
            modelkey = MODELKEY_NUMSCHEPISODES
        elif item.text(col) == COMPMODEL_SCHSTART1:
            diagtitle = COMPMODEL_SCHSTART1
            modelkey = MODELKEY_SCHSTART1
        elif item.text(col) == COMPMODEL_SCHEND1:
            diagtitle = COMPMODEL_SCHEND1
            modelkey = MODELKEY_SCHEND1
        elif item.text(col) == COMPMODEL_PRESCHLOC:
            diagtitle = COMPMODEL_PRESCHLOC
            modelkey = MODELKEY_PRESCHLOC
        elif item.text(col) == COMPMODEL_SCHLOC1:
            diagtitle = COMPMODEL_SCHLOC1
            modelkey = MODELKEY_SCHLOC1
        elif item.text(col) == COMPMODEL_WORKLOC:
            diagtitle = COMPMODEL_WORKLOC
            modelkey = MODELKEY_WORKLOC
        elif item.text(col) == COMPMODEL_NUMVEHS:
            diagtitle = COMPMODEL_NUMVEHS
            modelkey = MODELKEY_NUMVEHS
        elif item.text(col) == COMPMODEL_NUMTYPES:
            diagtitle = COMPMODEL_NUMTYPES
            modelkey = MODELKEY_NUMVEHTYPES
#        elif item.text(col) == COMPMODEL_NONWORKER:
#            diagtitle = COMPMODEL_NONWORKER
#            modelkey = MODELKEY_NONWORKER
        elif item.text(col) == COMPMODEL_ARRIVALDEPARTPRESCH:
            diagtitle = COMPMODEL_ARRIVALDEPARTPRESCH
            modelkey = MODELKEY_ARRIVALDEPARTPRESCH
        elif item.text(col) == COMPMODEL_TIMESPACE:
            diagtitle = COMPMODEL_TIMESPACE
            modelkey = MODELKEY_TIMESPACE
            
        elif item.text(col) == COMPMODEL_CSCHILD017:
            diagtitle = COMPMODEL_CSCHILD017
            modelkey = MODELKEY_CSCHILD017
        elif item.text(col) == COMPMODEL_SCHDAILYSTATUS1:
            diagtitle = COMPMODEL_SCHDAILYSTATUS1
            modelkey = MODELKEY_SCHDAILYSTATUS1
        elif item.text(col) == COMPMODEL_PRESCHDAILYSTATUS1:
            diagtitle = COMPMODEL_PRESCHDAILYSTATUS1
            modelkey = MODELKEY_PRESCHDAILYSTATUS1
        elif item.text(col) == COMPMODEL_CSCHILDSTA:
            diagtitle = COMPMODEL_CSCHILDSTA
            modelkey = MODELKEY_CSCHILDSTA
        elif item.text(col) == COMPMODEL_CSSCHPRE:
            diagtitle = COMPMODEL_CSSCHPRE
            modelkey = MODELKEY_CSSCHPRE
        elif item.text(col) == COMPMODEL_CSINDCHILD:
            diagtitle = COMPMODEL_CSINDCHILD
            modelkey = MODELKEY_CSINDCHILD
        elif item.text(col) == COMPMODEL_CSCHILDIND:
            diagtitle = COMPMODEL_CSCHILDIND
            modelkey = MODELKEY_CSCHILDIND
        elif item.text(col) == COMPMODEL_CSASSIGN:
            diagtitle = COMPMODEL_CSASSIGN
            modelkey = MODELKEY_CSASSIGN
        elif item.text(col) == COMPMODEL_SCHDAILYSTATUS2:
            diagtitle = COMPMODEL_SCHDAILYSTATUS2
            modelkey = MODELKEY_SCHDAILYSTATUS2
        elif item.text(col) == COMPMODEL_PRESCHDAILYSTATUS2:
            diagtitle = COMPMODEL_PRESCHDAILYSTATUS2
            modelkey = MODELKEY_PRESCHDAILYSTATUS2
        elif item.text(col) == COMPMODEL_SCHDAILYINDEPENDENCE:
            diagtitle = COMPMODEL_SCHDAILYINDEPENDENCE
            modelkey = MODELKEY_SCHDAILYINDEPENDENCE
        elif item.text(col) == COMPMODEL_CSMODETOSCH:
            diagtitle = COMPMODEL_CSMODETOSCH
            modelkey = MODELKEY_CSMODETOSCH
        elif item.text(col) == COMPMODEL_CSDROPOFF:
            diagtitle = COMPMODEL_CSDROPOFF
            modelkey = MODELKEY_CSDROPOFF
        elif item.text(col) == COMPMODEL_AFTSCHDAILYINDEPENDENCE:
            diagtitle = COMPMODEL_AFTSCHDAILYINDEPENDENCE
            modelkey = MODELKEY_AFTSCHDAILYINDEPENDENCE
        elif item.text(col) == COMPMODEL_CSMODEFROMSCH:
            diagtitle = COMPMODEL_CSMODEFROMSCH
            modelkey = MODELKEY_CSMODEFROMSCH
        elif item.text(col) == COMPMODEL_CSPICKUP:
            diagtitle = COMPMODEL_CSPICKUP
            modelkey = MODELKEY_CSPICKUP
        elif item.text(col) == COMPMODEL_AFTSCHACTSTATUS:
            diagtitle = COMPMODEL_AFTSCHACTSTATUS
            modelkey = MODELKEY_AFTSCHACTSTATUS
        elif item.text(col) == COMPMODEL_CSTREAT:
            diagtitle = COMPMODEL_CSTREAT
            modelkey = MODELKEY_CSTREAT
        elif item.text(col) == COMPMODEL_CSISTHERE:
            diagtitle = COMPMODEL_CSISTHERE
            modelkey = MODELKEY_CSISTHERE
        elif item.text(col) == COMPMODEL_CSACTTYPE:
            diagtitle = COMPMODEL_CSACTTYPE
            modelkey = MODELKEY_CSACTTYPE
        elif item.text(col) == COMPMODEL_CSWORKSTAT:
            diagtitle = COMPMODEL_CSWORKSTAT
            modelkey = MODELKEY_CSWORKSTAT
        elif item.text(col) == COMPMODEL_CSMOREACT:
            diagtitle = COMPMODEL_CSMOREACT
            modelkey = MODELKEY_CSMOREACT
        elif item.text(col) == COMPMODEL_CSRETURNH:
            diagtitle = COMPMODEL_CSRETURNH
            modelkey = MODELKEY_CSRETURNH
        elif item.text(col) == COMPMODEL_CSMOVEADULT:
            diagtitle = COMPMODEL_CSMOVEADULT
            modelkey = MODELKEY_CSMOVEADULT
        elif item.text(col) == COMPMODEL_ASISDEPEND:
            diagtitle = COMPMODEL_ASISDEPEND
            modelkey = MODELKEY_ASISDEPEND
        elif item.text(col) == COMPMODEL_ASHOUSEWORKER:
            diagtitle = COMPMODEL_ASHOUSEWORKER
            modelkey = MODELKEY_ASHOUSEWORKER
        elif item.text(col) == COMPMODEL_ASDEPENDWORKER:
            diagtitle = COMPMODEL_ASDEPENDWORKER
            modelkey = MODELKEY_ASDEPENDWORKER
        elif item.text(col) == COMPMODEL_ASADULTHOME:
            diagtitle = COMPMODEL_ASADULTHOME
            modelkey = MODELKEY_ASADULTHOME
        elif item.text(col) == COMPMODEL_ASONENWORKER:
            diagtitle = COMPMODEL_ASONENWORKER
            modelkey = MODELKEY_ASONENWORKER
        elif item.text(col) == COMPMODEL_ASDEPENDNONWORK:
            diagtitle = COMPMODEL_ASDEPENDNONWORK
            modelkey = MODELKEY_ASDEPENDNONWORK
        elif item.text(col) == COMPMODEL_ASASSIGNHOUSE:
            diagtitle = COMPMODEL_ASASSIGNHOUSE
            modelkey = MODELKEY_ASASSIGNHOUSE
        elif item.text(col) == COMPMODEL_ASISWORKER:
            diagtitle = COMPMODEL_ASISWORKER
            modelkey = MODELKEY_ASISWORKER
        elif item.text(col) == COMPMODEL_ASEMPLOYWORK:
            diagtitle = COMPMODEL_ASEMPLOYWORK
            modelkey = MODELKEY_ASEMPLOYWORK
        elif item.text(col) == COMPMODEL_WORKATHOME:
            diagtitle = COMPMODEL_WORKATHOME
            modelkey = MODELKEY_WORKATHOME
        elif item.text(col) == COMPMODEL_ASGOTOWORK:
            diagtitle = COMPMODEL_ASGOTOWORK
            modelkey = MODELKEY_ASGOTOWORK
        elif item.text(col) == COMPMODEL_ASNWORKEPISO:
            diagtitle = COMPMODEL_ASNWORKEPISO
            modelkey = MODELKEY_ASNWORKEPISO
        elif item.text(col) == COMPMODEL_ASRECONCIL:
            diagtitle = COMPMODEL_ASRECONCIL
            modelkey = MODELKEY_ASRECONCIL
        elif item.text(col) == COMPMODEL_ASCONST:
            diagtitle = COMPMODEL_ASCONST
            modelkey = MODELKEY_ASCONST
        elif item.text(col) == COMPMODEL_ASADJUST:
            diagtitle = COMPMODEL_ASADJUST
            modelkey = MODELKEY_ASADJUST
        elif item.text(col) == COMPMODEL_SMSLICE:
            diagtitle = COMPMODEL_SMSLICE
            modelkey = MODELKEY_SMSLICE
        elif item.text(col) == COMPMODEL_SMACTIVEPURSUE:
            diagtitle = COMPMODEL_SMACTIVEPURSUE
            modelkey = MODELKEY_SMACTIVEPURSUE
        elif item.text(col) == COMPMODEL_SMACTIVEASSIGNED:
            diagtitle = COMPMODEL_SMACTIVEASSIGNED
            modelkey = MODELKEY_SMACTIVEASSIGNED
        elif item.text(col) == COMPMODEL_SMASSIGNACTIVE:
            diagtitle = COMPMODEL_SMASSIGNACTIVE
            modelkey = MODELKEY_SMASSIGNACTIVE
        elif item.text(col) == COMPMODEL_AFTSCHACTIVITYMODE:
            diagtitle = COMPMODEL_AFTSCHACTIVITYMODE
            modelkey = MODELKEY_AFTSCHACTIVITYMODE
        elif item.text(col) == COMPMODEL_SMINDIVIDUAL:
            diagtitle = COMPMODEL_SMINDIVIDUAL
            modelkey = MODELKEY_SMINDIVIDUAL
        elif item.text(col) == COMPMODEL_SMTRIPTIME:
            diagtitle = COMPMODEL_SMTRIPTIME
            modelkey = MODELKEY_SMTRIPTIME
        elif item.text(col) == COMPMODEL_ACTIVITYTYPE:
            diagtitle = COMPMODEL_ACTIVITYTYPE
            modelkey = MODELKEY_ACTIVITYTYPE
        elif item.text(col) == COMPMODEL_SMSTARTTIME:
            diagtitle = COMPMODEL_SMSTARTTIME
            modelkey = MODELKEY_SMSTARTTIME
        elif item.text(col) == COMPMODEL_ACTIVITYDURATION:
            diagtitle = COMPMODEL_ACTIVITYDURATION
            modelkey = MODELKEY_ACTIVITYDURATION
        elif item.text(col) == COMPMODEL_SMPROCEED:
            diagtitle = COMPMODEL_SMPROCEED
            modelkey = MODELKEY_SMPROCEED
        elif item.text(col) == COMPMODEL_FIXEDACTIVITYMODE:
            diagtitle = COMPMODEL_FIXEDACTIVITYMODE
            modelkey = MODELKEY_FIXEDACTIVITYMODE
        elif item.text(col) == COMPMODEL_SMISHOV:
            diagtitle = COMPMODEL_SMISHOV
            modelkey = MODELKEY_SMISHOV
        elif item.text(col) == COMPMODEL_SMACTIVEPURSED:
            diagtitle = COMPMODEL_SMACTIVEPURSED
            modelkey = MODELKEY_SMACTIVEPURSED
        elif item.text(col) == COMPMODEL_JOINTACTIVITY:
            diagtitle = COMPMODEL_JOINTACTIVITY
            modelkey = MODELKEY_JOINTACTIVITY
        elif item.text(col) == COMPMODEL_SMACTIVENON:
            diagtitle = COMPMODEL_SMACTIVENON
            modelkey = MODELKEY_SMACTIVENON
        elif item.text(col) == COMPMODEL_SMACTIVEHOUSE:
            diagtitle = COMPMODEL_SMACTIVEHOUSE
            modelkey = MODELKEY_SMACTIVEHOUSE
        elif item.text(col) == COMPMODEL_TRIPVEHICLE:
            diagtitle = COMPMODEL_TRIPVEHICLE
            modelkey = MODELKEY_TRIPVEHICLE
        elif item.text(col) == COMPMODEL_SMPATTERN:
            diagtitle = COMPMODEL_SMPATTERN
            modelkey = MODELKEY_SMPATTERN      
        elif item.text(col) == COMPMODEL_ATRECONCIL:
            diagtitle = COMPMODEL_ATRECONCIL
            modelkey = MODELKEY_ATRECONCIL
        elif item.text(col) == COMPMODEL_ATPERCONST:
            diagtitle = COMPMODEL_ATPERCONST
            modelkey = MODELKEY_ATPERCONST
        elif item.text(col) == COMPMODEL_ATHOUCONST:
            diagtitle = COMPMODEL_ATHOUCONST
            modelkey = MODELKEY_ATHOUCONST
        elif item.text(col) == COMPMODEL_ATADJUST:
            diagtitle = COMPMODEL_ATADJUST
            modelkey = MODELKEY_ATADJUST

            
        
        if diagtitle != None:
            diag = AbtractSpecDialog(self.configobject,modelkey,diagtitle)
            diag.exec_()

        

        
        
