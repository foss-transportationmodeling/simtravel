from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class Model_Manager_Treewidget(QTreeWidget):
    def __init__(self, parent = None):
        super(Model_Manager_Treewidget, self).__init__(parent)
        self.models = Models(parent)
        self.setColumnCount(3)
        self.setHeaderLabels(["Model", "Completed", "Skip"])
        self.setColumnWidth(0, 260)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 30)
        self.setMinimumSize(360,50)
        
        self.configobject = None

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
        
        fixed_activity_models = QTreeWidgetItem(long_term_models)
        fixed_activity_models.setText(0, COMP_FIXEDACTLOCATION)     #"Fixed Activity Location Choice Generator")

        workers = QTreeWidgetItem(fixed_activity_models)
        workers.setText(0, "Workers")

        work_location = QTreeWidgetItem(workers)
        work_location.setText(0, COMPMODEL_WORKLOC)                 #"Identify a primary work location")

        children_adult = QTreeWidgetItem(fixed_activity_models)
        children_adult.setText(0, "Students")

        school_location_choice1 = QTreeWidgetItem(children_adult)
        school_location_choice1.setText(0, COMPMODEL_SCHLOC1)        #"School location choice")
        school_location_choice2 = QTreeWidgetItem(children_adult)
        school_location_choice2.setText(0, COMPMODEL_SCHLOC2)
        
        children_1 = QTreeWidgetItem(fixed_activity_models)
        children_1.setText(0, "Preschoolers")

        preschool_location_choice = QTreeWidgetItem(children_1)
        preschool_location_choice.setText(0, COMPMODEL_PRESCHLOC)   #"Preschool location choice"
        

        medium_term_models = QTreeWidgetItem(self)
        medium_term_models.setText(0, COMP_MEDIUMTERM)         
        
# Define Vehicle Ownership Model

        vehicle_ownership_models = QTreeWidgetItem(medium_term_models)
        vehicle_ownership_models.setText(0, COMP_VEHOWN)            #"Vehicle Ownership Model")

        count_vehicles = QTreeWidgetItem(vehicle_ownership_models)
        count_vehicles.setText(0, COMPMODEL_NUMVEHS)                #"Count of Vehicles")
        

        Vehicle_body_fuel_type  = QTreeWidgetItem(vehicle_ownership_models)
        Vehicle_body_fuel_type.setText(0, COMPMODEL_NUMTYPES )      #"Vehicle body/fuel type")

