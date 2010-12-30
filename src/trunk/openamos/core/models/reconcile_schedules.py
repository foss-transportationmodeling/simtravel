from openamos.core.agents.person import Person
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and

class ReconcileSchedules(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification



    def resolve_consistency(self, data, seed):
        houseIdsCol = data.columns([self.specification.hidName]).data
        houseIdsUnique = unique(houseIdsCol)
        #print houseIdsUnique

        schidCol = data._colnames[self.specification.scheduleidName]
        actTypeCol = data._colnames[self.specification.activitytypeName]
        locidCol = data._colnames[self.specification.locationidName]
        sttimeCol = data._colnames[self.specification.starttimeName]
        endtimeCol = data._colnames[self.specification.endtimeName]
        durCol = data._colnames[self.specification.durationName]

        colNames = [self.specification.scheduleidName, 
                    self.specification.activitytypeName,
                    self.specification.starttimeName,
                    self.specification.endtimeName,
                    self.specification.locationidName,
                    self.specification.durationName]

        


        for hid in houseIdsUnique:
            schedulesRowIndForHh = array(houseIdsCol == hid)
            schedulesRowIndForHh.shape = (schedulesRowIndForHh.shape[0],)


            schedulesForHh = data.rowsof(schedulesRowIndForHh)

            pIdsColForHh = schedulesForHh.columns([self.specification.pidName]).data
            pIdsUnique = unique(pIdsColForHh)

            pIdsCol = data.columns([self.specification.pidName]).data


            for pid in pIdsUnique:
                fullRecsInd = array([False]*data.rows)
                fullRecsInd.shape = (data.rows, )

                print pid, hid

                schedulesRowIndForPer = array(logical_and(pIdsCol == pid, houseIdsCol == hid))
                schedulesRowIndForPer.shape = (schedulesRowIndForPer.shape[0],)
                schedulesForPerson = data.rowsof(schedulesRowIndForPer)
            
                #print 'Raw schedules for hid:%s and pid:%s' %(hid, pid)
                #print schedulesForPerson._colnames
                #print 'ORIGINAL'
                #print schedulesForPerson.data.astype(int)

                activityList = []
                for sched in schedulesForPerson.data:
                    scheduleid = sched[schidCol]
                    activitytype = sched[actTypeCol]
                    locationid = sched[locidCol]
                    starttime = sched[sttimeCol]
                    endtime = sched[endtimeCol]
                    duration = sched[durCol]
                    
                    actepisode = ActivityEpisode(scheduleid, activitytype, locationid, 
                                                 starttime, endtime, duration)
                    activityList.append(actepisode)
                personObject = Person(hid, pid)
                reconciledSchedules = personObject.add_and_reconcile_episodes(activityList)
                


                i = 0
                for colN in colNames:
                    data.setcolumn(colN, reconciledSchedules[:,i], schedulesRowIndForPer)
                    i += 1
                                  

                #print 'MODIFIED DATA'
                #print data.rowsof(schedulesRowIndForPer).data.astype(int)
                #print data.data.shape
                
                
        return data

import unittest
from numpy import genfromtxt, unique
from openamos.core.data_array import DataArray

class TestReconcileModel(unittest.TestCase):
    def setUp(self):
        self.data = genfromtxt("/home/kkonduri/simtravel/test/mag_zone/schedule_txt.csv", delimiter=",", dtype=int)
        colNames = ['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime', 
                    'endtime', 'duration']
        self.actSchedules = DataArray(self.data, colNames)


        

    def test_retrieve_loop_ids(self):
        houseIdsCol = self.actSchedules.columns(['houseid']).data
        houseIdsUnique = unique(houseIdsCol)
        print houseIdsUnique

        
        for hid in houseIdsUnique:
            schedulesRowsIndForHh = houseIdsCol == hid
            schedulesForHh = self.actSchedules.rowsof(schedulesRowsIndForHh)

            pIdsCol = schedulesForHh.columns(['personid']).data
            pIdsUnique = unique(pIdsCol)

            for pid in pIdsUnique:
                schedulesRowIndForPer = pIdsCol == pid
                schedulesForPerson = schedulesForHh.rowsof(schedulesRowIndForPer)
            
                #print 'Raw schedules for hid:%s and pid:%s' %(hid, pid)
                #print schedulesForPerson

                activityList = []
                for sch in schedulesForPerson.data:
                    scheduleid = sch[2]
                    activitytype = sch[3]
                    locationid = sch[4]
                    starttime = sch[5]
                    endtime = sch[6]
                    duration = sch[7]
                    
                    actepisode = ActivityEpisode(scheduleid, activitytype, locationid, 
                                                 starttime, endtime, duration)
                    activityList.append(actepisode)
                personObject = Person(hid, pid)
                personObject.add_and_reconcile_episodes(activityList)
                #print '\tReconciled Activity schedules - ', personObject.reconciledActivityEpisodes
                #raw_input()
        #pid = unique(self.actSchedules.columns(['houseid', 'personid']).
        #acts = self.actSchedules

        #def 


if __name__ == "__main__":
    unittest.main()
        
