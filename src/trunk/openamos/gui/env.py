CONFIG_XML = 'config.xml'
PROJECT_CONFIG = 'ProjectConfig'
PROJECT = 'Project'
PROJECT_NAME = 'name'
PROJECT_HOME = 'location'
DB_CONFIG = 'DBConfig'
DB_PROTOCOL = 'dbprotocol'
DB_HOST = 'dbhost'
DB_USER = 'dbusername'
DB_PASS = 'dbpassword'
DB_NAME = 'dbname'
DB_TABLES = 'DBTables'
KEY = 'key'
COUNT_KEY = 'count_key'
ORDER = 'order'
POSTGRES = 'postgresql'
TABLEELT = 'Table'

LOCATION = 'location'
SEED = 'seed'
SUBSAMPLE = 'subsample'
SEED_DEF = '10'
SUBSAMPLE_DEF = '40000'

MODELCONFIG = 'ModelConfig'
COMP = 'Component'
MODEL = 'Model'
NAME = 'name'
FORMULATION = 'formulation'
MODELTYPE = 'type'
FILTER = 'Filter'
FILTERSET = 'FilterSet'
VERTEX = 'vertex'
START = 'start'
END = 'end'
VARIANCE = 'Variance'
VARIABLE = 'Variable'
ALTERNATIVE = 'Alternative'
DEPVARIABLE = 'DependentVariable'
VALUE = 'value'
TABLE = 'table'
COLUMN = 'var'
COND = 'condition'
COEFF = 'coeff'
ID = 'id'
THRESHOLD = 'threshold'
ALTSPEC = 'Alternative Specific'
BRANCH = 'Branch'
PROB = 'Probability'
RUNUNTIL = 'RunUntilCondition'
VTABLE = 'valuetable'
VCOLUMN = 'valuevar'

PROB_MODEL = 'Probability Distribution'
COUNT_MODEL = 'Count'
MNL_MODEL = 'Multinomial Logit'
GC_MNL_MODEL = 'Multinomial Logit (Generic Choices)'
ORD_MODEL = 'Ordered Choice'
NL_MODEL = 'Nested Logit'
SF_MODEL = 'Stochastic Frontier'
LOGSF_MODEL = 'Log Stochastic Frontier'
LOGREG_MODEL = 'Log Linear' #'Log Regression'
NEGBIN_MODEL = 'Negative Binomial'
POI_MODEL = 'Poisson'
LOGIT = 'Logit'
PROBIT = 'Probit'

MODELFORM_REG = 'Regression'
MODELFORM_ORD = 'Ordered'
MODELFORM_MNL = 'Multinomial Logit'
MODELFORM_CNT = 'Count'
MODELFORM_NL = 'Nested Logit'
MODELFORM_PD = 'Probability Distribution'

OP_EQUAL = 'equals'
OP_NOTEQUAL = 'not equals'
OP_GT = 'greater than'
OP_GTE = 'greater than equals'
OP_LT = 'less than'
OP_LTE = 'less than equals'
OP_AND = 'And'
OP_OR = 'Or'

TABLE_HH = 'households'
TABLE_PER = 'persons'

COMP_LONGTERM = 'Long Term Processes'
COMP_FIXEDACTLOCATION = 'Fixed Activity Location Choices'
COMP_VEHOWN = 'Vehicle Ownership Models'
COMP_FIXEDACTPRISM = 'Fixed Activity Prisms Generator'
COMP_CHILDSTATUS = 'Child Daily Status and Allocation'
COMP_ADULTSTATUS = 'Adult Daily Status'
COMP_ACTSKELRECONCILIATION = 'Activity Skeleton Reconciliation System'
COMP_ACTTRAVSIMULATOR = 'Activity Travel Pattern Simulator'
COMP_ACTTRAVRECONCILIATION = 'Activity Travel Reconciliation System'
COMP_TIMEUSEUTILITY = 'Time Use Utility Calculator'