# Define Fixed Activity Prism Models       

        fixed_activity_prism_models = QTreeWidgetItem(medium_term_models)
        fixed_activity_prism_models.setText(0, COMP_FIXEDACTPRISM)

        daystart = QTreeWidgetItem(fixed_activity_prism_models)
        daystart.setText(0, COMPMODEL_DAYSTART)

        daystart_aw = QTreeWidgetItem(daystart)
        daystart_aw.setText(0, "Adult Workers")
        daystart_an = QTreeWidgetItem(daystart)
        daystart_an.setText(0, "Adult Non-workers")
        daystart_na = QTreeWidgetItem(daystart)
        daystart_na.setText(0, "Children (5-17 years) and\nAdult Students")
        daystart_ps = QTreeWidgetItem(daystart)
        daystart_ps.setText(0, "Pre-school Children\n(0-4 years)")

        dayend = QTreeWidgetItem(fixed_activity_prism_models)
        dayend.setText(0, COMPMODEL_DAYEND)

        dayend_aw = QTreeWidgetItem(dayend)
        dayend_aw.setText(0, "Adult Workers")
        dayend_an = QTreeWidgetItem(dayend)
        dayend_an.setText(0, "Adult Non-workers")
        dayend_na = QTreeWidgetItem(dayend)
        dayend_na.setText(0, "Children (5-17 years) and\nAdult Students")
        dayend_ps = QTreeWidgetItem(dayend)
        dayend_ps.setText(0, "Pre-school Children\n(0-4 years)")
        
        work_episodes = QTreeWidgetItem(fixed_activity_prism_models)
        work_episodes.setText(0, COMPMODEL_WRKEPISODES)

        one_episode_workers = QTreeWidgetItem(fixed_activity_prism_models)
        one_episode_workers.setText(0, COMPMODEL_1WEPISODE)
        latest_oneepiso = QTreeWidgetItem(one_episode_workers)
        latest_oneepiso.setText(0, COMPMODEL_WORKSTART)
        early_oneepiso = QTreeWidgetItem(one_episode_workers)
        early_oneepiso.setText(0, COMPMODEL_WORKEND)        


        two_episode_workers1 = QTreeWidgetItem(fixed_activity_prism_models)
        two_episode_workers1.setText(0, COMPMODEL_2WEPISODE1)
        latest_twoepiso1 = QTreeWidgetItem(two_episode_workers1)
        latest_twoepiso1.setText(0, COMPMODEL_WORKSTART1)
        early_twoepiso1 = QTreeWidgetItem(two_episode_workers1)
        early_twoepiso1.setText(0, COMPMODEL_WORKEND1)

        two_episode_workers2 = QTreeWidgetItem(fixed_activity_prism_models)
        two_episode_workers2.setText(0, COMPMODEL_2WEPISODE2)
        latest_twoepiso2 = QTreeWidgetItem(two_episode_workers2)
        latest_twoepiso2.setText(0, COMPMODEL_WORKSTART2)
        early_twoepiso2 = QTreeWidgetItem(two_episode_workers2)
        early_twoepiso2.setText(0, COMPMODEL_WORKEND2)        
         
        schoolprisms = QTreeWidgetItem(fixed_activity_prism_models)
        schoolprisms.setText(0, COMPMODEL_SCHEPISODES)
        latest_school = QTreeWidgetItem(schoolprisms)
        latest_school.setText(0, COMPMODEL_SCHSTART)
        early_school = QTreeWidgetItem(schoolprisms)
        early_school.setText(0, COMPMODEL_SCHEND)        
                 
        preschoolprisms = QTreeWidgetItem(fixed_activity_prism_models)
        preschoolprisms.setText(0, COMPMODEL_PRESCHEPISODES)
        latest_preschool = QTreeWidgetItem(preschoolprisms)
        latest_preschool.setText(0, COMPMODEL_PRESCHSTART)
        early_preschool = QTreeWidgetItem(preschoolprisms)
        early_preschool.setText(0, COMPMODEL_PRESCHEND) 

# Define Activity Skeleton Reconciliation System        

        skeleton_reconciliation_system = QTreeWidgetItem(medium_term_models)
        skeleton_reconciliation_system.setText(0, COMP_ACTSKELRECONCILIATION)
        
        skeleton_reconciliation = QTreeWidgetItem(skeleton_reconciliation_system)
        skeleton_reconciliation.setText(0, COMPMODEL_ASRECONCIL)    #"Activity Skeleton Reconciliation")
        
        person_constraints_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        person_constraints_1.setText(0, COMPMODEL_ASCONST)          #"Within person constraints")
        
        adjustment_1 = QTreeWidgetItem(skeleton_reconciliation_system)
        adjustment_1.setText(0, COMPMODEL_ASADJUST )                #"Adjustments to the activity skeleton based on expected Travel Time from previous day")
        
        short_term_models = QTreeWidgetItem(self)
        short_term_models.setText(0, COMP_SHORTTERM) 

# Define Child Daily Status and Allocation Model

        child_model = QTreeWidgetItem(medium_term_models)
        child_model.setText(0, COMP_CHILDSTATUS)
        
        sch_status = QTreeWidgetItem(child_model)
        sch_status.setText(0, COMPMODEL_SCHSTATUS)
        children_preschool = QTreeWidgetItem(sch_status)
        children_preschool.setText(0, COMPMODEL_PRESCHDAILYSTATUS)
        children_school1 = QTreeWidgetItem(sch_status)
        children_school1.setText(0, COMPMODEL_SCHDAILYSTATUS)         #"Children (Status \55 School)")

        child_dependent = QTreeWidgetItem(child_model)
        child_dependent.setText(0, COMPMODEL_CHIDDEPEND) 
        children_hmindep = QTreeWidgetItem(child_dependent)
        children_hmindep.setText(0, COMPMODEL_HMINDEP)
        children_schindep = QTreeWidgetItem(child_dependent)
        children_schindep.setText(0, COMPMODEL_SCHDAILYINDEP)
        children_aftschindep = QTreeWidgetItem(child_dependent)
        children_aftschindep.setText(0, COMPMODEL_AFTSCHDAILYINDEP)
        
        aft_sch_activity = QTreeWidgetItem(child_model)
        aft_sch_activity.setText(0, COMPMODEL_AFTSCHACTIVITY)         
        children_aftschacttype = QTreeWidgetItem(aft_sch_activity)
        children_aftschacttype.setText(0, COMPMODEL_AFTSCHACTTYPE)
        children_aftschactdest = QTreeWidgetItem(aft_sch_activity)
        children_aftschactdest.setText(0, COMPMODEL_AFTSCHACTDEST)
        children_aftschactdur = QTreeWidgetItem(aft_sch_activity)
        children_aftschactdur.setText(0, COMPMODEL_AFTSCHACTDUR)
        children_aftschactjointact = QTreeWidgetItem(aft_sch_activity)
        children_aftschactjointact.setText(0, COMPMODEL_AFTSCHJOINTACT)
        
        
