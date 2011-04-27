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
        self.scheduleConflictIndicator = zeros((2880,1))

    def reconcile_activity_schedules(self, seed=1):
        self.reconciledActivityEpisodes = []
        self.seed = seed
        #print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
        #self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        self.scheduleConflictIndicator = zeros((2880, 1))
        self.listOfActivityEpisodes = copy.deepcopy(self.reconciledActivityEpisodes)
        for actStart, act in self.listOfActivityEpisodes:
            self._update_schedule_conflict_indicator(act, add=True)
        


    def adjust_schedules_given_arrival_info(self, seed=1):
	if self.destAct.startTime == self.actualArrival:
	    print '\n-- Arrived as expected; nothing needs to be done --'

	if self.destAct.startTime > self.actualArrival:
	    print '\n-- Arrived earlier than expected; minor adjustment needed for start of the subsequent activity --'
	    self.add_anchor_activity()

	if self.destAct.startTime < self.actualArrival:
	    print '\n-- Arrived later than expected; adjustment for activities needs to happen here --'
	    self.adjust_push_subsequent_activities()

    def add_anchor_activity(self):
	anchorAct = self.destAct
	#anchorAct.actType += 25
	anchorAct.actType = 598
	anchorAct.startTime = self.actualArrival
	anchorAct.endTime = self.actualArrival	
	anchorAct.duration = 0
	self.add_episodes([anchorAct])
	print 'Dest Act - ', self.destAct
	print 'Anchor Act - ', anchorAct
	#raw_input('adding an anchor activity')	


    def adjust_push_subsequent_activities(self):
	#raw_input('adjusting and pushing subsequent activities')

	self.add_anchor_activity()	    
	

	# Adjusting if only the first activity is affected
	firstExpActAfterArrival = self.expectedActivities[0]
	
	if firstExpActAfterArrival.startTime < self.actualArrival and firstExpActAfterArrival.endTime > self.actualArrival:
	    self.move_start(firstExpActAfterArrival, self.actualArrival + 1)
	    print ('Only first activity needs to be adjusted')
	    return

	# Adjusting when more than one activity is affected: Push all activities
	missedActsStillToPursue = []
	actsToPursue = []
	for act in self.expectedActivities:
	    if (act.endTime < self.actualArrival and act.dependentPersonId > 0):
		missedActsStillToPursue.append(act)
	    else:
	        actsToPursue.append(act)

	print 'Missed Activities'
	for act in missedActsStillToPursue:
	    print '\t', act

	print 'Activities to Pursue'
	for act in actsToPursue:
	    print '\t', act

	actEnd = self.actualArrival
	for act in missedActsStillToPursue + actsToPursue:
	    print '-->This ', act, ' is being moved by ', actEnd-act.startTime
	    if actEnd-act.startTime > 0:
		moveByValue = copy.deepcopy(actEnd-act.startTime)
		self.move_start_end(act, moveByValue)
	    actEnd = copy.deepcopy(act.endTime)
	
	print('Push all dependent activities that were missed and subsequent activities')



    def add_episodes(self, activityEpisodes, temp=False):
	print 'Before adding: Number of acts - ', len(self.listOfActivityEpisodes)
        for activity in activityEpisodes:
            #activity.personid = self.pid
	    if activity.startOfDay and not temp:
		self.firstEpisode = activity
	    if activity.endOfDay and not temp:
	        self.lastEpisode = activity
            hp.heappush(self.listOfActivityEpisodes, (activity.startTime, activity))
            self.actCount += 1
            self._update_schedule_conflict_indicator(activity, add=True)
	print 'After adding: Number of acts - ', len(self.listOfActivityEpisodes)

    def remove_episodes(self, activityEpisodes):
        #print 'CURRENT ACTIVIITES FOR PERSON - ', self.hid, self.pid
        #for currActivities in self.listOfActivityEpisodes:
        #    print '\t', currActivities

	for activity in activityEpisodes:
            #print (activity.startTime, activity)
	    try:
	        self.listOfActivityEpisodes.remove((activity.startTime, activity))
	    except ValueError, e:
		print 'Warning: Trying to remove a copy of the activityObject: %s' %e
		raise ValueError, 'Warning: Trying to remove a copy of the activityObject: %s' %e
		
	
            self._update_schedule_conflict_indicator(activity, add=False)

    def _update_schedule_conflict_indicator(self, activity, add=True):
        if add:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime,:] += 1
        else:
            self.scheduleConflictIndicator[activity.startTime:activity.endTime,:] -= 1            


    def adjust_child_dependencies(self, activityList):
        conflictActs = self._identify_conflict_activities(activityList)
        ownActs, depActs = self.return_own_dep_acts(conflictActs)
        #minStartTime, maxEndTime = self.return_min_max_time_of_activities(depActs)
        #print 'Min Start Time - %s and Max End Time - %s' %(minStartTime, maxEndTime)
        minStartTime = activityList[0].startTime
        maxEndTime = activityList[-1].endTime
        print 'DEPENDENT ACTS'
        for act in depActs:
            print '\t', act

        print 'OWN ACTIVITIES'
        for act in ownActs:
            print '\t', act
            
        print 'Min Start Time - %s and Max End Time - %s' %(minStartTime, maxEndTime)

        if len(ownActs) == 1:
            print '\tException, Only one activity of the adult that needs to be modified'            
            self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
        elif len(ownActs) > 1:
            print '\tException, More than one activity of the adult person need to be modified/deleted'
            self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
        else:
            raise Exception, 'NO CONFLICTS??'

        """
        if len(depActs) == 0:
            self.adjust_merged_own_acts(ownActs, minStartTime, maxEndTime)
        else:
            if len(ownActs) == 1:
                print '\tException, Only one activity of the adult that needs to be modified'            
                self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
            elif len(ownActs) > 1:
                print '\tException, More than one activity of the adult person need to be modified/deleted'
                self.adjust_and_delete_own_activities(ownActs, minStartTime, maxEndTime)
            else:
                print '\tException, NO CONFLICTS??'
        """        
    def adjust_merged_own_acts(self, ownActs, minStartTime, maxEndTime):
        # Remove completely engulfed own activities that are colliding 
        # with dependent activities of children
        newOwnActs = []
        for act in ownActs:
            if (act.startTime > minStartTime and act.endTime < maxEndTime):
                print '\tRemoving activity', act
                #raw_input()
                self.remove_episodes([act])
            else:
                newOwnActs.append(act)

        newOwnActs = self.sort_acts(newOwnActs)
        
        firstAct = newOwnActs[0]
        
        for nextActIndex in range(len(newOwnActs) - 1):
            nextAct = newOwnActs[nextActIndex + 1]
            print firstAct, nextAct, 'BEFORE'

            #self.remove_episodes([firstAct, nextAct])
            overlap = self._conflict_duration_with_activity(nextAct)
            overlapAdj = int(overlap/2)

            firstActRef = firstAct.endTime - overlapAdj
            self.move_end(firstAct, firstActRef)

            nextActRef = nextAct.startTime + (overlap - overlapAdj) + 1
            self.move_start(nextAct, nextActRef)
            print overlap, overlapAdj, firstActRef, nextActRef

            firstAct = nextAct


            print firstAct, nextAct, 'AFTER'
            raw_input()

    def sort_acts(self, actList):
        actVerticesDict = {}

        for act in actList:
            actVerticesDict[(act.startTime, act.endTime)] = act

        actVerticesList = actVerticesDict.keys()
        actVerticesList.sort()
        actList = [actVerticesDict[(st, end)] for (st, end) in actVerticesList]

        return actList
        



    def adjust_one_activity(self, ownAct, minStartTime, maxEndTime):
        #return
        # TODO: NEED TO INCLUDE THE NECESSARY TRAVEL TIME LATER
        # Adjusting start term episode
        print 'ownAct start - %s and ownAct end - %s' %(ownAct.startTime, ownAct.endTime)
        if (ownAct.startTime == 0 and ownAct.endTime >= minStartTime):
            self.move_end(ownAct, minStartTime - 1)
            return

        # Adjusting end term episode
        if (ownAct.endTime == 1439 and ownAct.startTime <= maxEndTime):
            self.move_start(ownAct, maxEndTime + 1)
            return

        # Own activity is engulfing the travel episode
        if ownAct.startTime < minStartTime and ownAct.endTime > maxEndTime:
            if ((minStartTime - ownAct.startTime) > (ownAct.endTime - maxEndTime)):
                self.move_end(ownAct, minStartTime - 1)
            else:
                self.move_start(ownAct, maxEndTime + 1)
            return 

        if (ownAct.endTime >= minStartTime and ownAct.endTime <= maxEndTime):
            self.move_end(ownAct, minStartTime - 1)
            return

        if (ownAct.startTime >= minStartTime and ownAct.startTime <= maxEndTime):
            self.move_start(ownAct, maxEndTime + 1)
            return

        print ownAct
        raise Exception, 'DONE NOTHING'
    def adjust_and_delete_own_activities(self, ownActs, minStartTime, maxEndTime):
        #return
        for act in ownActs:
            print 'THIS IS WHAT IS BEING ADJUSTED'
            if (act.startTime == minStartTime and act.endTime == maxEndTime and
                act.actType == 100):
                continue
            if (act.startTime == minStartTime and act.endTime == maxEndTime and 
                act.actType <> 100):
                print '\tRemoving activity', act
                self.remove_episodes([act])
                continue
            if (act.startTime >= minStartTime - 1 and act.endTime <= maxEndTime + 1):
                print '\tRemoving activity', act
                #raw_input()
                self.remove_episodes([act])
            else:
                
                self.adjust_one_activity(act, minStartTime, maxEndTime)


    def return_min_max_time_of_activities(self, activityList):
        minStartTime = 1440
        maxEndTime = 0
        for act in activityList:
            if act.startTime < minStartTime:
                minStartTime = act.startTime
            if act.endTime > maxEndTime:
                maxEndTime = act.endTime

        return minStartTime, maxEndTime

    def return_own_dep_acts(self, activityList):
        ownActsList = []
        depActsList = []
        for act in activityList:
            if act.dependentPersonId <> 99:
                ownActsList.append(act)
            elif act.dependentPersonId == 99 and (act.startTime == 0 or act.endTime == 1439):
                ownActsList.append(act)
            else:
                depActsList.append(act)
        return ownActsList, depActsList

        
    def _check_for_conflicts(self):
        conflict = (self.scheduleConflictIndicator[:,:] > 1).sum()
        if conflict > 0:
            print '\t\t\t\tTHERE ARE CONFLICTS IN THE SCHEDULE FOR PERSON - %s and CONFLICT - %s' %(self.pid,
                                                                                                    conflict)
            return False
        return True

    def _check_for_conflicts_with_activity(self, activity):
        if type(activity) == list:
            actList = activity
        else:
            actList = [activity]
        conflict = 0

        for activity in actList:
            stTime = activity.startTime
            endTime = activity.endTime
        #print 'stTime - ', stTime, 'endTime', endTime
            conflictAct = (self.scheduleConflictIndicator[stTime:endTime, :] > 1).sum()
            conflict += conflictAct
            
        if conflict > 0:
            print '\t\t\t\tTHERE ARE CONFLICTS IN THE SCHEDULE FOR PERSON - %s and CONFLICT - %s ' %(self.pid,
                                                                                                     conflict)
            return False
        return True

    def _check_for_ih_conflicts(self, activity):
        conflict = self._conflict_duration_with_activity(activity)
        
        self.remove_episodes([activity])

        conflictActs = self._identify_conflict_activities([activity])
        checkConflictActsLocation = self._check_location_match(activity,
                                                               conflictActs)
        
        #print 'Person Id - ', self.pid
        #print 'conflictActs', conflictActs
        
        #print 'conflict', conflict
        #print 'Same Location', checkConflictActsLocation

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
                #print act.location, activity.location
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
        # conflict with respect to a list of activities including chains
        
        actConflicts = []
        for act in activityList:
            actConflict = self._identify_conflict_activity(act)
            
            if actConflict is not None:
                for newConfAct  in actConflict:
                    if newConfAct not in actConflicts:
                        actConflicts.append(newConfAct)

        #actConflicts = self.sort_acts(actConflicts)
        return actConflicts


    def _identify_conflict_activity(self, activity):
        # conflict wrt one activity
        actList = []
        for stAct, act in self.listOfActivityEpisodes:
            #print len(self.listOfActivityEpisodes)
            #print 'ACTIVITY COORDINATES', activity.startTime, activity.endTime
            #print 'CONFLICT COORDINATES', act.startTime, act.endTime
            if ((act.startTime >= activity.startTime and act.startTime <= activity.endTime) 
                or
                (act.endTime >= activity.startTime and act.endTime <= activity.endTime)
                or 
                (act.endTime > activity.endTime and act.startTime < activity.startTime)):
                actList.append(act)
        return actList


    def pop_earliest_activity(self):
	self.actCount -= 1
	activityStart, activity = hp.heappop(self.listOfActivityEpisodes)
	self.scheduleIds.remove(activity.scheduleId)
	return activityStart, activity



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


    def move_start_end(self, act, moveByValue):
	print '\tRemoving episode - ', act
	self.remove_episodes([act])
	act.startTime += moveByValue + 1
	act.endTime += moveByValue + 1
	print '\tAdding episode - ', act
	self.add_episodes([act])
	


    def move_start(self, act, value):
        self.remove_episodes([act])
        act.startTime = value
        act.duration = act.endTime - act.startTime
        if act.duration < 0:
            raise Exception, 'Incorrect adjustment - %s' %act
        self.add_episodes([act])



    def move_end(self, act, value):
        self.remove_episodes([act])
        act.endTime = value
        act.duration = act.endTime - act.startTime
        if act.duration < 0:
            raise Exception, 'Incorrect adjustment - %s' %act
        self.add_episodes([act])



    def move_start_of_day(self, refEndTime):
        #print 'MOVED START from - ', self.firstEpisode.endTime, refEndTime, 
        self.remove_episodes([self.firstEpisode])
        self.firstEpisode.endTime = refEndTime
        self.firstEpisode.duration = (self.firstEpisode.endTime - 
                                      self.firstEpisode.startTime) 
        
        self.firstEpisode.dependentPersonId = 99
        self.add_episodes([self.firstEpisode])
        """
        self.scheduleConflictIndicator[self.firstEpisode.endTime:refEndTime, 
                                       :] += 1

	self.firstEpisode.endTime = refEndTime 
        self.firstEpisode.dependentPersonId = 99
	self.firstEpisode.duration = (self.firstEpisode.endTime - 
				      self.firstEpisode.startTime)
        """
        print 'START MOVED', self.firstEpisode


    def move_end_of_day(self, refStartTime):
        #print 'MOVED END from - ', self.lastEpisode.startTime, refStartTime
        self.remove_episodes([self.lastEpisode])
        self.lastEpisode.startTime = refStartTime
        self.lastEpisode.duration = (self.lastEpisode.endTime - 
                                      self.lastEpisode.startTime) 
        
        self.lastEpisode.dependentPersonId = 99
        self.add_episodes([self.lastEpisode])
        """
        self.scheduleConflictIndicator[refStartTime:self.lastEpisode.startTime, 
                                       :] += 1

	self.lastEpisode.startTime = refStartTime 
        self.lastEpisode.dependentPersonId = 99
	self.lastEpisode.duration = (self.lastEpisode.endTime -
				     self.lastEpisode.startTime)
        """
        print 'END MOVED', self.lastEpisode

    def add_status_dependency(self, workstatus, schoolstatus, child_dependency):
        self.workstatus = workstatus
        self.schoolstatus = schoolstatus
        self.child_dependency = child_dependency

        self.extract_work_episodes()
        self.extract_school_episodes()
        
    def add_arrival_status(self, actualArrival, expectedArrival):
	self.actualArrival = actualArrival
	self.expectedArrival = expectedArrival
	self.extract_destination_episode()

    def extract_destination_episode(self):
	self.expectedActivities = []
	self.actualActivities = []
	
	for startTime, destAct in self.listOfActivityEpisodes:
	    if destAct.startTime == self.expectedArrival:
		break


	print 'Activities after expected arrival of %s - ' %(self.expectedArrival)
	#tempActList = copy.deepcopy(self.listOfActivityEpisodes)
	tempActList = []
	for actIndex in range(len(self.listOfActivityEpisodes)):
	    startTime, act = hp.heappop(self.listOfActivityEpisodes)
	    if act.startTime >= self.expectedArrival:
		self.expectedActivities.append(act)
		print '\t', act
	    hp.heappush(tempActList, (startTime, act))

	self.listOfActivityEpisodes = tempActList
	tempActList = []
	print 'Activities after actual arrival of %s - ' %(self.actualArrival)
	#tempActList = copy.deepcopy(self.listOfActivityEpisodes)
	for actIndex in range(len(self.listOfActivityEpisodes)):
	    startTime, act = hp.heappop(self.listOfActivityEpisodes)
	    if act.startTime >= self.actualArrival:
		self.actualActivities.append(act)
		print '\t', act
	    hp.heappush(tempActList, (startTime, act))
	self.listOfActivityEpisodes = tempActList
	self.destAct = copy.deepcopy(destAct)


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
	    intAct = self._move_episode(stAct, endAct) 
	    if intAct.endTime > 1439:
	        print("cannot be adjusted within the day")	
	    else:
		stAct = intAct

    	    print '\tMOVED EPISODE -', stAct            
            
	    print 'RECONCILED SCHEDULES', self.reconciledActivityEpisodes

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))


    def _return_start_activity(self):
        stActFound = False
        
        while (not stActFound):
            act = hp.heappop(self.listOfActivityEpisodes)[1]
        
            if act.startTime == 0:
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


    def _collate_results_aslist(self):
        #print self.listOfActivityEpisodes
        #print self.reconciledActivityEpisodes
	print 'Length before collaing results - ', len(self.listOfActivityEpisodes)
        resList = []
        for recAct in self.listOfActivityEpisodes:
            actObject = recAct[1]
            resList.append([self.hid, self.pid, actObject.scheduleId, 
                            actObject.actType, actObject.startTime, actObject.endTime,
                            actObject.location, actObject.duration, actObject.dependentPersonId])
        return resList

    
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
	    hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
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
		
    	    print 'End activity before limiting to 1439- ', endAct

	    if (endAct.endTime > 1439 and endAct.startTime < 1438) or (endAct.endTime < 1439):
		# i.e even by limiting the endtime we are doing OK because the starttime is still < 1438
		# in the other case where starttime >= 1438 we try to leave out the activity since it 
		# cannot be accommodated within the schedule

		endAct.endTime = 1438
		print("endtime less than starttime random * duration being added")
		hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))
	     

            #Update duration
            endAct.duration = endAct.endTime - endAct.startTime
            
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
        tt = 1
        return tt

    