COMPKEY_LONGTERM = 'LongTermModels'
COMPKEY_VEHOWN = 'VehicleOwnershipModel'
COMPKEY_VEHATTR = 'VehicleAttributeModels'
COMPKEY_WRKEPISODES = 'WorkEpisodes'
COMPKEY_MORVERTEX = 'MorningVertex'
COMPKEY_EVEVERTEX = 'EveningVertex'
COMPKEY_PRISMSWRKR = 'FixedActivityEpisodePrismsWorkers1Episode'
COMPKEY_PRISMSWRKR1 = 'FixedActivity2Episodes1PrismsWorkers'
COMPKEY_PRISMSWRKR2 = 'FixedActivity2Episodes2PrismsWorkers'
COMPKEY_PRISMSSCH ='FixedActivityEpisodePrismsSchoolers'
COMPKEY_PRISMSPRESCH ='FixedActivityEpisodePrismsPreschoolers'
COMPKEY_AFTSCHACTS = 'AfterSchoolActivities'


#COMPKEY_FIXEDACTPRISM = 'FixedActivityPrismModels'
#COMPKEY_CHILDSTATUS = 'ChildStatusAllocationModels'
#COMPKEY_MORNNONWRKR = 'MorningVertexNonWorkers'
#COMPKEY_EVENWRKR = 'EveningVertexWorkers'
#COMPKEY_EVENNONWRKR = 'EveningVertexNonWorkers'
#COMPKEY_PRISMSWRKR = 'FixedActivityEpisodePrismsWorkers'
#COMPKEY_PRISMSSCHOOL = 'FixedActivityEpisodePrismsSchoolers'
#COMPKEY_LONGTERMCHOICE = 'LongTermChoice'
#COMPKEY_AFTSCHACTIVE = 'AfterSchoolActivities'


COMPMODEL_SYNTHPOP = 'Generate Synthetic Population'
COMPMODEL_WORKSTAT = 'Labor Force Participation Model'
COMPMODEL_NUMJOBS = 'Number of Jobs'
COMPMODEL_PRIMWORK = 'Primary Worker in the Household'
COMPMODEL_SCHSTAT = 'School Status'
COMPMODEL_RESLOC = 'Residential Location Choice'

COMPMODEL_WORKLOC = 'Work Location Choice'
COMPMODEL_SCHLOC1 = 'School Location: Ages 5-14'
COMPMODEL_SCHLOC2 = 'School Location: Ages 15 and over'
COMPMODEL_PRESCHLOC = 'PreSchool Location: Ages 0-4'

COMPMODEL_NUMVEHS = 'Household Vehicle Count'
COMPMODEL_NUMTYPES = 'Household Vehicle Types'

COMPMODEL_DAYSTART = 'Earliest Day Start Time'
COMPMODEL_DAYEND = 'Latest Day End Time'
COMPMODEL_WRKEPISODES = 'Daily Work Episodes'
COMPMODEL_WORKSTART = 'Latest Work Arrival Time'
COMPMODEL_WORKEND = 'Earliest Work Departure Time'
COMPMODEL_WORKSTART1 = 'Latest Work Arrival Time\n(Episode 1)'
COMPMODEL_WORKEND1 = 'Earliest Work Departure Time\n(Episode 1)'
COMPMODEL_WORKSTART2 = 'Latest Work Arrival Time\n(Episode 2)'
COMPMODEL_WORKEND2 = 'Earliest Work Departure Time\n(Episode 2)'
COMPMODEL_SCHSTART = 'Latest School Arrival Time'
COMPMODEL_SCHEND = 'Earliest School Departure Time'
COMPMODEL_PRESCHSTART = 'Latest Preschool Arrival Time'
COMPMODEL_PRESCHEND = 'Earliest Preschool Departure Time'

COMPMODEL_CSCHILD0t4 = 'Children (0-4 years)'
COMPMODEL_PRESCHDAILYSTATUS = 'Preschool Daily Status'
COMPMODEL_CSCHILD5t17 = 'Children (5-17 years)'
COMPMODEL_SCHDAILYSTATUS = 'School Daily Status'
COMPMODEL_HMINDEP = 'Home Independence'
COMPMODEL_SCHDAILYINDEP = 'School Daily Independence'
COMPMODEL_AFTSCHDAILYINDEP = 'After School Daily Independence'
COMPMODEL_AFTSCHACTTYPE = 'After School Activity Type'
COMPMODEL_AFTSCHACTDEST = 'After School Activity Destination'
COMPMODEL_AFTSCHACTDUR = 'After School Activity Duration'
COMPMODEL_AFTSCHJOINTACT = 'Joint Activity Engagement'


