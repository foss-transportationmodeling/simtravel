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
    scheduleid = t.Int32Col()
    activitytype = t.Int32Col()
    locationid = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()
    duration = t.Int32Col()

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
    tripid = t.Int32Col()
    vehid = t.Int32Col()
    tripmode = t.Int32Col()
    fromzone = t.Int32Col()
    tozone = t.Int32Col()
    starttime = t.Int32Col()
    endtime = t.Int32Col()