#        children_1 = QTreeWidgetItem(child_model)
#        children_1.setText(0, COMPMODEL_CSCHILD0t4)                 #"Children (0-4 years old)")
#        children_2 = QTreeWidgetItem(child_model)
#        children_2.setText(0, COMPMODEL_CSCHILD5t17) 




# Define Adult Daily Status Model

        adult_model = QTreeWidgetItem(medium_term_models)
        adult_model.setText(0, COMP_ADULTSTATUS)

        assign_stayhmchild_wrk = QTreeWidgetItem(adult_model)
        assign_stayhmchild_wrk.setText(0, COMPMODEL_ASDEPSTAYHM_WRK) #"Assign all dependent children to one non-working adult")
        assign_stayhmchild_nonwrk = QTreeWidgetItem(adult_model)
        assign_stayhmchild_nonwrk.setText(0, COMPMODEL_ASDEPSTAYHM_NONWORK)   #"Assign each dependent child to a household adult subject to the fixed activity schedule of the adult")
        assign_chauffchild = QTreeWidgetItem(adult_model)
        assign_chauffchild.setText(0, COMPMODEL_ASDEPCHAUFF)        
        work_today = QTreeWidgetItem(adult_model)
        work_today.setText(0, COMPMODEL_WRKDAILYSTATUS)

        