COMPMODEL_ASDEPSTAYHM_WRK = 'Working Adult Stay-Home Assignment'
COMPMODEL_ASDEPSTAYHM_NONWORK = 'Non-Working Adult Stay-Home Assignment'
COMPMODEL_ASDEPCHAUFF = 'Adult Chauffeuring Assignment'
COMPMODEL_WRKDAILYSTATUS = 'Work Daily Status'
#COMPMODEL_PRESCHSTAT = 'School Status: Ages 0 - 4'
#COMPMODEL_SCHSTAT1 = 'School Status: Ages 5 - 14'
#COMPMODEL_SCHSTAT2 = 'School Status: Ages 15 and over'





COMPMODEL_AFTSCHACTMODE = 'After School Activity Mode for Dependent Children'
COMPMODEL_ACTTYPE = 'Activity Type'
COMPMODEL_ACTDEST = 'Activity Destination'
COMPMODEL_ACTDUR = 'Activity Duration'
COMPMODEL_FIXEDACTMODE = 'Fixed Activity Mode'
COMPMODEL_JOINTACT = 'Joint Activity'
COMPMODEL_TRIPVEH = 'Trip Vehicle'

#Activity Skeleton Reconciliation System      
COMPMODEL_ASRECONCIL = 'Activity Skeleton Reconciliation'
COMPMODEL_ASCONST = 'Within person constraints'     
COMPMODEL_ASADJUST = 'Adjustments to the activity skeleton based on expected Travel Time from previous day'
#Activity Travel Pattern Simulator
COMPMODEL_SMSLICE = 'Within a time slice'
#Children with after school dependent activities
COMPMODEL_SMACTIVEPURSUE = 'Can activity be pursued jointly with a Household member?'
COMPMODEL_SMACTIVEASSIGNED = 'Activity assigned to a Non-household member comprising Joint Activity with Non-household member'
COMPMODEL_SMASSIGNACTIVE = 'Assign the activity to Household member comprising Joint Activity with household member'
COMPMODEL_AFTSCHACTIVITYMODE = 'Mode choice model for intra-household joint trips with children'
#All other individuals
COMPMODEL_SMINDIVIDUAL = 'Adult individuals, children with independent activities'
COMPMODEL_SMTRIPTIME = 'Is travel time to next fixed activity \74 time available in the prism?'
COMPMODEL_ACTIVITYTYPE = 'Activity Type Choice; Mode-Destination Choice'
COMPMODEL_SMSTARTTIME = 'Actual start time for the activity'
COMPMODEL_ACTIVITYDURATION = 'Is there enough time to engage in the activity?'
COMPMODEL_SMPROCEED = 'Proceed to next fixed activity'
COMPMODEL_FIXEDACTIVITYMODE = 'Mode Choice to the next fixed activity'
COMPMODEL_SMISHOV = 'Is the mode of the trip HOV?'
COMPMODEL_SMACTIVEPURSED = 'Can activity be pursued jointly with Household members?'
COMPMODEL_JOINTACTIVITY = 'For each available household member, check to see if he/she will join the activity?'
COMPMODEL_SMACTIVENON = 'Joint Activity with Non-household member'
COMPMODEL_SMACTIVEHOUSE = 'Joint Activity with household member'
COMPMODEL_TRIPVEHICLE = 'If mode is SOV or HOV Driver identify vehicle'
COMPMODEL_SMPATTERN = 'Activity-travel patterns for all individuals within the time-slice'
#Activity Travel Reconciliation System
COMPMODEL_ATRECONCIL = 'Activity-travel Pattern Reconciliation'
COMPMODEL_ATPERCONST = 'Within person constraints'
COMPMODEL_ATHOUCONST = 'Within household constraints'
COMPMODEL_ATADJUST = 'Duration adjustment after arrival'


