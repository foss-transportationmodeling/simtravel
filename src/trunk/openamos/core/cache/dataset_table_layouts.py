import tables as t
import time

class Travel_Skims(t.IsDescription):
    origin = t.Int32Col()
    destination = t.Int32Col()
    tt = t.Float32Col()


class Persons_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    wtt = t.Float32Col()


class Vehicles_R(t.IsDescription):
    houseid = t.Int64Col()
    vehid = t.Int32Col()
    vehtype = t.Int32Col()


class Households_R(t.IsDescription):
    houseid = t.Int64Col()
    numvehs = t.Int32Col()

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


class DailyStatus_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    schdailystatus = t.Int32Col()
    wrkdailystatus = t.Int32Col()

class ChildDependency_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    dependency = t.Int32Col()


class Workers_R(t.IsDescription):
    houseid = t.Int64Col()
    personid = t.Int32Col()
    episodes = t.Int32Col()

