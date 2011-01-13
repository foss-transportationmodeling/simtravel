import copy
import heapq as hp
from numpy import array,zeros

from openamos.core.models.abstract_random_distribution_model import RandomDistribution


class Person(object):
    def __init__(self, hid, pid):
        self.hid = hid
        self.pid = pid
        self.listOfActivityEpisodes = []
        self.workEpisodes = []
        self.schoolEpisodes = []
        self.actCount = 0
	self.scheduleIds = []
	self.firstEpisode = None
	self.lastEpisode = None
        self.scheduleConflictIndicator = zeros((1440,0))

    def reconcile_activity_schedules(self, seed=1):
        self.reconciledActivityEpisodes = []
        self.seed = seed
        #print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
        #self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        self.listOfActivityEpisodes = copy.deepcopy(self.reconciledActivityEpisodes)
        #results = self._collate_results()
        #return results
        

    def add_episodes(self, activityEpisodes):
        for activity in activityEpisodes:
	    if activity.startOfDay:
		self.firstEpisode = activity
	    if activity.endOfDay:
	        self.lastEpisode = activity
            hp.heappush(self.listOfActivityEpisodes, (activity.startTime, activity))
            self.actCount += 1
            self.scheduleIds.append(activity.scheduleId)
            self._update_schedule_conflict_indicator(activity, add=True)


    def remove_episodes(self, activityEpisodes):
	for activity in activityEpisodes:
	    self.listOfActivityEpisodes.remove((activity.startTime, activity))
	    self.actCount -= 1
	    self.scheduleIds.remove(activity.scheduleId)
            self._update_schedule_conflict_indicator(activity, add=True)

    def _update_schedule_conflict_indicator(self, activity, add=True):
        if add:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime] += 1
        else:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime] -= 1            

        
    def _check_for_conflicts(self):
        if (self.scheduleConflictIndicator > 1).sum() > 1:
            print 'THERE ARE CONFLICTS IN THE SCHEDULE FOR PERSON - ', self.pid
            for recAct in self.listOfActivityEpisodes:
                print recAct
            return False
        return True
            
    def pop_earliest_activity(self):
	self.actCount -= 1
	activityStart, activity = hp.heappop(self.listOfActivityEpisodes)
	self.scheduleIds.remove(activity.scheduleId)
	return activityStart, activity


    def new_schedule_id(self):
	newId = self.actCount + 1
	if newId not in self.scheduleIds:
	    return newId
	else:
	    for i in range(newId):
	        if i not in self.scheduleIds:
		    return i
	

    def check_start_of_day(self, refEndTime, depPersonId):
	if self.firstEpisode.endTime >= refEndTime:
	    self.firstEpisode.dependentPersonId = depPersonId
	    return True
	else:
	    return False
	
	

    def check_end_of_day(self, refStartTime, depPersonId):
	if self.lastEpisode.startTime <= refStartTime:
	    self.lastEpisode.dependentPersonId = depPersonId
	    return True
	else:
	    return False



    def move_start_of_day(self, refEndTime, depPersonId):
	self.firstEpisode.endTime = refEndTime 
        self.firstEpisode.dependentPersonId = depPersonId
	self.firstEpisode.duration = (self.firstEpisode.endTime - 
				      self.firstEpisode.startTime)


    def move_end_of_day(self, refStartTime, depPersonId):
	self.lastEpisode.startTime = refStartTime 
        self.lastEpisode.dependentPersonId = depPersonId
	self.lastEpisode.duration = (self.lastEpisode.endTime -
				     self.lastEpisode.startTime)


    def add_status_dependency(self, workstatus, schoolstatus, child_dependency):
        self.workstatus = workstatus
        self.schoolstatus = schoolstatus
        self.child_dependency = child_dependency

        self.extract_work_episodes()
        self.extract_school_episodes()
        
    def extract_work_episodes(self):
        for startTime, act in self.listOfActivityEpisodes:
            if act.actType > 199 and act.actType < 300:
                self.workEpisodes.append(act)

    def extract_school_episodes(self):
        for startTime, act in self.listOfActivityEpisodes:
            if act.actType > 299 and act.actType < 400:
                self.schoolEpisodes.append(act)        

    def _reconcile_schedule(self):
        print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
        #stAct = hp.heappop(self.listOfActivityEpisodes)[1]
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):
            
            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex, 
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
	    print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
	    print '\tFIRST ACT OF PRISM - ', stAct
	    print '\tLAST ACT OF PRISM -  ', endAct
	
            if endAct.endTime == 1439 and len(self.listOfActivityEpisodes) > 0:
                hp.heappush(self.listOfActivityEpisodes, (1439, endAct))
                continue

            # If there are subsequent activities with a start time of 0 then we need to
            # move it and not process it as a start of day reconciliation
            if endAct.startTime == 0 and len(self.listOfActivityEpisodes) > 0:
                endAct.startOfDay = False

            # First act
            if stAct.startOfDay == True:
                stAct = self._adjust_first_episode(stAct, endAct)
                continue

            # Last act
            if endAct.endOfDay == True:
                stAct = self._adjust_last_episode(stAct, endAct)
                continue

            # intermediate acts
            stAct = self._move_episode(stAct, endAct)
    	    print '\tMOVEDD EPISODE -', stAct            
            
        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))


    def _return_start_activity(self):
        stActFound = False
        
        while (not stActFound):
            act = hp.heappop(self.listOfActivityEpisodes)[1]
        
            if act.scheduleId == 1:
                stActFound = True
            else:
                if act.startTime == 0:
                    hp.heappush(self.listOfActivityEpisodes, (1, act))
                else:
                    hp.heappush(self.listOfActivityEpisodes, (act.startTime, act))
        
        return act

    def _collate_results(self):
        #print self.listOfActivityEpisodes
        #print self.reconciledActivityEpisodes
        resList = []
        for recAct in self.listOfActivityEpisodes:
            actObject = recAct[1]
            resList.append([actObject.scheduleId, 
                            actObject.actType, actObject.startTime, actObject.endTime,
                            actObject.location, actObject.duration])
        return array(resList)

    
    def _adjust_first_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        adjDenominator = stAct.duration + 0.5*endAct.duration

        if prismDur > tt:
            pass
        else:
            print '\t\t-- ADJUSTING FOR FIRST PRISM OF DAY --'

            adjDur = tt - prismDur

            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * stAct.duration/adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            #Update duration
            stAct.duration = stAct.endTime - stAct.startTime

            # Modify start of the Ending Activity for the prism
            endAct_StAdj = adjDur * 0.5*endAct.duration/adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * endAct_StAdj
            endAct.endTime = endAct.endTime + endAct_EndAdj

            if endAct.endTime > 1439:
                endAct.endTime = 1439
            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime


        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def _adjust_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        adjDenominator = 0.5*stAct.duration + 0.5*endAct.duration + tt

        if prismDur > tt:
            pass
        else:
            print '\t\t-- ADJUSTING FOR ACTIVITIES WITHIN A DAY --'

            adjDur = tt - prismDur

            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * 0.5*stAct.duration/adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            #Update duration
            stAct.duration = stAct.endTime - stAct.startTime

            # Modify start of the Ending Activity for the prism
            endAct_StAdj = adjDur * 0.5*endAct.duration/adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * endAct_StAdj
            endAct.endTime = endAct.endTime + endAct_EndAdj

            if endAct.endTime > 1439:
                endAct.endTime = 1439
            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime


        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct


    def _move_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime
        
        if prismDur > tt:
            pass
        else:
            print "\t\t-- MOVING WITHIN DAY FIXED ACTIVITY --"

            adjDur = tt - prismDur

            # Modify start of the Ending Activity for the prism
            endAct.startTime = endAct.startTime + adjDur
            # Modify end of the Ending Activity for the prism
            rndNum = self.rndGen.return_random_variables()
            endAct_EndAdj = rndNum * 0.5 * adjDur
            endAct.endTime = endAct.endTime + endAct_EndAdj
            
                #If the adjusted endtime is less than the adjusted starttime
            if endAct.endTime < endAct.startTime:
                rndNum = self.rndGen.return_random_variables()
                endAct.endTime = endAct.startTime + rndNum * endAct.duration


            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime
            
        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def _adjust_last_episode(self, stAct, endAct):
        tt = self._extract_travel_time(stAct.location, endAct.location)
        prismDur = endAct.startTime - stAct.endTime

        adjDenominator = 0.5*stAct.duration + endAct.duration

        if prismDur > tt:
            pass
        else:
            print "\t\t-- ADJUSTING FOR LAST PRISM OF DAY --"
            adjDur = tt - prismDur

            # Modify end of the Starting Activity for the prism
            stAct_EndAdj = adjDur * 0.5*stAct.duration/adjDenominator
            stAct.endTime = stAct.endTime - stAct_EndAdj
            #Update duration
            stAct.duration = stAct.endTime - stAct.startTime

            # Modify start of the Ending Activity for the prism
            endAct_StAdj = adjDur * endAct.duration/adjDenominator
            endAct.startTime = endAct.startTime + endAct_StAdj
            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
        return endAct

    def adjust_activity_schedules(self, seed=1):
	self.reconciledActivityEpisodes = []
	self.seed = seed
	self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
	self._adjust_schedule()
	self.listOfActivityEpisodes = copy.deepcopy(self.reconciledActivityEpisodes)


    def _adjust_schedule(self):
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):
            
            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex, 
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
	    print '\tFIRST ACT OF PRISM - ', stAct
	    print '\tLAST ACT OF PRISM -  ', endAct
	
            if endAct.endTime == 1439 and len(self.listOfActivityEpisodes) > 0:
                hp.heappush(self.listOfActivityEpisodes, (1439, endAct))
                continue

            # If there are subsequent activities with a start time of 0 then we need to
            # move it and not process it as a start of day reconciliation
            if endAct.startTime == 0 and len(self.listOfActivityEpisodes) > 0:
                endAct.startOfDay = False

            # First act
            if stAct.startOfDay == True:
                stAct = self._adjust_first_episode(stAct, endAct)
                continue

            # Last act
            if endAct.endOfDay == True:
                stAct = self._adjust_last_episode(stAct, endAct)
                continue

            # intermediate acts
            stAct = self._adjust_episode(stAct, endAct)
    	    print '\tADJUSTEDD EPISODE -', stAct            
            
        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))



    def _extract_travel_time(self, st_loc, end_loc):
        # Currently assume that the travel time between any two 
        # activity episodes that are not same is 30 mins
        # TODO: Needs to be replaced with querying the travel skims
        if st_loc == end_loc:
            tt = 1
        tt = 30
        return tt

