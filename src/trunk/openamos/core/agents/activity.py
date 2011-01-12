

class ActivityEpisode(object):
    def __init__(self, scheduleId, actType, location, startTime, endTime, duration, personId=0):
        self.scheduleId = scheduleId
        self.actType = actType
        self.startTime = startTime
        self.endTime = endTime
        self.location = location
        self.duration = self.endTime - self.startTime
	self.dependentPersonId = personId
        self._first_episode_check()
        self._last_episode_check()


    def _first_episode_check(self):
        self.startOfDay = self.startTime == 0

    def _last_episode_check(self):
        self.endOfDay = self.endTime == 1439


    def __repr__(self):
        return """scheduleid - %s, acttype - %s, """\
            """location - %s, """\
            """starttime - %s, endtime - %s, duration - %s, """\
	    """depPersonId - %s """% (self.scheduleId, self.actType, self.location,
		                      self.startTime, self.endTime, self.duration,
			              self.dependentPersonId)

