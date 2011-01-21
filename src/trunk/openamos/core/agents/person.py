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
        self.scheduleConflictIndicator = zeros((1440,1))

    def reconcile_activity_schedules(self, seed=1):
        self.reconciledActivityEpisodes = []
        self.seed = seed
        #print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
        #self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        self.scheduleConflictIndicator = zeros((1440, 1))
        self.listOfActivityEpisodes = copy.deepcopy(self.reconciledActivityEpisodes)
        for actStart, act in self.listOfActivityEpisodes:
            self._update_schedule_conflict_indicator(act, add=True)
        

        #results = self._collate_results()
        #return results
        

    def add_episodes(self, activityEpisodes, temp=False):
        for activity in activityEpisodes:
            #activity.personid = self.pid
	    if activity.startOfDay and not temp:
		self.firstEpisode = activity
	    if activity.endOfDay and not temp:
	        self.lastEpisode = activity
            hp.heappush(self.listOfActivityEpisodes, (activity.startTime, activity))
            self.actCount += 1
            #self.scheduleIds.append(activity.scheduleId)
            self._update_schedule_conflict_indicator(activity, add=True)


    def remove_episodes(self, activityEpisodes):
	for activity in activityEpisodes:
	    self.listOfActivityEpisodes.remove((activity.startTime, activity))
	    self.actCount -= 1
	    #self.scheduleIds.remove(activity.scheduleId)
            self._update_schedule_conflict_indicator(activity, add=False)

    def _update_schedule_conflict_indicator(self, activity, add=True):
        if add:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime,:] += 1
        else:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime,:] -= 1            

        
    def _check_for_conflicts(self):
        conflict = (self.scheduleConflictIndicator[:,:] > 1).sum()
        if conflict > 0:
            print '\t\t\t\tTHERE ARE CONFLICTS IN THE SCHEDULE FOR PERSON - %s and CONFLICT - %s' %(self.pid,
                                                                                                    conflict)
            return False
        return True

    def _check_for_ih_conflicts(self, activity):
        conflict = (self.scheduleConflictIndicator[:,:] > 1).sum()
        
        conflictActs = self._identify_conflict_activities([activity])
        checkConflictActsLocation = self._check_location_match(activity,
                                                               conflictActs)
        

        if (conflict == activity.duration) and checkConflictActsLocation:
            print """\t\t\t\tThere is some person at the current location """\
                """and the activities temporal vertices fit in with this person - %s""" %(self.pid)
            for act in conflictActs:
                act.dependentPersonId = 99

            return True
        else:
            return False


    def _check_location_match(self, activity, conflictActs):
        for act in conflictActs:
            if act.location <> activity.location:
                return False

        return True

            
    def _check_for_travel_threshold(self):
        pass

    def _check_for_roundtrip_threshold(self):
        pass


    def _conflict_duration(self):
        conflict = (self.scheduleConflictIndicator[:,:] > 1).sum()
        return conflict


    def _conflict_duration_with_activity(self, activity):
        stTime = activity.startTime
        endTime = activity.endTime
        #print 'stTime - ', stTime, 'endTime', endTime
        conflict = (self.scheduleConflictIndicator[stTime:endTime, :] > 1).sum()
        return conflict

    def _identify_conflict_activities(self, activityList):
        # ONLY IDENTIFIES ACTIVITIES THAT PERFECTLY FIT WITHIN THE SCHEDULE
        
        actConflicts = []
        
        for act in activityList:
            actConflict = self._identify_conflict_activity(act)
            
            if actConflict is not None:
                actConflicts.append(actConflict)
        return actConflicts


    def _identify_conflict_activity(self, activity):
        for stAct, act in self.listOfActivityEpisodes:
            if (activity.startTime >= act.startTime and 
                activity.endTime <= act.endTime):
                return act


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
	

    def check_start_of_day(self, refEndTime):
	if self.firstEpisode.endTime >= refEndTime:
            #if self.firstEpisode.dependentPersonId == 0:
            #    self.firstEpisode.dependentPersonId = depPersonId
            self.firstEpisode.dependentPersonId = 99
	    return True
	else:
	    return False
	
	

    def check_end_of_day(self, refStartTime):
	if self.lastEpisode.startTime <= refStartTime:
            #if self.lastEpisode.dependentPersonId == 0:
            #    self.lastEpisode.dependentPersonId = depPersonId
            self.lastEpisode.dependentPersonId = 99
	    return True
	else:
	    return False



    def move_start_of_day(self, refEndTime):
        #print 'MOVED START from - ', self.firstEpisode.endTime, refEndTime, 
        self.scheduleConflictIndicator[self.firstEpisode.endTime:refEndTime, 
                                       :] += 1

	self.firstEpisode.endTime = refEndTime 
        self.firstEpisode.dependentPersonId = 99
	self.firstEpisode.duration = (self.firstEpisode.endTime - 
				      self.firstEpisode.startTime)
        print 'START MOVED', self.firstEpisode


    def move_end_of_day(self, refStartTime):
        #print 'MOVED END from - ', self.lastEpisode.startTime, refStartTime
        self.scheduleConflictIndicator[refStartTime:self.lastEpisode.startTime, 
                                       :] += 1

	self.lastEpisode.startTime = refStartTime 
        self.lastEpisode.dependentPersonId = 99
	self.lastEpisode.duration = (self.lastEpisode.endTime -
				     self.lastEpisode.startTime)
        print 'END MOVED', self.lastEpisode

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
        #print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
        #stAct = hp.heappop(self.listOfActivityEpisodes)[1]
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):
            
            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex, 
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
	    #print len(self.listOfActivityEpisodes), len(self.reconciledActivityEpisodes)
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

    def extract_skims(self, skimsMatrix):
        # hstack a column for the skims that need to be extracted for the                                                           
        # location pair                                                                                                             
        originLocColName = spatialconst.startConstraint.locationField
        destinationLocColName = spatialconst.endConstraint.locationField

        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)


        vals = skimsMatrix2[originLocColVals, destinationLocColVals]

        rowsEqualsDefault = vals.mask
        vals[rowsEqualsDefault] = 0
        #vals.shape = (data.rows,1)                                                                                                 
        if spatialconst.asField:
            colName = spatialconst.asField
        else:
            colName = spatialconst.skimField

        sampleVarDict = {'temp':[colName]}
        self.append_cols_for_dependent_variables(data, sampleVarDict)

        #print vals[:,0]                                                                                                            
        data.insertcolumn([colName], vals)

        return data
