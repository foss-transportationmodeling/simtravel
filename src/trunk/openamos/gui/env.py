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
LOGREG_MODEL = 'Logistic Regression'
NEGBIN_MODEL = 'Negative Binomial'
POI_MODEL = 'Poisson'
LOGIT = 'Logit'
PROBIT = 'Probit'

MODELFORM_REG = 'Regression'
MODELFORM_ORD = 'Ordered'
MODELFORM_MNL = 'Multinomial Logit'
MODELFORM_CNT = 'Count'
MODELFORM_NL = 'Nested Logit'

OP_EQUAL = 'equals'
OP_NOTEQUAL = 'not equals'
OP_GT = 'greater than'
OP_GTE = 'greater than equals'
OP_LT = 'less than'
OP_LTE = 'less than equals'

TABLE_HH = 'households'
TABLE_PER = 'persons'

COMP_LONGTERM = 'Long Term Choices'
COMP_FIXEDACTLOCATION = 'Fixed Activity Location Choices'
COMP_VEHOWN = 'Vehicle Ownership Model'
COMP_FIXEDACTPRISM = 'Fixed Activity Prism Generator'
COMP_CHILDSTATUS = 'Child Daily Status and Allocation Model'
COMP_ADULTSTATUS = 'Adult Daily Status Model'
COMP_ACTSKELRECONCILIATION = 'Activity Skeleton Reconciliation System'
COMP_ACTTRAVSIMULATOR = 'Activity Travel Pattern Simulator'
COMP_ACTTRAVRECONCILIATION = 'Activity Travel Reconciliation System'

COMPKEY_LONGTERM = 'LongTermModels'
COMPKEY_VEHOWN = 'VehicleOwnershipModel'
COMPKEY_VEHATTR = 'VehicleAttributeModels'
COMPKEY_FIXEDACTPRISM = 'FixedActivityPrismModels'
COMPKEY_CHILDSTATUS = 'ChildStatusAllocationModels'


