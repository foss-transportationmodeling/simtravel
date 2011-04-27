from openamos.core.agents.person import Person
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model
 
from numpy import array, logical_and, zeros, histogram

import time


class AdjustSchedules(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
	self.specification = specification
	self.activityAttribs = self.specification.activityAttribs
	self.arrivalInfoAttribs = self.specification.arrivalInfoAttribs

	self.colNames = [self.activityAttribs.hidName,
                         self.activityAttribs.pidName,
                         self.activityAttribs.scheduleidName, 
                         self.activityAttribs.activitytypeName,
                         self.activityAttribs.starttimeName,
                         self.activityAttribs.endtimeName,
                         self.activityAttribs.locationidName,
                         self.activityAttribs.durationName,
                         self.activityAttribs.dependentPersonName]

    def create_indices(self, data):
        idCols = data.columns([self.activityAttribs.hidName, 
                               self.activityAttribs.pidName]).data
        combId = idCols[:,0]*100 + idCols[:,1]
        
        print idCols[:20,:]
        print 'comid', combId[:20]
        print 'comid', combId[-20:]

        comIdUnique, comId_reverse_indices = unique(combId, return_inverse=True)

        print 'unique', comIdUnique[:20]
        print 'unique records', comIdUnique.shape
        print 'reverse indices', comId_reverse_indices[:20]
        print 'reverse indices', comId_reverse_indices[-20:]


        binsIndices = array(range(comId_reverse_indices.max()+2))
        
        histIndices = histogram(comId_reverse_indices, bins=binsIndices)
        print histIndices[0][:20]
        print histIndices[0][-20:]
        
        indicesRowCount = histIndices[0]
        
        indicesRow = indicesRowCount.cumsum()
        print 'Row Count', indicesRowCount[:20]
        print 'Row Index Low', indicesRow[:20]
        #print 'Row Index Hig', indicesRowHigh[:20]


        self.indices = zeros((comIdUnique.shape[0], 4), dtype=int)

        print self.indices.shape
        print idCols.shape
        print indicesRow.shape
        print binsIndices.shape

        self.indices[:,0] = comIdUnique/100
        self.indices[:,1] = comIdUnique - self.indices[:,0]*100

        self.indices[1:,2] = indicesRow[:-1]
        self.indices[:,3] = indicesRow
        
        print self.indices[:20, :]
        print self.indices[-20:, :]
        
    def create_col_numbers(self, colNamesDict):
        self.schidCol = colNamesDict[self.activityAttribs.scheduleidName]
        self.actTypeCol = colNamesDict[self.activityAttribs.activitytypeName]
        self.locidCol = colNamesDict[self.activityAttribs.locationidName]
        self.sttimeCol = colNamesDict[self.activityAttribs.starttimeName]
        self.endtimeCol = colNamesDict[self.activityAttribs.endtimeName]
        self.durCol = colNamesDict[self.activityAttribs.durationName]
	self.depPersonCol = colNamesDict[self.activityAttribs.dependentPersonName]

	self.actualArrivalCol = colNamesDict[self.arrivalInfoAttribs.actualArrivalName]
	self.expectedArrivalCol = colNamesDict[self.arrivalInfoAttribs.expectedArrivalName]

    def return_arrival_info(self, schedulesForPerson):
	actualArrival = schedulesForPerson.data[0,self.actualArrivalCol]
	expectedArrival = schedulesForPerson.data[0,self.expectedArrivalCol]
	
	print 'Actual Arrival - %s and Expected Arrival - %s ' %(actualArrival, expectedArrival)
	return actualArrival, expectedArrival


    def resolve_consistency(self, data, seed):
	actList = []
        data.sort([self.activityAttribs.hidName,
                   self.activityAttribs.pidName,
                   self.activityAttribs.scheduleidName])
        ti = time.time()
        # Create Index Matrix
        self.create_indices(data)
	self.create_col_numbers(data._colnames)

        print 'Indices created in %.4f' %(time.time()-ti)

        row = 0
        
        for perIndex in self.indices:
            schedulesForPerson = DataArray(data.data[perIndex[2]:perIndex[3],:], data.varnames)
            #print schedulesForPerson.data.astype(int)
            #raw_input()

            activityList = []
            for sched in schedulesForPerson.data:
                scheduleid = sched[self.schidCol]
                activitytype = sched[self.actTypeCol]
                locationid = sched[self.locidCol]
                starttime = sched[self.sttimeCol]
                endtime = sched[self.endtimeCol]
                duration = sched[self.durCol]
		depPers = sched[self.depPersonCol]                
	
                actepisode = ActivityEpisode(scheduleid, activitytype, locationid, 
                                             starttime, endtime, duration, depPers)
                activityList.append(actepisode)

	    
            personObject = Person(perIndex[0], perIndex[1])
            personObject.add_episodes(activityList)
	    actualArrival, expectedArrival = self.return_arrival_info(schedulesForPerson)
	    personObject.add_arrival_status(actualArrival, expectedArrival)
	    print 'person indices', perIndex
	    print 'Activity list before adjustment'
	    
	    oriList = activityList
	    oriList = personObject.sort_acts(oriList)

	    for x in oriList:
		print '\t', x
            personObject.adjust_schedules_given_arrival_info(seed)
	    reconciledSchedules = personObject._collate_results_aslist()

	    print 'Activity list after adjustment'
	    #modList = personObject.listOfActivityEpisodes
	    #modList = personObject.sort_acts(modList)

	    for x in reconciledSchedules:
		print '\t', x


	    if not personObject._check_for_conflicts():
                raise Exception, "THE SCHEDULES ARE STILL MESSED UP"    
            #reconciledSchedules = personObject.add_and_reconcile_episodes(activityList)
	    #raw_input('Person schedules processed')             
	    actList += reconciledSchedules

        return DataArray(actList, self.colNames)
                
        #return data

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
        
