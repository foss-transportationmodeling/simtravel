

class ReconcileSchedulesSpecification(object):
    def __init__(self, activityAttribs):
        self.activityAttribs = activityAttribs

        self.choices = None
        self.coefficients = None

class HouseholdSpecification(object):
    def __init__(self, activityAttribs, dailyStatusAttribs,
                 dependencyAttribs):
	self.activityAttribs = activityAttribs
	self.dailyStatusAttribs = dailyStatusAttribs
	self.dependencyAttribs = dependencyAttribs

	self.choices = None
	self.coefficients = None
	
class ActivityAttribsSpecification(object):
    def __init__(self, hidName, pidName, scheduleidName,
                 activitytypeName, starttimeName,
                 endtimeName, locationidName, 
                 durationName, dependentPersonName):
	self.hidName = hidName
        self.pidName = pidName
        self.scheduleidName = scheduleidName
        self.activitytypeName = activitytypeName
        self.locationidName = locationidName
        self.starttimeName = starttimeName
        self.endtimeName = endtimeName
        self.durationName = durationName
        self.dependentPersonName = dependentPersonName

class DailyStatusAttribsSpecification(object):
    def __init__(self, workStatusName, schoolStatusName):
	self.workStatusName = workStatusName
	self.schoolStatusName = schoolStatusName


class DependencyAttribsSpecification(object):
    def __init__(self, childDependencyName, elderlyDependencyName=None):
	self.childDependencyName = childDependencyName
	self.elderlyDependencyName = elderlyDependencyName