# Define Activity Travel Pattern Simulator
        activity_travel_pattern_simulator = QTreeWidgetItem(short_term_models)
        activity_travel_pattern_simulator.setText(0, COMP_ACTTRAVSIMULATOR)
        
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
        travel_reconciliation_system = QTreeWidgetItem(short_term_models)
        travel_reconciliation_system.setText(0, COMP_ACTTRAVRECONCILIATION)

        pattern_reconciliation = QTreeWidgetItem(travel_reconciliation_system)
        pattern_reconciliation.setText(0, COMPMODEL_ATRECONCIL)             #"Activity-travel Pattern Reconciliation")
        
        person_constraints_2 = QTreeWidgetItem(travel_reconciliation_system)
        person_constraints_2.setText(0, COMPMODEL_ATPERCONST)               #"Within person constraints")
        
        hhold_constraints = QTreeWidgetItem(travel_reconciliation_system)
        hhold_constraints.setText(0, COMPMODEL_ATHOUCONST)                  #"Within household constraints")
        
        adjustment_2 = QTreeWidgetItem(travel_reconciliation_system)
        adjustment_2.setText(0, COMPMODEL_ATADJUST)                         #"Duration adjustment after arrival")

        

        time_use_utility_calculator = QTreeWidgetItem(self)
        time_use_utility_calculator.setText(0, COMP_TIMEUSEUTILITY)

        self.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.treeItemSelected)
        self.connect(self, SIGNAL('itemChanged (QTreeWidgetItem *,int)'), self.saveSkip)
        

    def setConfigObject(self,co):
        self.configobject = co
        self.setAllComSimStatuses()
        
    def setAllComSimStatuses(self):
        self.setCompSimStatus(COMPMODEL_NUMVEHS)
        self.setCompSimStatus(COMPMODEL_NUMTYPES)
        self.setCompSimStatus(COMPMODEL_DAYSTART)
        self.setCompSimStatus(COMPMODEL_DAYEND)
        self.setCompSimStatus(COMPMODEL_WRKEPISODES)
        self.setCompSimStatus(COMPMODEL_1WEPISODE)
        self.setCompSimStatus(COMPMODEL_2WEPISODE1)
        self.setCompSimStatus(COMPMODEL_2WEPISODE2)
        self.setCompSimStatus(COMPMODEL_SCHEPISODES)
        self.setCompSimStatus(COMPMODEL_PRESCHEPISODES)
        self.setCompSimStatus(COMPMODEL_SCHSTATUS)
        self.setCompSimStatus(COMPMODEL_CHIDDEPEND)
        self.setCompSimStatus(COMPMODEL_AFTSCHACTIVITY)
        

    def setCompSimStatus(self,comptitle):
        treecomp = self.findItems(QString(comptitle),Qt.MatchFixedString | Qt.MatchRecursive)[0]
        treecomp.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        compname = (COMPONENTMAP[comptitle])[0]
        compsimstat = self.configobject.getCompSimStatus(compname)
        if compsimstat != None:
            treecomp.setIcon(1, QIcon("./images/%s" %(compsimstat[0])))
            if compsimstat[1]:
                treecomp.setCheckState(2, Qt.Checked)
            else:
                treecomp.setCheckState(2, Qt.Unchecked)


    def saveSkip(self,item,col):
        if self.configobject != None and col == 2:
            compname = (COMPONENTMAP[str(item.text(0))])[0]
            comp = self.configobject.getComponent(compname)
            if comp != None:
                if item.checkState(2) == 2:
                    comp.set('skip','True')
                else:
                    comp.set('skip','False')


    def treeItemSelected(self,item,col):
        diagtitle = None
        diag = None
        modelkey = None
        if str(item.text(col)).lower() == COMPMODEL_NUMVEHS.lower():
            diagtitle = COMPMODEL_NUMVEHS
            modelkey = MODELKEY_NUMVEHS
        elif str(item.text(col)).lower() == COMPMODEL_NUMTYPES.lower():
            diagtitle = COMPMODEL_NUMTYPES
            modelkey = MODELKEY_VEHTYPE   

        elif str(item.text(col)).lower() == ('Adult Workers').lower():
            seg = str((item.parent()).text(0)).lower()
            if seg == COMPMODEL_DAYSTART.lower():
                diagtitle = COMPMODEL_DAYSTART
                modelkey = MODELKEY_DAYSTART_AW
            elif seg == COMPMODEL_DAYEND.lower():
                diagtitle = COMPMODEL_DAYEND
                modelkey = MODELKEY_DAYEND_AW
        elif str(item.text(col)).lower() == ('Adult Non-workers').lower():
            seg = str((item.parent()).text(0)).lower()
            if seg == COMPMODEL_DAYSTART.lower():
                diagtitle = COMPMODEL_DAYSTART
                modelkey = MODELKEY_DAYSTART_AN
            elif seg == COMPMODEL_DAYEND.lower():
                diagtitle = COMPMODEL_DAYEND
                modelkey = MODELKEY_DAYEND_AN                
        elif str(item.text(col)).lower() == ('Children (5-17 years) and\nAdult Students').lower():
            seg = str((item.parent()).text(0)).lower()
            if seg == COMPMODEL_DAYSTART.lower():
                diagtitle = COMPMODEL_DAYSTART
                modelkey = MODELKEY_DAYSTART_NA
            elif seg == COMPMODEL_DAYEND.lower():
                diagtitle = COMPMODEL_DAYEND
                modelkey = MODELKEY_DAYEND_NA  
        elif str(item.text(col)).lower() == ('Pre-school Children\n(0-4 years)').lower():
            seg = str((item.parent()).text(0)).lower()
            if seg == COMPMODEL_DAYSTART.lower():
                diagtitle = COMPMODEL_DAYSTART
                modelkey = MODELKEY_DAYSTART_PS
            elif seg == COMPMODEL_DAYEND.lower():
                diagtitle = COMPMODEL_DAYEND
                modelkey = MODELKEY_DAYEND_PS 

        elif str(item.text(col)).lower() == COMPMODEL_WRKEPISODES.lower():
            diagtitle = COMPMODEL_WRKEPISODES
            modelkey = MODELKEY_WRKEPISODES
        elif str(item.text(col)).lower() == COMPMODEL_WORKSTART.lower():
            diagtitle = COMPMODEL_WORKSTART
            modelkey = MODELKEY_WORKSTART
        elif str(item.text(col)).lower() == COMPMODEL_WORKEND.lower():
            diagtitle = COMPMODEL_WORKEND
            modelkey = MODELKEY_WORKEND
        elif str(item.text(col)).lower() == COMPMODEL_WORKSTART1.lower():
            diagtitle = COMPMODEL_WORKSTART1
            modelkey = MODELKEY_WORKSTART1
        elif str(item.text(col)).lower() == COMPMODEL_WORKEND1.lower():
            diagtitle = COMPMODEL_WORKEND1
            modelkey = MODELKEY_WORKEND1
        elif str(item.text(col)).lower() == COMPMODEL_WORKSTART2.lower():
            diagtitle = COMPMODEL_WORKSTART2
            modelkey = MODELKEY_WORKSTART2
        elif str(item.text(col)).lower() == COMPMODEL_WORKEND2.lower():
            diagtitle = COMPMODEL_WORKEND2
            modelkey = MODELKEY_WORKEND2

        elif str(item.text(col)).lower() == COMPMODEL_SCHSTART.lower():
            diagtitle = COMPMODEL_SCHSTART
            modelkey = MODELKEY_SCHSTART
        elif str(item.text(col)).lower() == COMPMODEL_SCHEND.lower():
            diagtitle = COMPMODEL_SCHEND
            modelkey = MODELKEY_SCHEND     

        elif str(item.text(col)).lower() == COMPMODEL_PRESCHSTART.lower():
            diagtitle = COMPMODEL_PRESCHSTART
            modelkey = MODELKEY_PRESCHSTART
        elif str(item.text(col)).lower() == COMPMODEL_PRESCHEND.lower():
            diagtitle = COMPMODEL_PRESCHEND
            modelkey = MODELKEY_PRESCHEND           

        elif str(item.text(col)).lower() == COMPMODEL_PRESCHDAILYSTATUS.lower():
            diagtitle = COMPMODEL_PRESCHDAILYSTATUS
            modelkey = MODELKEY_PRESCHDAILYSTATUS   
        elif str(item.text(col)).lower() == COMPMODEL_SCHDAILYSTATUS.lower():
            diagtitle = COMPMODEL_SCHDAILYSTATUS
            modelkey = MODELKEY_SCHDAILYSTATUS  
        elif str(item.text(col)).lower() == COMPMODEL_HMINDEP.lower():
            diagtitle = COMPMODEL_HMINDEP
            modelkey = MODELKEY_HMINDEP 
        elif str(item.text(col)).lower() == COMPMODEL_SCHDAILYINDEP.lower():
            diagtitle = COMPMODEL_SCHDAILYINDEP
            modelkey = MODELKEY_SCHDAILYINDEP 
        elif str(item.text(col)).lower() == COMPMODEL_AFTSCHDAILYINDEP.lower():
            diagtitle = COMPMODEL_AFTSCHDAILYINDEP
            modelkey = MODELKEY_AFTSCHDAILYINDEP 
        elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTTYPE.lower():
            diagtitle = COMPMODEL_AFTSCHACTTYPE
            modelkey = MODELKEY_AFTSCHACTTYPE 
        elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTDEST.lower():
            diagtitle = COMPMODEL_AFTSCHACTDEST
            modelkey = MODELKEY_AFTSCHACTDEST 
        elif str(item.text(col)).lower() == COMPMODEL_AFTSCHACTDUR.lower():
            diagtitle = COMPMODEL_AFTSCHACTDUR
            modelkey = MODELKEY_AFTSCHACTDUR 
        elif str(item.text(col)).lower() == COMPMODEL_AFTSCHJOINTACT.lower():
            diagtitle = COMPMODEL_AFTSCHJOINTACT
            modelkey = MODELKEY_AFTSCHJOINTACT 

        elif str(item.text(col)).lower() == COMPMODEL_WRKDAILYSTATUS.lower():
            diagtitle = COMPMODEL_WRKDAILYSTATUS
            modelkey = MODELKEY_WRKDAILYSTATUS 
            

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
#        elif item.text(col) == COMPMODEL_SMPROCEED:
#            diagtitle = COMPMODEL_SMPROCEED
#            modelkey = MODELKEY_SMPROCEED
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
        elif item.text(col) == COMPMODEL_TRIPVEHICLE:
            diagtitle = COMPMODEL_TRIPVEHICLE
            modelkey = MODELKEY_TRIPVEHICLE



        if diagtitle != None and self.configobject != None:
            diag = AbtractSpecDialog(self.configobject,modelkey,diagtitle)
            diag.exec_()




