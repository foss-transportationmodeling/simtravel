import copy
import heapq as hp
from numpy import array

from openamos.core.models.abstract_random_distribution_model import RandomDistribution

class Household(object):
    def __init__(self, hid):
        self.hid = hid
        self.persons = {}
        self.dependencyPersonIds = []
        self.dailyFixedActPersonIds = []
        self.noDailyFixedActPersonIds = []
        

    def add_person(self, person):
        # person is an object of the Person class
        self.persons[person.pid] = person

        if person.child_dependency == 1:
            self.dependencyPersonIds.append(person.pid)
        elif person.workstatus == 1 or person.schoolstatus == 1:
            self.dailyFixedActPersonIds.append(person.pid)
        else:
            self.noDailyFixedActPersonIds.append(person.pid)

        
    def _collate_results(self):
        resList = []
        for pid in self.persons:
            person = self.persons[pid]
            
            for actStart, act in person.listOfActivityEpisodes:
                resList.append([self.hid, pid, act.scheduleId,
                                act.actType, act.startTime, act.endTime,
                                act.location, act.duration, act.dependentPersonId])
        return resList

        
    def _check_for_dependency(self, person):
        if person.child_dependency == 1:
            return True
        else:
            return False

    def _check_for_dailyFixedActStatus(self, person):
        if person.workstatus == 1 or person.schoolstatus == 1:
            return True
        else:
            return False


    def clean_schedules(self, seed):
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds        
        
        self.personIds = self.persons.keys()
        self.personIds.sort()

        # delete fixed work episodes
        for pid in self.personIds:
            person = self.persons[pid]
            if person.workstatus == 0:
                self.remove_work_episodes(person)

        # delete fixed school episodes
        for pid in self.personIds:
            person = self.persons[pid]
            if person.schoolstatus == 0:
                self.remove_school_episodes(person)        

        return self._collate_results()

    def remove_work_episodes(self, person):
        #for wrkEpisode in person.workEpisodes:
        print '\tActually REMOVING WORK ACTIVITY; WORK STATUS FOR DAY IS ZERO for pid - ', person.pid
        print '\t', person.workEpisodes, '-----------------<<<<<<<<<<<<<<<<'
        
        person.remove_episodes(person.workEpisodes)

    def remove_school_episodes(self, person):
        #for schEpisode in person.schoolEpisodes:
        print '\tActually REMOVING SCHOOL ACTIVITY; SCHOOL STATUS FOR DAY IS ZERO for pid - ', person.pid
        print '\t', person.schoolEpisodes, '-----------------<<<<<<<<<<<<<<<<'

        person.remove_episodes(person.schoolEpisodes)

    def allocate_dependent_activities(self, seed):
        self.seed = seed
        self.rndGen = RandomDistribution(int(self.hid + self.seed))


        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds

        if len(self.dependencyPersonIds) > 0:
            print 'DEPENDENCIES EXIST; ACTIVITIES NEED TO BE ALLOCATED TO INDEPENDENT PERSONS'

        # For each person identify an adult that has open 
        # periods and then allocate to him
            for pid in self.dependencyPersonIds:
                person = self.persons[pid]

                actsOfDepPerson = copy.deepcopy(person.listOfActivityEpisodes)


                print 'ALLOCATING ACTIVITIES FOR PERSON ID - ', pid
                self.print_activity_list(person)
                stActStartTime, stAct = hp.heappop(actsOfDepPerson)
                #hp.heappop(person.listOfActivityEpisodes)

                print '\n\t\t1. End of Day/Start of Day: Someone needs to be there'
                self.adjust_terminal_activity_episodes(pid, stAct, start=True)
                #raw_input()

                while (len(actsOfDepPerson) > 0):
                    endActStartTime, endAct = hp.heappop(actsOfDepPerson)
                    #hp.heappop(person.listOfActivityEpisodes)

                    if endAct.actType > 100 and endAct.actType < 200:
                        print '\n\t\t2.1. IH Act: Someone needs to be there'
                        print '\t\t\t', endAct
                        self.allocate_activity(pid, endAct)


                    if endAct.actType >= 200:
                        print '\n\t\t2.2. OH Act: Pick-up/Drop-off'
                        print '\n\t\t\t START-', stAct
                        print '\t\t\t END-  ', endAct
                        self.allocate_pickup_dropoff(pid, stAct, endAct)

                    stAct = endAct

                print '\n\t\t3. End of Day/Start of Day: Someone needs to be there'
                self.adjust_terminal_activity_episodes(pid, stAct, start=False)                    

        return self._collate_results()

    def print_activity_list(self, person):
        print '--> ACTIVITY LIST for person - ', person.hid, person.pid
        for actSt, act in person.listOfActivityEpisodes:
            print '\t\t', act
                    
    def check_for_terminal_vertex(self, actOfPerson, actOfdepPerson, start):
        if start:
            return actOfdepPerson.endTime >= actOfPerson.endTime
        else:
            return actOfdepPerson.startTime <= actOfPerson.startTime


    def _adjust_terminal_vertex(self, actOfPerson, actOfdepPerson, start):
        if start:
            actOfPerson.endTime = actOfdepPerson.endTime - 1
            actOfPerson.duration = actOfPerson.endTime - actOfPerson.startTime
        else:
            actOfPerson.startTime = actOfdepPerson.startTime + 1
            actOfPerson.duration = actOfPerson.endTime - actOfPerson.startTime
        return actOfPerson

    def find_terminal_vertex(self, person, start):
        if start:
            actStartTime, act = hp.heappop(person.listOfActivityEpisodes)
            return act
        else:
            for actStartTime, act in person.listOfActivityEpisodes:
                if act.endOfDay:
                    person.remove_episodes([act])
                    return act


    def adjust_terminal_activity_episodes(self, depPersonId, actOfdepPerson, start=True):
        
        print '\t\t\t\tAdjusting the terminal start-"%s" activity episodes to ensure that the child is taken care of' %(start)
        depPerson = self.persons[depPersonId]
        
        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]

            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                return True

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]


            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime, depPersonId)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime, depPersonId)

            if check:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                return True


        print """ --- > Exception: No person identified that can be with the """\
            """dependent child for the terminal episodes in a day"""\

        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities and  then adjust their terminal 
        # episode durations so that children are not abandoned

        if len(self.noDailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.noDailyFixedActPersonIds)

        elif len(self.dailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.dailyFixedActPersonIds)
        else:
            raise Exception, "\t\t\t\t--There are no independent adults in the household--"

        print "\t\t\t\t--Randomly independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #actOfPerson = self.find_terminal_vertex(person, start)

        if start:
            person.move_start_of_day(actOfdepPerson.endTime, depPersonId)
        else:
            person.move_end_of_day(actOfdepPerson.startTime, depPersonId)

        self.print_activity_list(person)
        return True


    def allocate_activity(self, depPersonId, act):
        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act])
            
            if not person._check_for_conflicts():
                person.remove_episodes([act])
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                return True
                
        # Person with fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1            
            person.add_episodes([act])

            if not person._check_for_conflicts():
                person.remove_episodes([act])
            else:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                return True

        print " \t\t\t--- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        if len(self.noDailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.noDailyFixedActPersonIds)

        elif len(self.dailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.dailyFixedActPersonIds)
        else:
            raise Exception, "\t\t\t--There are no independent adults in the household--"

        print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        act.dependentPersonId = depPersonId
        act.scheduleId = self.persons[pid].actCount + 1
        person = self.persons[pid]
        person.add_episodes([act])
        #person.adjust_activity_schedules(self.seed)
        return True



    def allocate_travel_episode(self, depPersonId, stAct, endAct):
        pass
            


    def allocate_pickup_dropoff(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)
        
        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2
            person.add_episodes([dummyActPickUp,dummyActDropOff])           
 
            if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp,dummyActDropOff])           
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                return True
                
        # Person with fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]

            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2            
            person.add_episodes([dummyActPickUp,dummyActDropOff])

            if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp,dummyActDropOff])
            else:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                return True

        print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities

        if len(self.noDailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.noDailyFixedActPersonIds)

        elif len(self.dailyFixedActPersonIds) > 0:
            pid = self.randPersonId(self.dailyFixedActPersonIds)
        else:
            raise Exception, "--There are no independent adults in the household--"


        print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]

        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2

        person.add_episodes([dummyActPickUp, dummyActDropOff])

        #person.adjust_activity_schedules(self.seed)
        return True
            



    def randPersonId(self, personIdList):
        lengthOfList = len(personIdList)
        randNum = self.rndGen.return_random_integers(0, lengthOfList - 1)
        pid = personIdList[randNum]
        return pid


            
        
    def create_dummy_activity(self, depPersonId, stAct, endAct):
        dummyPickUpAct = copy.deepcopy(stAct)
        dummyDropOffAct = copy.deepcopy(endAct)
        
        dummyPickUpAct.startTime = dummyPickUpAct.endTime
        dummyPickUpAct.endTime = dummyPickUpAct.endTime + 1
        dummyPickUpAct.duration = 1
        dummyPickUpAct.actType = 600
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False
        dummyPickUpAct.dependentPersonId = depPersonId


        
        dummyDropOffAct.startTime = dummyDropOffAct.startTime - 1 -1
        dummyDropOffAct.endTime = dummyDropOffAct.startTime + 1
        dummyDropOffAct.duration = 1
        dummyDropOffAct.actType = 601
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False


        print '\tPICKUP ACTIVITY - ', dummyPickUpAct

        print '\tDropOff ACTIVITY -', dummyDropOffAct


        return dummyPickUpAct, dummyDropOffAct


        
    def _extract_travel_time(self, st_loc, end_loc):
        # Currently assume that the travel time between any two
        # activity episodes that are not same is 30 mins
        # TODO: Needs to be replaced with querying the travel skims

        if st_loc == end_loc:
            tt = 1

        tt = 30
        return tt