COMPMODEL_SYNTHPOP = 'Generate Synthetic Population'
COMPMODEL_WORKSTAT = 'Labor Force Participation Model'      #COMPMODEL_WORKSTAT = 'Worker Status'
COMPMODEL_NUMJOBS = 'Identify the number of jobs'           #COMPMODEL_NUMJOBS = 'Number of Jobs'
COMPMODEL_PRIMWORK = 'Primary worker in the household'
COMPMODEL_SCHSTAT = 'School status of everyone'
COMPMODEL_RESLOC = 'Residential Location Choice'
COMPMODEL_PRESCHSTAT = 'School Status: Ages 0 - 4'
COMPMODEL_SCHSTAT1 = 'School Status: Ages 5 - 14'
COMPMODEL_SCHSTAT2 = 'School Status: Ages 15 and over'
COMPMODEL_WORKLOC = 'Work Location Choice'
COMPMODEL_PRESCHLOC = 'PreSchool Location: Ages 0 - 4'
COMPMODEL_SCHLOC1 = 'School Location: Ages 5 - 14'
COMPMODEL_SCHLOC2 = 'School Location: Ages 15 and over'
COMPMODEL_NUMVEHS = 'Household Vehicle Counts'
COMPMODEL_NUMTYPES = 'Household Vehicle Types'
COMPMODEL_DAYSTART = 'Daily Prism Start'
COMPMODEL_DAYEND = 'Daily Prism End'
COMPMODEL_NUMWRKEPISODES = 'Number of Work Episodes'
COMPMODEL_WORKSTART1 = 'Work Prism 1 Start'
COMPMODEL_WORKEND1 = 'Work Prism 1 End'
COMPMODEL_WORKSTART2 = 'Work Prism 2 Start'
COMPMODEL_WORKEND2 = 'Work Prism 2 End'
COMPMODEL_NUMSCHEPISODES = 'Number of School Episodes'
COMPMODEL_SCHSTART1 = 'School Prism 1 Start'
COMPMODEL_SCHEND1 = 'School Prism 1 End'
COMPMODEL_SCHSTART2 = 'School Prism 2 Start'
COMPMODEL_SCHEND2 = 'School Prism 2 End'
COMPMODEL_PRESCHSTART = 'PreSchool Prism Start'
COMPMODEL_PRESCHEND = 'PreSchool Prism End'
COMPMODEL_PRESCHDAILYSTAT = 'PreSchool Daily Status'
COMPMODEL_SCHDAILYSTAT = 'School Daily Status: Ages 5 - 17'
COMPMODEL_SCHDAILYINDEP = 'School Daily Independence: Ages 5 - 17'
COMPMODEL_AFTSCHDAILYINDEP = 'After School Daily Independence: Ages 5 - 17'
COMPMODEL_AFTSCHACTSTAT = 'After School Activity Status: Ages 5 - 17'
COMPMODEL_AFTSCHACTTYPE = 'After School Activity Type: Ages 0 - 17'
COMPMODEL_AFTSCHACTDEST = 'After School Activity Destination: Ages 0 - 17'
COMPMODEL_AFTSCHACTDUR = 'After School Activity Duration: Ages 0 - 17'
COMPMODEL_WRKDAILYSTAT = 'Work Daily Status'
COMPMODEL_AFTSCHACTMODE = 'After School Activity Mode for Dependent Children'
COMPMODEL_ACTTYPE = 'Activity Type'
COMPMODEL_ACTDEST = 'Activity Destination'
COMPMODEL_ACTDUR = 'Activity Duration'
COMPMODEL_FIXEDACTMODE = 'Fixed Activity Mode'
COMPMODEL_JOINTACT = 'Joint Activity'
COMPMODEL_TRIPVEH = 'Trip Vehicle'
COMPMODEL_NONWORKER = "Non-worker"
COMPMODEL_ARRIVALDEPARTPRESCH = "The arrival and departure time from Pre-school"
COMPMODEL_TIMESPACE = "Time-space prism vertices"
#Child Daily Status and Allocation Model
COMPMODEL_CSCHILD017 = 'Children (0-17 years old)'
COMPMODEL_SCHDAILYSTATUS1 = 'Children (Status \55 School)'
COMPMODEL_PRESCHDAILYSTATUS1 = 'Children (Status \55 Pre-school)'
COMPMODEL_CSCHILDSTA = 'Children (Status \55 Stay home)'
COMPMODEL_CSSCHPRE = 'Is the child going to School or Pre-school today?'
COMPMODEL_CSINDCHILD = 'Can the child engage in activities independently?'
COMPMODEL_CSCHILDIND = 'Child can engage in activities independently like adults'
COMPMODEL_CSASSIGN = 'Assign the child to household'
COMPMODEL_SCHDAILYSTATUS2 = 'Children (Status \55 School)'
COMPMODEL_PRESCHDAILYSTATUS2 = 'Children (Status \55 Pre-school)'
COMPMODEL_SCHDAILYINDEPENDENCE = 'Does the child travel independently to school?'
COMPMODEL_CSMODETOSCH = 'Travel Mode to School'
COMPMODEL_CSDROPOFF = 'Assign a drop-off event to household'
COMPMODEL_AFTSCHDAILYINDEPENDENCE = 'Does the child travel independently from school?'
COMPMODEL_CSMODEFROMSCH = 'Travel Mode from School'
COMPMODEL_CSPICKUP = 'Assign a pick-up event to household'
COMPMODEL_AFTSCHACTSTATUS = 'Activity pursued independently after school?'
COMPMODEL_CSTREAT = 'Treat the child like an adult and generate activity-travel patterns'
COMPMODEL_CSISTHERE = 'Is there time to engage in an after school CHILD activity?'
COMPMODEL_CSACTTYPE = 'Activity Type\Choice Destination Choice\Activity Duration Choice'
COMPMODEL_CSWORKSTAT = 'Flag the child as a dependent and the child engages in activity with an adult'
COMPMODEL_CSMOREACT = 'More activities'
COMPMODEL_CSRETURNH = 'Return Home'
COMPMODEL_CSMOVEADULT = 'Move to Adult Daily Status'
#Adult Daily Status Model
COMPMODEL_ASISDEPEND = 'Is a dependent child/children assigned to household including stay home and chauffeuring activities?'
COMPMODEL_ASHOUSEWORKER = 'Households with all working adults'
COMPMODEL_ASDEPENDWORKER = 'Assign all dependent children to a working adult'
COMPMODEL_ASADULTHOME = 'This adult works from home'
COMPMODEL_ASONENWORKER = 'Households with at least one non-working adult'
COMPMODEL_ASDEPENDNONWORK = 'Assign all dependent children to one non-working adult'
COMPMODEL_ASASSIGNHOUSE = 'Assign each dependent child to a household adult subject to the fixed activity schedule of the adult'
COMPMODEL_ASISWORKER = 'For all other adults, check to see if the adult is worker?'
COMPMODEL_ASEMPLOYWORK = 'Is an employed adult going to work today?'
COMPMODEL_WORKATHOME = 'Work from home'
COMPMODEL_ASGOTOWORK = 'Go to Work'
COMPMODEL_ASNWORKEPISO = 'No Work Episodes'
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
MODELKEY_PRESCHSTAT = 'PreSchStat'
MODELKEY_SCHSTAT1 = 'SchStat1'
MODELKEY_SCHSTAT2 = 'SchStat2'
MODELKEY_WORKLOC = 'WorkLoc'
MODELKEY_PRESCHLOC = 'PreSchLoc'
MODELKEY_SCHLOC1 = 'SchLoc1'
MODELKEY_SCHLOC2 = 'SchLoc2'
MODELKEY_NUMVEHS = 'NumVehs'
MODELKEY_VEHTYPE = 'VehType'
MODELKEY_DAYSTART = 'DayStart'
MODELKEY_DAYEND = 'DayEnd'
MODELKEY_NUMWRKEPISODES = 'NumWorkEpisodes'
MODELKEY_WORKSTART1 = 'WorkStart1'
MODELKEY_WORKEND1 = 'WorkEnd1'
MODELKEY_WORKSTART2 = 'WorkStart2'
MODELKEY_WORKEND2 = 'WorkEnd2'
MODELKEY_NUMSCHEPISODES = 'NumSchEpisodes'
MODELKEY_SCHSTART1 = 'SchStart1'
MODELKEY_SCHEND1 = 'SchEnd1'
MODELKEY_SCHSTART2 = 'SchStart2'
MODELKEY_SCHEND2 = 'SchEnd2'
MODELKEY_PRESCHDAILYSTAT = 'PreSchDailyStatus'
MODELKEY_SCHDAILYSTAT = 'SchDailyStatus'
MODELKEY_SCHDAILYINDEP = 'SchDailyIndependence'
MODELKEY_AFTSCHDAILYINDEP = 'AfterSchDailyIndependence'
MODELKEY_AFTSCHACTSTAT = 'AfterSchActStatus'
MODELKEY_AFTSCHACTTYPE = 'AftSchActivityType'
MODELKEY_AFTSCHACTDEST = 'AftSchActDestination'
MODELKEY_AFTSCHACTDUR = 'AftSchActDuration'
MODELKEY_WRKDAILYSTAT = 'WorkDailyStatus'
MODELKEY_AFTSCHACTMODE = 'AftSchActivityMode'
MODELKEY_ACTTYPE = 'ActivityType'
MODELKEY_ACTDEST = 'ActDestinationMode'
MODELKEY_ACTDUR = 'ActivityDuration'
MODELKEY_FIXEDACTMODE = 'FixedActivityMode'
MODELKEY_JOINTACT = 'JointActivity'
MODELKEY_TRIPVEH = 'TripVehicle'
MODELKEY_NONWORKER = "NonWorker"
MODELKEY_ARRIVALDEPARTPRESCH = "ArrivalDepartureFromPreSch"
MODELKEY_TIMESPACE = "TimeSpacePrismVertices"
#Child Daily Status and Allocation Model
MODELKEY_CSCHILD017 = 'Child0-17'
MODELKEY_SCHDAILYSTATUS1 = 'SchDailyStatus1'
MODELKEY_PRESCHDAILYSTATUS1 = 'PreSchDailyStatus1'
MODELKEY_CSCHILDSTA = 'ChildStayHome'
MODELKEY_CSSCHPRE = 'SchOrPresch'
MODELKEY_CSINDCHILD = 'ActiveIndepend'
MODELKEY_CSCHILDIND = 'ActiveIndependAdult'
MODELKEY_CSASSIGN = 'AssignChildHouse'
MODELKEY_SCHDAILYSTATUS2 = 'SchDailyStatus2'
MODELKEY_PRESCHDAILYSTATUS2 = 'PreSchDailyStatus2'
MODELKEY_SCHDAILYINDEPENDENCE = 'SchDailyIndependence'
MODELKEY_CSMODETOSCH = 'TravelModeTo'
MODELKEY_CSDROPOFF = 'AssignDrop-off'
MODELKEY_AFTSCHDAILYINDEPENDENCE = 'AfterSchDailyIndependence'
MODELKEY_CSMODEFROMSCH = 'TravelModeFrom'
MODELKEY_CSPICKUP = 'AssignPick-up'
MODELKEY_AFTSCHACTSTATUS = 'AfterSchActStatus'
MODELKEY_CSTREAT = 'ActiveTravelPatterns'
MODELKEY_CSISTHERE = 'IsAfterSchoolActive'
MODELKEY_CSACTTYPE = 'ChildActiveType'
MODELKEY_CSWORKSTAT = 'ActiveWithAdult'
MODELKEY_CSMOREACT = 'MoreActive'
MODELKEY_CSRETURNH = 'RetHome'
MODELKEY_CSMOVEADULT = 'Move to Adult Daily Status'
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



