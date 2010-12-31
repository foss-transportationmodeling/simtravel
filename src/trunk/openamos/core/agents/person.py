import heapq as hp
from numpy import array,zeros

from openamos.core.models.abstract_random_distribution_model import RandomDistribution


class Person(object):
    def __init__(self, hid, pid):
        self.hid = hid
        self.pid = pid
        self.listOfActivityEpisodes = []
        self.reconciledActivityEpisodes = []


    def add_and_reconcile_episodes(self, activityEpisodes, seed=1):
        self.seed = seed
        #print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
        self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        self._check_for_conflicts()
        results = self._collate_results()
        return results
        
        
    def add_episodes(self, activityEpisodes):
        for activity in activityEpisodes:
            hp.heappush(self.listOfActivityEpisodes, (activity.startTime, activity))

    def _reconcile_schedule(self):

        #stAct = hp.heappop(self.listOfActivityEpisodes)[1]
        stAct = self._return_start_activity()

        while (len(self.listOfActivityEpisodes) > 0):
            
            endAct = hp.heappop(self.listOfActivityEpisodes)[1]
            # If the second activity is identified as end of the day vertex, 
            # then we move its location in the heap to end so that the adjustment
            # for this activity happens at the end after all other activities have been
            # reconciled
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
        for recAct in self.reconciledActivityEpisodes:
            actObject = recAct[1]
            resList.append([actObject.scheduleId, 
                            actObject.actType, actObject.startTime, actObject.endTime,
                            actObject.location, actObject.duration])
        return array(resList)

    def _check_for_conflicts(self):
        checkArray = zeros((1440,))
        for recAct in self.reconciledActivityEpisodes:        
            actObject = recAct[1]
            checkArray[actObject.startTime:actObject.endTime] += 1
        if (checkArray > 1).sum() > 1:
            for recAct in self.reconciledActivityEpisodes:
                print recAct

            print 'TEHRE ARE STILL CONFLICTS'
            raise Exception, "THE SCHEDULES ARE STILL MESSED UP"
            
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

    def _extract_travel_time(self, st_loc, end_loc):
        # Currently assume that the travel time between any two 
        # activity episodes that are not same is 30 mins
        # TODO: Needs to be replaced with querying the travel skims
        if st_loc == end_loc:
            tt = 1
        tt = 30
        return tt