MODELKEY_SYNTHPOP = 'SynthPop'
MODELKEY_WORKSTAT = 'WorkStat'     
MODELKEY_NUMJOBS = 'NumJobs'
MODELKEY_PRIMWORK = 'PrimWork'
MODELKEY_SCHSTAT = 'SchStat'
MODELKEY_RESLOC = 'ResLoc'

MODELKEY_WORKLOC = 'WorkLoc'
MODELKEY_SCHLOC1 = 'SchLoc1'
MODELKEY_SCHLOC2 = 'SchLoc2'
MODELKEY_PRESCHLOC = 'PreSchLoc'

MODELKEY_NUMVEHS = 'VehCount'
MODELKEY_VEHTYPE = 'VehType'

MODELKEY_DAYSTART_AW = 'MorVtxAW'
MODELKEY_DAYEND_AW = 'EveVtxAW'
MODELKEY_WRKEPISODES = 'NumEpisodes'
MODELKEY_WORKSTART = 'WrkrStart'
MODELKEY_WORKEND = 'WrkrEnd'
MODELKEY_WORKSTART1 = 'WrkrStart1'
MODELKEY_WORKEND1 = 'WrkrEnd1'
MODELKEY_WORKSTART2 = 'WrkrStart2'
MODELKEY_WORKEND2 = 'WrkrEnd2'
MODELKEY_DAYSTART_AN = 'MorVtxAN'
MODELKEY_DAYEND_NW = 'EveVtxAN'
MODELKEY_DAYSTART_NA = 'MorVtxNA'
MODELKEY_DAYEND_NA = 'EveVtxNA'
MODELKEY_SCHSTART = 'SchStart'
MODELKEY_SCHEND = 'SchEnd'
MODELKEY_DAYSTART_PS = 'MorVtxPS'
MODELKEY_DAYEND_PS = 'EveVtxPS'
MODELKEY_PRESCHSTART = 'PreSchStart'
MODELKEY_PRESCHEND = 'PreSchEnd'

MODELKEY_PRESCHDAILYSTATUS = 'PreSchDailyStatus'
MODELKEY_SCHDAILYSTATUS = 'SchDailyStatus'
MODELKEY_HMINDEP = 'HomeIndependence'
MODELKEY_SCHDAILYINDEP = 'SchDailyIndependence'
MODELKEY_AFTSCHDAILYINDEP = 'AfterSchDailyIndependence'
MODELKEY_AFTSCHACTTYPE = 'AftSchActivityType'
MODELKEY_AFTSCHACTDEST = 'AftSchActDestination'
MODELKEY_AFTSCHACTDUR = 'AftSchActDuration'
MODELKEY_AFTSCHJOINTACT = 'AftSchJointAct'

MODELKEY_WRKDAILYSTATUS = 'WorkDailyStatus'
MODELKEY_AFTSCHACTMODE = 'AftSchActivityMode'
MODELKEY_ACTTYPE = 'ActivityType'
MODELKEY_ACTDEST = 'ActDestinationMode'
MODELKEY_ACTDUR = 'ActivityDuration'
MODELKEY_FIXEDACTMODE = 'FixedActivityMode'
MODELKEY_JOINTACT = 'JointActivity'
MODELKEY_TRIPVEH = 'TripVehicle'
MODELKEY_TIMESPACE = "TimeSpacePrismVertices"
#Child Daily Status and Allocation Model