COMPMODELMAP = {}
COMPMODELMAP[COMPKEY_FIXEDACTPRISM] = [MODELKEY_DAYSTART,MODELKEY_DAYEND,MODELKEY_NUMWRKEPISODES,
                                       MODELKEY_WORKSTART1,MODELKEY_WORKEND1,MODELKEY_WORKSTART2,MODELKEY_WORKEND2,
                                       MODELKEY_NUMSCHEPISODES,MODELKEY_SCHSTART1,MODELKEY_SCHEND1,MODELKEY_SCHSTART2,
                                       MODELKEY_SCHEND2]

COMPMODELMAP[COMPKEY_VEHOWN] = [MODELKEY_NUMVEHS]
COMPMODELMAP[COMPKEY_VEHATTR] = [MODELKEY_VEHTYPE]

PERSON_TABLE_MODELS = [MODELKEY_DAYSTART,MODELKEY_DAYEND,MODELKEY_NUMWRKEPISODES,
                                       MODELKEY_WORKSTART1,MODELKEY_WORKEND1,MODELKEY_WORKSTART2,MODELKEY_WORKEND2,
                                       MODELKEY_NUMSCHEPISODES,MODELKEY_SCHSTART1,MODELKEY_SCHEND1,MODELKEY_SCHSTART2,
                                       MODELKEY_SCHEND2]

