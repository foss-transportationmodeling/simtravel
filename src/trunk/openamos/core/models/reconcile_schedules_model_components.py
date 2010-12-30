

class ReconcileSchedulesSpecification(object):
    def __init__(self, hidName, pidName, scheduleidName,
                 activitytypeName, starttimeName,
                 endtimeName, locationidName, durationName):
        self.hidName = hidName
        self.pidName = pidName
        self.scheduleidName = scheduleidName
        self.activitytypeName = activitytypeName
        self.locationidName = locationidName
        self.starttimeName = starttimeName
        self.endtimeName = endtimeName
        self.durationName = durationName
        

        self.choices = None
        self.coefficients = None
