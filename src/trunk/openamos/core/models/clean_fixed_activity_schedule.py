from openamos.core.agents.person import Person
from openamos.core.agents.household import Household
from openamos.core.agents.activity import ActivityEpisode
from openamos.core.models.abstract_model import Model

from numpy import array, logical_and, histogram, zeros

class CleanFixedActivitySchedule(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification
        self.activityAttribs = self.specification.activityAttribs
        self.dailyStatusAttribs = self.specification.dailyStatusAttribs
        self.dependencyAttribs = self.specification.dependencyAttribs
        self.colNames = [self.activityAttribs.hidName,
                         self.activityAttribs.pidName,
                         self.activityAttribs.scheduleidName, 
                         self.activityAttribs.activitytypeName,
                         self.activityAttribs.starttimeName,
                         self.activityAttribs.endtimeName,
                         self.activityAttribs.locationidName,
                         self.activityAttribs.durationName,
                         self.activityAttribs.dependentPersonName]
        





    def create_col_numbers(self, colnamesDict):
        print colnamesDict
        self.schidCol = colnamesDict[self.activityAttribs.scheduleidName]
        self.actTypeCol = colnamesDict[self.activityAttribs.activitytypeName]
        self.locidCol = colnamesDict[self.activityAttribs.locationidName]
        self.sttimeCol = colnamesDict[self.activityAttribs.starttimeName]
        self.endtimeCol = colnamesDict[self.activityAttribs.endtimeName]
        self.durCol = colnamesDict[self.activityAttribs.durationName]
        self.depPersonCol = colnamesDict[self.activityAttribs.dependentPersonName]

        self.schoolStatusCol = colnamesDict[self.dailyStatusAttribs.schoolStatusName]
        self.workStatusCol = colnamesDict[self.dailyStatusAttribs.workStatusName]

        self.childDependencyCol = colnamesDict[self.dependencyAttribs.childDependencyName]


        


    def create_indices1(self, data):
        houseIdsUnique, hId_reverse_indices = unique(data.columns([self.activityAttribs.hidName]).data,
                                                 return_inverse=True)


        countOfHid = 0

        hhldIndicesOfPersons = []
        personIndicesOfActs = []
        self.actIndex = 0
        self.persIndex = 0
        for hid in houseIdsUnique:
            hIdIndices = hId_reverse_indices == countOfHid
            #hIdIndices.shape = (hIdIndices.sum(), )
            schedulesForHid = data.rowsof(hIdIndices)
            #print 'houseID, number of household records - ',hid, hIdIndices.sum(), schedulesForHid.rows
            #print schedulesForHid.data.astype(int)
            
            pIdsUnique, pId_reverse_indices = unique(schedulesForHid.columns([self.activityAttribs.pidName]).data,
                                                  return_inverse=True)
            #print '\tperson Ids - ', pIdsUnique
            countOfPid = 0
            for pid in pIdsUnique:
                pIdIndices = pId_reverse_indices == countOfPid
                #print ('\tperson id', pid, ' number of person records-', pIdIndices.sum(), 
                #       ' start-', self.actIndex, ' end-', (self.actIndex + pIdIndices.sum()))
                #print data.data[self.actIndex:(self.actIndex + pIdIndices.sum()), :].astype(int)
                
                personIndicesOfActs.append([hid, pid, self.actIndex, self.actIndex + pIdIndices.sum()])

                self.actIndex += pIdIndices.sum()
                countOfPid += 1

            hhldIndicesOfPersons.append([hid, self.persIndex, self.persIndex + pIdsUnique.shape[0]])
            #print 'HID - %s, pers index start - %s, pers index end - %s ' %(hid, self.persIndex,
            #                                                                self.persIndex + pIdsUnique.shape[0])
            self.persIndex += pIdsUnique.shape[0]
            countOfHid += 1

        self.personIndicesOfActs = array(personIndicesOfActs, dtype=int)
        self.hhldIndicesOfPersons = array(hhldIndicesOfPersons, dtype=int)
                   

        #print self.personIndicesOfActs
        #print self.hhldIndicesOfPersons

        #raw_input()

    def create_indices(self, data):
        idCols = data.columns([self.activityAttribs.hidName,
                               self.activityAttribs.pidName]).data
        combId = idCols[:,0]*100 + idCols[:,1]
        comIdUnique, comId_reverse_indices = unique(combId, return_inverse=True)

        binsIndices = array(range(comId_reverse_indices.max()+2))
        histIndices = histogram(comId_reverse_indices, bins=binsIndices)

        indicesRowCount = histIndices[0]
        indicesRow = indicesRowCount.cumsum()


        self.personIndicesOfActs = zeros((comIdUnique.shape[0], 4), dtype=int)

        self.personIndicesOfActs[:,0] = comIdUnique/100
        self.personIndicesOfActs[:,1] = comIdUnique - self.personIndicesOfActs[:,0]*100
        self.personIndicesOfActs[1:,2] = indicesRow[:-1]
        self.personIndicesOfActs[:,3] = indicesRow

        print self.personIndicesOfActs[:20, :]
        print self.personIndicesOfActs[-20:, :]



        hid = self.personIndicesOfActs[:,0]
        
        hidUnique, hid_reverse_indices = unique(hid, return_inverse=True)

        binsHidIndices = array(range(hid_reverse_indices.max()+2))
        histHidIndices = histogram(hid_reverse_indices, bins=binsHidIndices)
        
        indicesHidRowCount = histHidIndices[0]
        indicesHidRow = indicesHidRowCount.cumsum()

        self.hhldIndicesOfPersons = zeros((hidUnique.shape[0], 3))

        self.hhldIndicesOfPersons[:,0] = hidUnique
        self.hhldIndicesOfPersons[1:,1] = indicesHidRow[:-1]
        self.hhldIndicesOfPersons[:,2] = indicesHidRow

        print idCols[:30,:]
        print self.hhldIndicesOfPersons[:20,:]
        print self.personIndicesOfActs[:20,:]

        print idCols[-30:,:]
        print self.hhldIndicesOfPersons[-20:,:]
        print self.personIndicesOfActs[-20:,:]



        raw_input('new implementation of indices')







    def resolve_consistency(self, data, seed):

        actList = []
        data.sort([self.activityAttribs.hidName,
                   self.activityAttribs.pidName,
                   self.activityAttribs.scheduleidName])

        # Create Index Matrix
        self.create_indices(data)
        self.create_col_numbers(data._colnames)

        for hhldIndex in self.hhldIndicesOfPersons:
            firstPersonRec = hhldIndex[1]
            lastPersonRec = hhldIndex[2]

            firstPersonFirstAct = self.personIndicesOfActs[firstPersonRec,2]
            lastPersonLastAct = self.personIndicesOfActs[lastPersonRec-1,3]

            schedulesForHhld = DataArray(data.data[firstPersonFirstAct:
                                                       lastPersonLastAct,:], data.varnames)
            print 'hID - ', hhldIndex[0]
            print schedulesForHhld.data.astype(int)
            print data.varnames

            persIndicesForActsForHhld = self.personIndicesOfActs[firstPersonRec:
                                                                     lastPersonRec,
                                                                 :]




            householdObject = Household(hhldIndex[0])

            for perIndex in persIndicesForActsForHhld:
                personObject = Person(perIndex[0], perIndex[1])
                schedulesForPerson = DataArray(data.data[perIndex[2]:perIndex[3],:], data.varnames)
                activityList = self.return_activity_list_for_person(schedulesForPerson)
                personObject.add_episodes(activityList)
                workStatus, schoolStatus, childDependency = self.return_status_dependency(schedulesForPerson)
                personObject.add_status_dependency(workStatus, schoolStatus, 
                                                   childDependency)

                householdObject.add_person(personObject)

                print '\thID - %s, pID - %s' %(perIndex[0], perIndex[1])
                print schedulesForPerson.data.astype(int)

            reconciledSchedules = householdObject.clean_schedules(seed)
            print reconciledSchedules
            
            actList += reconciledSchedules

            
            #raw_input()

            # TODO: CHECK THE DATA UPDATING PART
            #i = 0
            #for colN in colNames:
            #    data.setcolumn(colN, reconciledSchedules[:,i], start=perIndex[2], end=perIndex[3])
            #    i += 1
                
        return DataArray(actList, self.colNames)

    def return_activity_list_for_person(self, schedulesForPerson):
        # Updating activity list
        activityList = []
        for sched in schedulesForPerson.data:
            scheduleid = sched[self.schidCol]
            activitytype = sched[self.actTypeCol]
            locationid = sched[self.locidCol]
            starttime = sched[self.sttimeCol]
            endtime = sched[self.endtimeCol]
            duration = sched[self.durCol]
            depPersonId = sched[self.depPersonCol]

            actepisode = ActivityEpisode(scheduleid, activitytype, locationid, 
                                         starttime, endtime, duration, depPersonId)
            activityList.append(actepisode)

        

        return activityList

    def return_status_dependency(self, schedulesForPerson):
        workStatus = schedulesForPerson.data[0,self.workStatusCol]
        schoolStatus = schedulesForPerson.data[0,self.schoolStatusCol]
        childDependency = schedulesForPerson.data[0,self.childDependencyCol]

        #print 'wrkcol - %s, schcol - %s, depcol - %s' %(self.workStatusCol, 
        #                                                self.schoolStatusCol,
        #                                                self.childDependencyCol)
        #print 'wrkst - %s, schst - %s, dep - %s' %(workStatus, schoolStatus, 
        #                                           childDependency)
        
        # Checking for status and dependency
        # whether the merge happened correctly
        # this can be replaced with a simple extraction as opposed 
        # to identifying unique values, checking for single value 
        # and then updating the status variables
        workStatusUnique = unique(schedulesForPerson.data[:, self.workStatusCol])
        if workStatusUnique.shape[0] > 1:
            print 'Work Status', workStatusUnique
        
            raise Exception, "More than one values for status/dependency"
        else:
            workStatus = workStatusUnique[0]
        
        schoolStatusUnique = unique(schedulesForPerson.data[:, self.schoolStatusCol])
        if schoolStatusUnique.shape[0] > 1:
            print 'School Status', schoolStatusUnique
            raise Exception, "More than one values for status/dependency"
        else:
            schoolStatus = schoolStatusUnique[0]

        childDependencyUnique = unique(schedulesForPerson.data[:, self.childDependencyCol])
        if childDependencyUnique.shape[0] > 1:
            print 'Child Dependency', childDependencyUnique
            raise Exception, "More than one values for status/dependency"
        else:
            childDependency = childDependencyUnique[0]
        
        #print 'wrkst - %s, schst - %s, dep - %s' %(workStatus, schoolStatus, 
        #                                           childDependency)
        return workStatus, schoolStatus, childDependency

        




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
        
