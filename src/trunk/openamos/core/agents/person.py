import heapq as hp
from numpy import array

from openamos.core.models.abstract_random_distribution_model import RandomDistribution


class Person(object):
    def __init__(self, hid, pid):
        self.hid = hid
        self.pid = pid
        self.listOfActivityEpisodes = []
        self.reconciledActivityEpisodes = []


    def add_and_reconcile_episodes(self, activityEpisodes, seed=1):
        self.seed = seed
        print self.hid * self.pid + self.seed
        self.rndGen = RandomDistribution(int(self.hid * self.pid + self.seed))
        self.add_episodes(activityEpisodes)
        self._reconcile_schedule()
        results = self._collate_results()
        return results
        
        
    def add_episodes(self, activityEpisodes):
        for activity in activityEpisodes:
            hp.heappush(self.listOfActivityEpisodes, (activity.startTime, activity))

    def _reconcile_schedule(self):

        stAct = hp.heappop(self.listOfActivityEpisodes)[1]

        while (len(self.listOfActivityEpisodes) > 0):
            endAct = hp.heappop(self.listOfActivityEpisodes)[1]

            #print '\tSTART ACTIVITY OF PRISM --', stAct, stAct.startOfDay
            #print '\tEND ACTIVITY OF PRISM --', endAct, endAct.endOfDay

        
            if stAct.startOfDay == True:
                stAct = self._adjust_first_episode(stAct, endAct)
                continue

            if stAct.startOfDay == False and endAct.endOfDay == False:
                stAct = self._move_episode(stAct, endAct)
                continue

            if endAct.endOfDay == True:
                stAct = self._adjust_last_episode(stAct, endAct)
                continue
        

        hp.heappush(self.reconciledActivityEpisodes, (stAct.startTime, stAct))

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
        pass
            

            
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
            endAct_EndAdj = rndNum * endAct_StAdj
            endAct.endTime = endAct.endTime + endAct_EndAdj
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
            endAct_EndAdj = rndNum * adjDur
            endAct.endTime = endAct.endTime + endAct_EndAdj
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

