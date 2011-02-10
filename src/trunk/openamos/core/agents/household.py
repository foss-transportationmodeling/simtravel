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
        self.indepPersonIds = []

    def add_person(self, person):
        # person is an object of the Person class
        self.persons[person.pid] = person

        if person.child_dependency == 1:
            self.dependencyPersonIds.append(person.pid)
        elif person.workstatus == 1 or person.schoolstatus == 1:
            self.dailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)
        else:
            self.noDailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)


        
        
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


                print '\n\t\t1.1. End of Day/Start of Day: Someone needs to be there'
                self.adjust_terminal_activity_episodes(pid, stAct, start=True)
                #raw_input()

                print '\n\t\t1.2. End of Day/Start of Day: Someone needs to be there'
                endAct = person.lastEpisode
                self.adjust_terminal_activity_episodes(pid, endAct, start=False)                    




                while (len(actsOfDepPerson) > 0):
                    endActStartTime, endAct = hp.heappop(actsOfDepPerson)
                    #hp.heappop(person.listOfActivityEpisodes)

                    if endAct.actType > 100 and endAct.actType < 200:
                        print '\n\t\t2.1. IH Act: Someone needs to be there'
                        print '\t\t\t', endAct
                        self.allocate_ih_activity(pid, endAct)


                    if (endAct.location <> stAct.location) and (endAct.actType >= 400 and endAct.actType < 500):
                        print '\n\t\t2.2. OH Act: Pick-up/Drop-off and also allocate activity to adult if maintenance'
                        print '\t\t\t START-', stAct
                        print '\t\t\t END-  ', endAct
                        self.allocate_pickup_dropoff_endact(pid, stAct, endAct)


                    if (endAct.location <> stAct.location)  and (endAct.actType < 400 or endAct.actType >= 500):
                        print '\n\t\t2.3. OH Act: Terminal activity is a maintenance activity and needs to be allocated'
                        print '\t\t\t Terminal Activity-', endAct
                        self.allocate_pickup_dropoff(pid, stAct, endAct)


                    stAct = endAct

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
                check = person.check_start_of_day(actOfdepPerson.endTime)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime)

            if check:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]


            if start:
                check = person.check_start_of_day(actOfdepPerson.endTime)
            else:
                check = person.check_end_of_day(actOfdepPerson.startTime)

            if check:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
                return True


        print """\t\t\t --- > Exception: No person identified that can be with the """\
            """dependent child for the terminal episodes in a day"""\

        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities and  then adjust their terminal 
        # episode durations so that children are not abandoned


        if start:
            terminalAct = depPerson.firstEpisode
        else:
            terminalAct = depPerson.lastEpisode


        pid = self.personId_with_terminal_episode_overlap([terminalAct], 
                                                          self.indepPersonIds)

        #pid = self.personId_with_least_conflict([terminalAct], 
        #                                        self.indepPersonIds)
        if pid is None:
            raise Exception, "--There are no independent adults in the household--"


        print "\t\t\t\t--Randomly independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #actOfPerson = self.find_terminal_vertex(person, start)

        if start:
            person.move_start_of_day(actOfdepPerson.endTime)
        else:
            person.move_end_of_day(actOfdepPerson.startTime)

        person._check_for_conflicts()

        self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
        return True


    def update_depPersonId_for_terminal_episode(self, start, depPersonId, pid):
        depPerson = self.persons[depPersonId]
        if start:
            depPerson.firstEpisode.dependentPersonId = pid
        else:
            depPerson.lastEpisode.dependentPersonId = pid            

        
            


    def allocate_ih_activity(self, depPersonId, act):
        # Changing the activitytype to +50 to assign that as a dependent
        # activity
        act = copy.deepcopy(act)
        act.actType += 50
        act.dependentPersonId = 99
        
        # If there are people already home then that 
        # person is allocated this particular activity
        
        self.rndGen.shuffle_sequence(self.indepPersonIds)

        for pid in self.indepPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)

            if person._check_for_ih_conflicts(act):
                print '\t\t\t\tPerson - %s is already home so he is allocated this activity' %(pid)
                self.update_depPersonId(act, depPersonId, pid)
                person.remove_episodes([act])
                return True
            else:
                person.remove_episodes([act])                
                













        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)
            
            if not person._check_for_conflicts():
                person.remove_episodes([act])
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId(act, depPersonId, pid)
                return True
                
        # Person with fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1            
            person.add_episodes([act], temp=True)

            if not person._check_for_conflicts():
                person.remove_episodes([act])
            else:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.update_depPersonId(act, depPersonId, pid)
                return True

        print " \t\t\t--- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, [act], 
                                                self.indepPersonIds)



        if pid is None:
            print "Exception, --There are no independent adults in the household--"
            #raw_input()
            return
        else:
            print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)
            person._check_for_conflicts()            

            self.update_depPersonId(act, depPersonId, pid)


        #person.adjust_activity_schedules(self.seed)
            return True        

    def update_depPersonId(self, activity, depPersonId, pid):
        depPerson = self.persons[depPersonId]

        for actStart, act in depPerson.listOfActivityEpisodes:
            if act.startTime == activity.startTime:
                break

        #indAct = depPerson.listOfActivityEpisodes.index((activity.startTime, activity))
        #act = depPerson.listOfActivities[indAct]
        
        print 'BEFORE ASSIGN', act
        act.dependentPersonId = pid

        print 'AFTER ASSIGN', act
        #print pid
        #raw_input('FOUND THE INDEX')


    """

    def allocate_activity(self, depPersonId, act):
        # Changing the activitytype to +50 to assign that as a dependent
        # activity
        act.actType += 50

        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)
            
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
            person.add_episodes([act], temp=True)

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


        pid = self.personId_with_least_conflict(depPersonId, [act], 
                                                self.indepPersonIds)



        if pid is None:
            print "Exception, --There are no independent adults in the household--"
            #raw_input()
            return
        else:
            print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid
            
            act.dependentPersonId = depPersonId
            act.scheduleId = self.persons[pid].actCount + 1
            person = self.persons[pid]
            person.add_episodes([act])
            person._check_for_conflicts()            
        #person.adjust_activity_schedules(self.seed)
            return True


    """

    def allocate_pickup_dropoff(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)

        dummyActPickUp.dependentPersonId = 99
        dummyActDropOff.dependentPersonId = 99

        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)           

            if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff])           
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True
                
        # Person with fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2     

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)

            if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff])
            else:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True

        print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, 
                                                [dummyActPickUp, dummyActDropOff], 
                                                self.indepPersonIds)

        if pid is None:
            print "Exception, --There are no independent adults in the household--"
            #raw_input()
            return

        print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2

        person.add_episodes([dummyActPickUp, dummyActDropOff])

        person._check_for_conflicts()

        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
        #person.adjust_activity_schedules(self.seed)
        return True


    def allocate_pickup_dropoff_endact(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:
        endActToNonDependent = copy.deepcopy(endAct)
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)

        dummyActPickUp.dependentPersonId = 99
        dummyActDropOff.dependentPersonId = 99
        endActToNonDependent.dependentPersonId = 99
        endActToNonDependent.actType += 50



        # Person without fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2
            endActToNonDependent.scheduleId = person.actCount + 3
            #print dummyActPickUp
            #print dummyActDropOff
            person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent], temp=True)           
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])           
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                endAct.dependentPersonId = pid
                return True
                
        # Person with fixed activities
        print '\t\t\tFollowing person without fixed activities is identified - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2     
            endActToNonDependent.scheduleId = person.actCount + 3       
            #print dummyActPickUp
            #print dummyActDropOff
            person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent], temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            if not person._check_for_conflicts():
                

                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            else:
                print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                endAct.dependentPersonId = pid
                return True

        print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, 
                                                [dummyActPickUp, dummyActDropOff], 
                                                self.indepPersonIds)

        if pid is None:
            print "Exception, --There are no independent adults in the household--"
            #raw_input()
            return

        print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #self.print_activity_list(person)        
        #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2
        endActToNonDependent.scheduleId = person.actCount + 3       
        #print dummyActPickUp
        #print dummyActDropOff
        person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
        #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
        #self.print_activity_list(person)
        person._check_for_conflicts()

        #dummyActPickUp = copy.deepcopy(dummyActPickUp)
        #dummyActDropOff = copy.deepcopy(dummyActDropOff)

        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
        endAct.dependentPersonId = pid
        #person.adjust_activity_schedules(self.seed)
        return True
            

    def add_activity_update_depPersonId(self, activityList, depPersonId, pid):
        depPerson = self.persons[depPersonId]

        activityList = copy.deepcopy(activityList)

        for i in range(len(activityList)):
            act = activityList[i]
            act.scheduleId = depPerson.actCount + i + 1
            act.dependentPersonId = pid

        depPerson.add_episodes(activityList)
        depPerson._check_for_conflicts()
        




    def randPersonId(self, personIdList):
        lengthOfList = len(personIdList)
        randNum = self.rndGen.return_random_integers(0, lengthOfList - 1)
        pid = personIdList[randNum]
        return pid



    def personId_with_least_conflict(self, depPersonId, activityList, personIdList):
        personConflict = {}
        personConflictActs = {}
        for pid in personIdList:
            person = self.persons[pid]            
            
            person.add_episodes(activityList, temp=True)
            conflict = person._conflict_duration()
            person.remove_episodes(activityList)

            conflictActs = person._identify_conflict_activities(activityList)

            checkForDependencies = self._check_for_dependencies_for_conflictActivities(depPersonId,
                                                                                       conflictActs)
            
            if not checkForDependencies:
                continue

            personConflict[pid] = conflict
            personConflictActs[pid] = conflictActs

        print personConflict
        print personConflictActs

            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid, conflict)
        if len(personConflict) > 0:
            leastConflict = min(personConflict.values())
        else:
            return

        for pid in personConflict.keys():
            print '\t\t\t\t\tperson - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:
                return pid



    def _check_for_dependencies_for_conflictActivities(self, depPersonId, conflictActs):
        print '\t\t\t\tCHECKING FOR DEPENDENCIES for dep act of person - ', depPersonId

        for act in conflictActs:
            print '\t\t\t\t\t', act
            if (act.dependentPersonId > 0 and act.dependentPersonId <> depPersonId):
                return False
        return True


    def personId_with_terminal_episode_overlap(self, activityList, personIdList):
        print activityList
        personConflict = {}

        for pid in personIdList:
            person = self.persons[pid]

            person.add_episodes(activityList, temp=True)
            conflictWithTerminalEpisode = person._conflict_duration_with_activity(person.lastEpisode)
            conflict = person._conflict_duration()
            
            personConflict[pid] = conflict - conflictWithTerminalEpisode
            person.remove_episodes(activityList)

            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid, 
            #                                                                                  (conflict - 
            #                                                                                   conflictWithTerminalEpisode))
            #print '\t\t\t\t\tConflict - %s and conflict with last episode - %s' %(conflict,
            #                                                                      conflictWithTerminalEpisode)

            leastConflict = min(personConflict.values())

        for pid in personConflict.keys():
            print 'person - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:
                print '\t\t\t\tPerson with least conflict with terminal episode is', pid
                return pid
                
                
            
            
            


            

            
    def create_dummy_activity(self, depPersonId, stAct, endAct):
        dummyPickUpAct = copy.deepcopy(stAct)
        dummyDropOffAct = copy.deepcopy(endAct)



        dummyPickUpAct.startTime = dummyPickUpAct.endTime + 1
        dummyPickUpAct.endTime = dummyPickUpAct.startTime + 1
        dummyPickUpAct.duration = 1
        dummyPickUpAct.actType = 600
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False
        dummyPickUpAct.dependentPersonId = 0


        
        dummyDropOffAct.startTime = dummyDropOffAct.startTime - 1 -1
        dummyDropOffAct.endTime = dummyDropOffAct.startTime + 1
        dummyDropOffAct.duration = 1
        dummyDropOffAct.actType = 601
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False
        dummyPickUpAct.dependentPersonId = 0


        print '\n\t\t\tPICKUP ACTIVITY - ', dummyPickUpAct

        print '\t\t\tDropOff ACTIVITY -', dummyDropOffAct


        return dummyPickUpAct, dummyDropOffAct


        










