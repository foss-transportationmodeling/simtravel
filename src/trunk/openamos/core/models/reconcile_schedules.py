from openamos.core.agents.person import Person
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and

class ReconcileSchedules(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

    def create_indices(self, data):
        houseIdsUnique, hId_reverse_indices = unique(data.columns([self.specification.hidName]).data,
                                                 return_inverse=True)


        #print data.data[:10,:].astype(int)
        #print data._colnames
        #print houseIdsUnique, 

        #raw_input()
        countOfHid = 0


        self.indices = []
        self.index = 0
        for hid in houseIdsUnique:
            hIdIndices = hId_reverse_indices == countOfHid
            #hIdIndices.shape = (hIdIndices.sum(), )
            schedulesForHid = data.rowsof(hIdIndices)
            print 'houseID, number of household records - ',hid, hIdIndices.sum(), schedulesForHid.rows
            print schedulesForHid.data.astype(int)
            
            pIdsUnique, pId_reverse_indices = unique(schedulesForHid.columns([self.specification.pidName]).data,
                                                  return_inverse=True)
            print '\tperson Ids - ', pIdsUnique
            countOfPid = 0
            for pid in pIdsUnique:
                pIdIndices = pId_reverse_indices == countOfPid
                print ('\tperson id', pid, ' number of person records-', pIdIndices.sum(), 
                       ' start-', self.index, ' end-', (self.index + pIdIndices.sum()))
                print data.data[self.index:(self.index + pIdIndices.sum()), :].astype(int)
                
                self.indices.append([hid, pid, self.index, self.index + pIdIndices.sum()])

                self.index += pIdIndices.sum()
                countOfPid += 1

            countOfHid += 1


        self.indices = array(self.indices)
        print self.indices
            #hIdIndex += schedulesForHid.rows
            #raw_input()


    def resolve_consistency(self, data, seed):

        data.sort([self.specification.hidName,
                   self.specification.pidName,
                   self.specification.scheduleidName])

        # Create Index Matrix
        self.create_indices(data)

        
        

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



        row = 0
        
        for perIndex in self.indices:
            #schedulesRowIndForHh = array(houseIdsCol == hid)
            #schedulesRowIndForHh.shape = (schedulesRowIndForHh.shape[0],)

            #schedulesForHh = data.rowsof(schedulesRowIndForHh)

            #pIdsColForHh = schedulesForHh.columns([self.specification.pidName]).data
            #pIdsUnique = unique(pIdsColForHh)

            #pIdsCol = data.columns([self.specification.pidName]).data

            """
            for pid in pIdsUnique:
                fullRecsInd = array([False]*data.rows)
                fullRecsInd.shape = (data.rows, )

                print pid, hid

                schedulesRowIndForPer = array(logical_and(pIdsCol == pid, houseIdsCol == hid))
                schedulesRowIndForPer.shape = (schedulesRowIndForPer.shape[0],)
                schedulesForPerson = data.rowsof(schedulesRowIndForPer)
            
                #print 'Raw schedules for hid:%s and pid:%s' %(hid, pid)
                print schedulesForPerson._colnames
                print 'ORIGINAL'
                #print schedulesForPerson.data.astype(int)
                print data.rowsof(schedulesRowIndForPer).data.astype(int)

            """
            schedulesForPerson = DataArray(data.data[perIndex[2]:perIndex[3],:], data.varnames)
            print schedulesForPerson.data.astype(int)
           #raw_input()

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

            personObject = Person(perIndex[0], perIndex[1])
            reconciledSchedules = personObject.add_and_reconcile_episodes(activityList)
                

            #recsInd = array([False]*data.rows)
            #recsInd.shape = (data.rows,)
            
            #recsInd[perIndex[2]:perIndex[3]] = True

            i = 0
            for colN in colNames:
                data.setcolumn(colN, reconciledSchedules[:,i], start=perIndex[2], end=perIndex[3])
                i += 1
                                  

            print 'MODIFIED DATA'
            print data.rowsof(recsInd).data.astype(int)
            #print reconciledSchedules.astype(int)
            #print data.data.shape
            #raw_input()
                
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
        