#Adult Daily Status Model
MODELKEY_ASISDEPEND = 'DependentAssignedtoHouse'
MODELKEY_ASHOUSEWORKER = 'HouseWorkAdults'
MODELKEY_ASDEPENDWORKER = 'AssignDependentWorkAdult'
MODELKEY_ASADULTHOME = 'WorkfromHome'
MODELKEY_ASONENWORKER = 'HouseNonWorkAdult'
MODELKEY_ASDEPENDNONWORK = 'AssignDependentNonWorker'
MODELKEY_ASASSIGNHOUSE = 'AssignDependentHouse'
MODELKEY_ASISWORKER = 'AdultisWorker'
MODELKEY_ASEMPLOYWORK = 'EmployedToworkToday'
MODELKEY_WORKATHOME = 'WorkAtHome'
MODELKEY_ASGOTOWORK = 'GoWork'
MODELKEY_ASNWORKEPISO = 'NoWorkEpisodes'
#Activity Skeleton Reconciliation System      
MODELKEY_ASRECONCIL = 'ActiveSkeletonReconcil'
MODELKEY_ASCONST = 'PersonConstraint'     
MODELKEY_ASADJUST = 'AdjustActiveSkeleton'
#Activity Travel Pattern Simulator
MODELKEY_SMSLICE = 'TimeSlice'
#Children with after school dependent activities
MODELKEY_SMACTIVEPURSUE = 'CanActivePursued'
MODELKEY_SMACTIVEASSIGNED = 'ActiveAssignedNon-household'
MODELKEY_SMASSIGNACTIVE = 'AssignAcivityHousehold'
MODELKEY_AFTSCHACTIVITYMODE = 'AftSchActivityMode'
#All other individuals
MODELKEY_SMINDIVIDUAL = 'IndividualsActive'
MODELKEY_SMTRIPTIME = 'TravelTimeNextActivity'
MODELKEY_ACTIVITYTYPE = 'ActivityType'
MODELKEY_SMSTARTTIME = 'ActualStartTime'
MODELKEY_ACTIVITYDURATION = 'ActivityDuration'
MODELKEY_SMPROCEED = 'ProceedNextActive'
MODELKEY_FIXEDACTIVITYMODE = 'FixedActivityMode'
MODELKEY_SMISHOV = 'IsHOV'
MODELKEY_SMACTIVEPURSED = 'ActivePursued?'
MODELKEY_JOINTACTIVITY = 'JointActivity'
MODELKEY_SMACTIVENON = 'JointActiveNon-house'
MODELKEY_SMACTIVEHOUSE = 'JointActiveHouse'
MODELKEY_TRIPVEHICLE = 'TripVehicle'
MODELKEY_SMPATTERN = 'ActiveTravelPattern'
#Activity Travel Reconciliation System
MODELKEY_ATRECONCIL = 'ActiveTravelReconcil'
MODELKEY_ATPERCONST = 'PersonConstraint'
MODELKEY_ATHOUCONST = 'HouseConstraint'
MODELKEY_ATADJUST = 'DurationAdjust'


MODELMAP = {}

MODELMAP[MODELKEY_NUMVEHS] = [COMPKEY_VEHOWN,MODELKEY_NUMVEHS]
MODELMAP[MODELKEY_VEHTYPE] = [COMPKEY_VEHATTR,MODELKEY_VEHTYPE]

MODELMAP[MODELKEY_DAYSTART_AW] = [COMPKEY_MORVERTEX,'endtime',1]
MODELMAP[MODELKEY_DAYSTART_AN] = [COMPKEY_MORVERTEX,'endtime',2]
MODELMAP[MODELKEY_DAYSTART_NA] = [COMPKEY_MORVERTEX,'endtime',3]
MODELMAP[MODELKEY_DAYSTART_PS] = [COMPKEY_MORVERTEX,'endtime',4]

MODELMAP[MODELKEY_DAYEND_AW] = [COMPKEY_EVEVERTEX,'starttime',1]
MODELMAP[MODELKEY_DAYEND_NW] = [COMPKEY_EVEVERTEX,'starttime',2]
MODELMAP[MODELKEY_DAYEND_NA] = [COMPKEY_EVEVERTEX,'starttime',3]
MODELMAP[MODELKEY_DAYEND_PS] = [COMPKEY_EVEVERTEX,'starttime',4]

MODELMAP[MODELKEY_WRKEPISODES] = [COMPKEY_WRKEPISODES,'NumEpisodes']

