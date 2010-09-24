import tables as t
import time

class Households(t.IsDescription):
    houseid = t.Int32Col()
    drvrcnt = t.Int32Col()
    inclt35k = t.Int32Col()
    numchild = t.Int32Col()
    ownhome = t.Int32Col()
    urb = t.Int32Col()
    one = t.Int32Col()
    zero = t.Int32Col()
    htaz = t.Int32Col()

class Persons(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int32Col()
    wtaz = t.Int32Col()
    r_age = t.Int32Col()
    r_sex = t.Int32Col()
    one = t.Int32Col()
    zero = t.Int32Col()
    coled = t.Int32Col()
    male = t.Int32Col()
    drvr = t.Int32Col()
    aglte18 = t.Int32Col()
    aggte65 = t.Int32Col()
    timetowrk = t.Int32Col()
    wrkr = t.Int32Col()

class Travel_Skims(t.IsDescription):
    origin = t.Int16Col()
    destination = t.Int16Col()
    tt = t.Float32Col()


class Persons_R(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int32Col()
    wtt = t.Float32Col()


class Vehicles_R(t.IsDescription):
    houseid = t.Int32Col()
    vehid = t.Int16Col()
    vehtype = t.Int16Col()


class Households_R(t.IsDescription):
    houseid = t.Int32Col()
    numvehs = t.Int16Col()

class Tsp_R(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int16Col()
    daystart = t.Float32Col()
    dayend = t.Float32Col()
	
class Schedule_R(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int16Col()
    scheduleid = t.Int16Col()
    activitytype = t.Int16Col()
    locationid = t.Int16Col()
    starttime = t.Float32Col()
    endtime = t.Float32Col()
    duration = t.Float32Col()