HH_TABLE_MODELS = [MODELKEY_NUMVEHS,MODELKEY_VEHTYPE]

MODELKEYSMAP = {}
MODELKEYSMAP[MODELKEY_WORKSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMJOBS] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTAT1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTAT2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_RESLOC] = ['Household_ID','']
MODELKEYSMAP[MODELKEY_WORKLOC] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHLOC] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMVEHS] = ['Household_ID','']
MODELKEYSMAP[MODELKEY_VEHTYPE] = ['Household_ID_fk','Vehicle_ID']
MODELKEYSMAP[MODELKEY_DAYSTART] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_DAYEND] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMWRKEPISODES] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKSTART1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKEND1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKSTART2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKEND2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMSCHEPISODES] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTART1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHEND1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTART2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHEND2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHDAILYINDEP] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHDAILYINDEP] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTTYPE] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_AFTSCHACTDEST] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_AFTSCHACTDUR] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_WRKDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTMODE] = ['PT_ID_fk','Trip_ID']
MODELKEYSMAP[MODELKEY_ACTTYPE] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_ACTDEST] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_ACTDUR] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_FIXEDACTMODE] = ['PT_ID_fk,Trip_ID','']
MODELKEYSMAP[MODELKEY_JOINTACT] = ['PT_ID_fk,Trip_ID','']
MODELKEYSMAP[MODELKEY_TRIPVEH] = ['Vehicle_ID_fk','Trip_ID']