MODELMAP[MODELKEY_WORKSTART] = [COMPKEY_PRISMSWRKR,'starttime']
MODELMAP[MODELKEY_WORKEND] = [COMPKEY_PRISMSWRKR,'EndTime']
MODELMAP[MODELKEY_WORKSTART1] = [COMPKEY_PRISMSWRKR1,'starttime']
MODELMAP[MODELKEY_WORKEND1] = [COMPKEY_PRISMSWRKR1,'EndTime']
MODELMAP[MODELKEY_WORKSTART2] = [COMPKEY_PRISMSWRKR2,'starttime']
MODELMAP[MODELKEY_WORKEND2] = [COMPKEY_PRISMSWRKR2,'EndTime']
MODELMAP[MODELKEY_SCHSTART] = [COMPKEY_PRISMSSCH,'starttime']
MODELMAP[MODELKEY_SCHEND] = [COMPKEY_PRISMSSCH,'EndTime']
MODELMAP[MODELKEY_PRESCHSTART] = [COMPKEY_PRISMSPRESCH,'starttime']
MODELMAP[MODELKEY_PRESCHEND] = [COMPKEY_PRISMSPRESCH,'EndTime']

MODELMAP[MODELKEY_PRESCHDAILYSTATUS] = ['DailySchStatus','DailySchStatus',1]
MODELMAP[MODELKEY_SCHDAILYSTATUS] = ['DailySchStatus','DailySchStatus',6]
MODELMAP[MODELKEY_HMINDEP] = ['ChildDependency','OtherKidsDependency']
MODELMAP[MODELKEY_SCHDAILYINDEP] = ['ChildDependency','OtherKidsDependency']
MODELMAP[MODELKEY_AFTSCHDAILYINDEP] = ['ChildDependency','OtherKidsDependency']
MODELMAP[MODELKEY_AFTSCHACTTYPE] = [COMPKEY_AFTSCHACTS,'AftSchActivityType']
MODELMAP[MODELKEY_AFTSCHACTDEST] = [COMPKEY_AFTSCHACTS,'locationIDOHActs']
MODELMAP[MODELKEY_AFTSCHACTDUR] = [COMPKEY_AFTSCHACTS,'AftSchActDuration']
MODELMAP[MODELKEY_AFTSCHJOINTACT] = [COMPKEY_AFTSCHACTS,'']

MODELMAP[MODELKEY_WRKDAILYSTATUS] = ['DailyWorkStatus','DailyWorkStatus']
#MODELKEYSMAP = {}
#MODELKEYSMAP[MODELKEY_WORKSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_NUMJOBS] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_PRESCHSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHSTAT1] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHSTAT2] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_RESLOC] = ['Household_ID','']
#MODELKEYSMAP[MODELKEY_WORKLOC] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_PRESCHLOC] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHLOC1] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_NUMVEHS] = ['Household_ID','']
#MODELKEYSMAP[MODELKEY_VEHTYPE] = ['Household_ID_fk','Vehicle_ID']
#MODELKEYSMAP[MODELKEY_DAYSTART] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_DAYEND] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_WRKEPISODES] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_WORKSTART1] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_WORKEND1] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_WORKSTART2] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_WORKEND2] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_NUMSCHEPISODES] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHSTART] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHEND] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_PRESCHDAILYSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHDAILYSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_SCHDAILYINDEP] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_AFTSCHDAILYINDEP] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_AFTSCHACTSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_AFTSCHACTTYPE] = ['Person_ID_fk','Schedule_ID']
#MODELKEYSMAP[MODELKEY_AFTSCHACTDEST] = ['Person_ID_fk','Schedule_ID']
#MODELKEYSMAP[MODELKEY_AFTSCHACTDUR] = ['Person_ID_fk','Schedule_ID']
#MODELKEYSMAP[MODELKEY_WRKDAILYSTAT] = ['Person_ID','']
#MODELKEYSMAP[MODELKEY_AFTSCHACTMODE] = ['PT_ID_fk','Trip_ID']
#MODELKEYSMAP[MODELKEY_ACTTYPE] = ['Person_ID','Schedule_ID']
#MODELKEYSMAP[MODELKEY_ACTDEST] = ['Person_ID','Schedule_ID']
#MODELKEYSMAP[MODELKEY_ACTDUR] = ['Person_ID','Schedule_ID']
#MODELKEYSMAP[MODELKEY_FIXEDACTMODE] = ['PT_ID_fk,Trip_ID','']
#MODELKEYSMAP[MODELKEY_JOINTACT] = ['PT_ID_fk,Trip_ID','']
#MODELKEYSMAP[MODELKEY_TRIPVEH] = ['Vehicle_ID_fk','Trip_ID']



