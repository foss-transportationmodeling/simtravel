import tables as t
import time

class Travel_Skims(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    tt = t.Float32Col()

class Locations(t.IsDescription):
    locationid = t.Int32Col()
    population = t.Int32Col()
    public_employment = t.Int32Col()
    retail_employment = t.Int32Col()
    office_employment = t.Int32Col()
    industrial_employment = t.Int32Col()
    other_employment = t.Int32Col()
    public_employment_ind = t.Int32Col()
    retail_employment_ind = t.Int32Col()
    office_employment_ind = t.Int32Col()
    industrial_employment_ind = t.Int32Col()
    other_employment_ind = t.Int32Col()
    total_area = t.Float32Col()
    residential_population = t.Int32Col()
    single_family_dwelling = t.Int32Col()
    institutional_population = t.Int32Col()
    multi_family_dwelling = t.Int32Col()    

class Persons_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    wtt = t.Float32Col()


class Households_Vehicles_Count_R(t.IsDescription):
    houseid = t.Int64Col()
    vehcount = t.Int32Col()

class Vehicles_R(t.IsDescription):
    houseid = t.Int64Col()
    vehid = t.Int32Col()
    vehtype = t.Int32Col()

class Tsp_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    daystart = t.Int32Col()
    dayend = t.Int32Col()
	
class Schedule_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    dependentpersonid = t.Int64Col()

class Schedule_Allocation_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()
    dependentpersonid = t.Int64Col()
    tripcount = t.Int32Col()


class Child_Dependency_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    dependency = t.Int32Col()

class Daily_School_Status_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    schdailystatus = t.Int32Col()

class Daily_Work_Status_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    wrkdailystatus = t.Int32Col()

class Workers_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    episodes = t.Int32Col()

class Trips_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    vehid = t.Int32Col()
    tripmode = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    trippurposefrom = t.Int32Col()
    trippurpose = t.Int32Col()
    duration = t.Int32Col()
    occupancy = t.Int32Col()
    tripind = t.Int32Col()
    dependentpersonid = t.Int64Col()

class Trips_Invalid_R(t.IsDescription):
    tripid = t.Int64Col()
    tripind = t.Int32Col()


class Occupancy_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    tripid = t.Int32Col()
    occupancy = t.Int32Col()
    dependentpersonid = t.Int64Col()

class Trips_Final_R(t.IsDescription):
    tripid = t.Int64Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()
    vehid = t.Int32Col()
    tripmode = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    trippurpose = t.Int32Col()

class Persons_Prism_Activities_R(t.IsDescription):
    scheduleid = t.Int64Col()
    houseid = t.Int64Col()
    personid = t.Int32Col()

class Persons_Location_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    personuniqueid = t.Int32Col()
    time = t.Int32Col()
    location = t.Int32Col()
    lasttripcount = t.Int32Col()
	
class Persons_History_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    personuniqueid = t.Int32Col()
    ih_history = t.Int32Col()
    maintenance_history = t.Int32Col()
    discretionary_history = t.Int32Col()
    fixed_history = t.Int32Col()


class Gap_Function_R(t.IsDescription):
    tripid = t.Int64Col()
    houseid = t.Int32Col()
    personid = t.Int32Col()
    gap_before = t.Int32Col()
    gap_after = t.Int32Col()

class OD_R(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    count = t.Int32Col()


class ODT_R(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    time = t.Int32Col()
    count = t.Int32Col()


class Mortality_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    mortality_f = t.Int32Col()

class Birth_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    childbirth_f = t.Int32Col()

class Aging_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age_f = t.Int32Col()
    age_sq_f = t.Int32Col()

class Student_Residence_Choice_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    residence_type_f = t.Int32Col()

class Education_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    enroll = t.Int32Col()
    grade_disagg = t.Int32Col()
    educ_disagg = t.Int32Col()
    educ_in_yrs = t.Int32Col()

class Education_Forecast_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    enroll_f = t.Int32Col()
    grade_disagg_f = t.Int32Col()
    educ_disagg_f = t.Int32Col()
    educ_in_yrs_f = t.Int32Col()

class Labor_Participation_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    labor_participation_f = t.Int32Col()
    occupation_f = t.Int32Col()
    income_f = t.Int32Col()

class Marriage_Decision_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    marriage_decision_f = t.Int32Col()

class Divorce_Decision_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    divorce_decision_f = t.Int32Col()

class Household_Forecast_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    bldgsz = t.Int32Col()
    hht = t.Int32Col()
    hinc = t.Int32Col()
    noc = t.Int32Col()
    persons = t.Int32Col()
    unittype = t.Int32Col()
    vehicl = t.Int32Col()
    wif = t.Int32Col()
    yrmoved = t.Int32Col()
    old_houseid = t.Int64Col()

class Household_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    bldgsz = t.Int32Col()
    hht = t.Int32Col()
    hinc = t.Int32Col()
    noc = t.Int32Col()
    persons = t.Int32Col()
    unittype = t.Int32Col()
    vehicl = t.Int32Col()
    wif = t.Int32Col()
    yrmoved = t.Int32Col()

class Person_Forecast_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ_disagg = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade_disagg = t.Int32Col()
    hispan = t.Int32Col()
    old_houseid = t.Int64Col()

class Person_Moving_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade = t.Int32Col()
    hispan = t.Int32Col()

class Person_Population_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int64Col()
    age = t.Int32Col()
    clwkr = t.Int32Col()
    educ_disagg = t.Int32Col()
    enroll = t.Int32Col()
    esr = t.Int32Col()
    indnaics = t.Int32Col()
    occcen5 = t.Int32Col()
    race1 = t.Int32Col()
    relate = t.Int32Col()
    sex = t.Int32Col()
    marstat = t.Int32Col()
    hours = t.Int32Col()
    grade_disagg = t.Int32Col()
    hispan = t.Int32Col()


class Age_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    age = t.Int32Col()
    count = t.Int32Col()

class Sex_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    sex = t.Int32Col()
    count = t.Int32Col()


class Race_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    race1 = t.Int32Col()
    count = t.Int32Col()


class Persons_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    persons = t.Int32Col()
    count = t.Int32Col()

class Hht_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    hht = t.Int32Col()
    count = t.Int32Col()

class Wif_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    wif = t.Int32Col()
    count = t.Int32Col()

class Noc_Dist_R(t.IsDescription):
    analysisinterval = t.Int64Col()
    noc = t.Int32Col()
    count = t.Int32Col()

