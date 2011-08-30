import copy
import heapq as hp
from numpy import array, zeros

from openamos.core.models.abstract_random_distribution_model import RandomDistribution
from openamos.core.agents.person import Person

class Household(object):
    def __init__(self, hid):
        self.hid = hid
        self.persons = {}
        self.dependencyPersonIds = []
        self.dailyFixedActPersonIds = []
        self.noDailyFixedActPersonIds = []
        self.indepPersonIds = []
	self.numPersons = 0


	# Household attributes for evolution
	self.bldgsz = 0
	self.hht = 0
	self.hinc = 0
	self.noc = 0
	self.personsSize = 0
	self.unittype = 0
	self.vehicl = 0
	self.wif = 0
	self.yrMoved = 0
	self.oldHid = 0


	self.relateDict = {1:'Householder',
			   2:'Husband/Wife',
			   3:'Natural born son/daughter',
			   4:'Adopted son/daughter',
			   5:'Stepson/stepdaughter',
			   6:'Brother/sister',
			   7:'Father/mother',
			   8:'Grandchild',
			   9:'Parent-in-law',
			   10:'Son-in-law/daughter-in-law',
			   11:'Other relative',
			   12:'Brother-in-law/sister-in-law',
			   13:'Nephew/niece',
			   14:'Grandparent',
			   15:'Uncle/aunt',
			   16:'Cousin',
			   17:'Roomer/boarder',
			   18:'Housemate/roommate',
			   19:'Unmarried partner',
			   20:'Foster child',
			   21:'Other nonrelative',
			   22:'Institutionalized GQ person',
			   23:'Noninstitutionalized GQ person'}

	self.hhtDict = {0:"Not in universe (Vacant or GQ)",
			     1:"Family household: Married-couple",
			     2:"Family household: Male householder, no wife present",
			     3:"Family household: Female householder, no husband present",
			     4:"Nonfamily household: Male householder, living alone",
			     5:"Nonfamily household: Male householder, not living alone",
			     6:"Nonfamily household: Female householder, living alone",
			     7:"Nonfamily household: Female householder, not living alone"}

	self.sexDict = {1:'Male', 2:'Female'}

	self.hhldrAlive = True


    def add_person(self, person):
        # person is an object of the Person class
	person.hid = self.hid
        self.persons[person.pid] = person
	self.personsSize += 1
	if person.age < 18:
	    self.noc += 1

        if person.child_dependency == 1:
            self.dependencyPersonIds.append(person.pid)
        elif person.workstatus == 1 or person.schoolstatus == 1:
            self.dailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)
        else:
            self.noDailyFixedActPersonIds.append(person.pid)
            self.indepPersonIds.append(person.pid)

    def remove_person(self, personId):
	person = self.persons.pop(personId)
	self.personsSize -= 1
	if person.age < 18:
	    self.noc -= 1

	return person

    def return_person_list(self):
	personList = []
	for personId in self.persons.keys():
	    person = self.persons[personId]
	    personList.append([person.hid,
			       person.pid,
				person.age_f,
				person.clwkr,
				person.educ_f,
				person.enrollment_f,
				person.esr,
				person.indnaics,
				person.occupation_f,
				person.race1,
				person.relate,
				person.sex,
				person.marstat,
				person.hours,
				person.grade_f,	
				person.hispan,
			        self.oldHid])

        return personList

	    



    def set_household_attributes(self, bldgsz, hht, hinc, noc,
				 persons, unittype, vehicl, wif,
				 yrMoved):
	self.bldgsz = bldgsz
	self.hht = hht
	self.hinc = hinc
	#self.noc = noc (No need to assign these; they are updated as person objects are added)
	#self.persons = persons (No need to assign these; they are updated as person objects are added)
	self.unittype = unittype
	self.vehicl = vehicl
	self.wif = wif
	self.yrMoved = yrMoved

    def print_person_relationship_gender(self):
	personIds = copy.deepcopy(self.persons.keys())
	print '\n    Household Id - ', self.hid
	for personId in personIds:
	    person = self.persons[personId]
	    print """\t    Relationship of person - %s, """\
			"""relationship - %s and gender - %s' """%(person.pid, 
								   self.relateDict[person.relate], 
								   self.sexDict[person.sex])
	

    def evolve_population(self, seed, highestHid):
	# All data dictionaries are borrowed directly from PUMS 2000
	# Once a full implementation is complete we can extend the code
	# to generalize the data dictionaries
	
        self.rndGen = RandomDistribution(int(self.hid + seed))
	self.highestHid = highestHid


	# Printing relationship for current residents of the household
	print 'HOUSEHOLD ID - %s' %self.hid
        print '\tHousehold type - ', self.hhtDict[self.hht]
	personIds = copy.deepcopy(self.persons.keys())
	for personId in personIds:
	    person = self.persons[personId]
	    print '\t    Relationship of all people - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])

	# Processing birth
	birthFlag = False
	personIds = copy.deepcopy(self.persons.keys())
	for personId in personIds:
	    person = self.persons[personId]
	    	
	    if person.birth_f == 1:
		self.process_birth()
		birthFlag = True
	if birthFlag:
	    print '1. After birth processing'
	    self.print_person_relationship_gender()
	    #raw_input("press any key to continue...")

	# Processing mortality
	mortalityFlag = False
	personIds = copy.deepcopy(self.persons.keys())
	for personId in personIds:
	    person = self.persons[personId]
	    #print '\tRelationship of all people - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])
	    if person.mortality_f == 1:
		self.process_mortality(personId)
		mortalityFlag = True
		if person.relate == 1:
		    self.hhldrAlive = False

	if mortalityFlag:
	    print '2. After Mortality Processing'
	    self.print_person_relationship_gender()		
	    #raw_input("press any key to continue...")


	# Processing divorce
	divorceFlag = False
	personIds = copy.deepcopy(self.persons.keys())
	for personId in personIds:
	    person = self.persons[personId]
	    if person.divorceDecision_f == 1:
		partnerHousehold = self.process_divorce()
		divorceFlag = True
		break
	
	if divorceFlag:
	    print '3. After divorce processing'
	    self.print_person_relationship_gender()
	    if partnerHousehold is not None:
		partnerHousehold.print_person_relationship_gender()
	    #raw_input("press any key to continue...")
	else:
	    partnerHousehold = None
	self.process_household_type()	


	#TODO:update the household type for this household and partner's household
	#TODO:update the household income for this household and partner's household
	#TODO:update the unit type for this household and partner's household
	#TODO:update the vehicle count for this household and partner's household
	#TODO:update the number of workers for this household and partner's household
	#TODO:update the vehicle count for this household and partner's household
	#TODO:update the yrmoved for this household and partner's household


	#TODO:update PERSON ATTRIBUTES


	return partnerHousehold, self.highestHid
	
    def process_birth(self):
	print '\n--1. Person born--'
	maxPid = max(self.persons.keys())
	personNew = Person(self.hid, maxPid + 1)

	sexRndNum = self.rndGen.return_uniform()
	if sexRndNum<= 0.5:
	    sex = 1
	else:
	    sex = 2

	personNew.sex = sex
	personNew.relate = 3

	hhldrId = False
	partnerId = False
	for personId in self.persons.keys():
	    person = self.persons[personId]
	    if person.relate == 1:
		hhldrId = personId
	    elif person.relate == 2:
		partnerId = personId

	if hhldrId <> False and partnerId <> False:
	    hhldr = self.persons[hhldrId]
	    partner = self.persons[partnerId]

	    if hhldr.race1 == partner.race1:
		personNew.race1 = hhldr.race1

	    if hhldr.race1 <> partner.race1:
		personNew.race1 = 9
	    
	    print 'Hhldr race - %s and partner race - %s and new Kids race - %s' %(hhldr.race1, partner.race1, personNew.race1)

	if hhldrId <> False and partnerId == False:
	    hhldr = self.persons[hhldrId]
	    personNew.race1 = hhldr.race1

	    print 'Hhldr race - %s and partner race - %s and new Kids race - %s' %(hhldr.race1, None, personNew.race1)

	#raw_input()	



	self.add_person(personNew)


    def process_mortality(self, personId):
	# Remove person record
	print '\n--2. Person expired need to remove record and update household attributes--'

	print '\tPerson ids list', self.persons.keys()
	#person = self.persons.pop(personId)
	person = self.persons[personId]
	
	# Update marriage status for the partner
	if person.marstat == 1:
	    hhldrId, partnerId = self.identify_hhldr_partner_id()
	    if hhldrId == personId and partnerId <> False:
		partner = self.persons[partnerId]
		partner.marstat = 2

	    if hhldrId <> False and partnerId == personId:
		hhldr = self.persons[partnerId]
		hhldr.marstat = 2
		
	self.remove_person(personId)

	print '\tNew Person ids list', self.persons.keys()
	print


    def process_divorce(self):
	print '\n--k. Divorce occurred need to dissolve the household--'
	
	if self.hht >=4 and self.hht <=7:
	    self.print_person_relationship_gender()
	    print ('Non family household seeking divorce')	
	partnerHousehold = None


	hhldrId, partnerId = self.identify_hhldr_partner_id()


	if hhldrId <> False:
	    hhldr = self.persons[hhldrId]
	    hhldr.marstat = 3			# changing the marriage status of the hhldr
		
	if partnerId <> False:
	    partner = self.persons[partnerId]
	    partner.marstat = 3				# changing the marriage status of the partner

	if hhldrId == False or partnerId == False:
	    print '\tOne or more partners was not identified husbandPid - %s and wifePid - %s' %(hhldrId, partnerId)
	    #raw_input("\tNo need to dissolve the household one or both are missing from the household due to passign away")

	if hhldrId and partnerId:
	    print '\tBoth partners were identified husbandPid - %s and wifePid - %s' %(hhldrId, partnerId)


	    self.highestHid += 1
	    partnerHousehold = Household(self.highestHid)

	    print '\t    a. Allocate the partner'
	    #partner = self.persons.pop(partnerId)
	    partner = self.remove_person(partnerId)
	    partnerHousehold.add_person(partner)

	    print '\tMembers in the household other than the householder and partner- '
		
	    ownKidIds = []
	    partnersKidIds = []
	    ownParentIds = []
	    partnersParentIds = []		
	    otherIds = []

	    personIds = copy.deepcopy(self.persons.keys())
	    for personId in personIds:
	    	person = self.persons[personId]

	    	print '\t    Relationship of surviving - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])
		if person.relate == 3 or person.relate == 4:
		    ownKidIds.append(personId)
		elif person.relate == 5:
		    partnersKidIds.append(personId)
		elif person.relate == 7:
		    ownParentIds.append(personId)
		elif person.relate == 9:
		    partnersParentIds.append(personId)
		elif person.relate <> 1 and person.relate <> 2:
		    otherIds.append(personId)

	    print '\t    b. Own Kids - ', ownKidIds
	    print '\t\t Allocating Own Kids'
	    ownKidsRndNum = self.rndGen.return_uniform()
	    if ownKidsRndNum <= 0.5:
		for ownKidId in ownKidIds:
		    #ownKid = self.persons.pop(ownKidId)
		    ownKid = self.remove_person(ownKidId)
		    partnerHousehold.add_person(ownKid)

	    print '\t    c. Partners Kids - ', partnersKidIds
	    print '\t\t Allocating partner kids'
	    for partnersKidId in partnersKidIds:
		#partnersKid = self.persons.pop(partnersKidId)
		partnersKid = self.remove_person(partnersKidId)
		partnerHousehold.add_person(partnersKid)

	    print '\t    d. Own parents - ', ownParentIds

	    print '\t    e. Partners parents - ', partnersParentIds
	    print '\t\t Allocating partner parents'
	    for partnersParentId in partnersParentIds:
		#partnersParent = self.persons.pop(partnersParentId)
		partnersParent = self.remove_person(partnersParentId)
		partnerHousehold.add_person(partnersParent)

	    print '\t    f. Other - ', otherIds
	    print '\t\t Allocating others'
	    for otherId in otherIds:
		otherRndNum = self.rndGen.return_uniform()
		if otherRndNum <= 0.5:
		    #other = self.persons.pop(otherId)
		    other = self.remove_person(otherId)
		    partnerHousehold.add_person(other)

	    partnerHousehold.oldHid = self.hid
	    #raw_input("\tWe need to dissolve the household")	
	
	return partnerHousehold


    def identify_hhldr_partner_id(self, hid=None):
	hhldrId = False
	partnerId = False
	if hid is None:
	    personsDict = self.persons
	else:
	    personsDict = hid.persons

	personIds = copy.deepcopy(personsDict.keys())
	for personId in personIds:
	    person = personsDict[personId]
	    # Male householder
	    if person.relate == 1 and person.sex == 1:
		print '\tIdentified the male householder in the marriage - ', personId
		hhldrId = personId
	    # female non-householder
	    if person.relate == 2 and person.sex == 2:
		print '\tIdentified the female non-householder in the marriage - ', personId		
		partnerId = personId
	    # female householder
	    if person.relate == 1 and person.sex == 2:
		print '\tIdentified the female householder in the marriage - ', personId
		hhldrId = personId
	    # male non-householder
	    if person.relate == 2 and person.sex == 1:
		print '\tIdentified the male non-householder in the marriage - ', personId		
		partnerId = personId
	return hhldrId, partnerId

    def process_household_type(self):
	print '\n--k+1. Process the household type --'
	print '\tHouseholder alive flag - %s' %self.hhldrAlive
	personIds = copy.deepcopy(self.persons.keys())
	for personId in personIds:
	    person = self.persons[personId]
	    print '\t    Relationship of surviving - %s and gender - %s' %(self.relateDict[person.relate], self.sexDict[person.sex])

	    if self.hhldrAlive:
		# Householder alive
		if self.hht >= 1 and self.hht <= 3:
		    if self.persons == 1:
			pass
		    

	    else:
		# Householder not alive
		pass
       
    def _collate_results(self):
        resList = []
        for pid in self.persons:
            person = self.persons[pid]

                
            for actStart, act in person.listOfActivityEpisodes:
                resList.append([self.hid, pid, act.scheduleId,
                                act.actType, act.startTime, act.endTime,
                                act.location, act.duration, act.dependentPersonId])
        return resList

    def _collate_results_without_dependentActs(self):
        resList = []
        for pid in self.dependencyPersonIds:
            person = self.persons[pid]
            for actStart, act in person.listOfActivityEpisodes:
		if act.dependentPersonId == 0:
                    resList.append([self.hid, pid, act.scheduleId,
                                   act.actType, act.startTime, act.endTime,
                                   act.location, act.duration, act.dependentPersonId])

        for pid in self.indepPersonIds:
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

	
    def clean_schedules_for_in_home_episodes(self, seed):
        self.personIds = self.persons.keys()
        self.personIds.sort()

	for pid in self.personIds:
	    person = self.persons[pid]
	    person.clean_schedules_for_in_home_episodes()

            if not person._check_for_conflicts():
                self.print_activity_list(person)
                print 'Exception', 'The person still has conflicts - %s, %s' %(self.hid, pid)
                raw_input()


	return self._collate_results()


    def clean_schedules(self, seed):
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        #print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds        
        
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
        #print '\tActually REMOVING WORK ACTIVITY; WORK STATUS FOR DAY IS ZERO for pid - ', person.pid
        #print '\t', person.workEpisodes, '-----------------<<<<<<<<<<<<<<<<'
        
        person.remove_episodes(person.workEpisodes)

    def remove_school_episodes(self, person):
        #for schEpisode in person.schoolEpisodes:
        #print '\tActually REMOVING SCHOOL ACTIVITY; SCHOOL STATUS FOR DAY IS ZERO for pid - ', person.pid
        #print '\t', person.schoolEpisodes, '-----------------<<<<<<<<<<<<<<<<'

        person.remove_episodes(person.schoolEpisodes)


    def resolve_conflicts_for_dependency_activities(seed):
        return self._collate_results()


    def identify_joint_episodes(self):
	if self.dependencyPersonIds == []:
	    return self._collate_results()

        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with NO dependencies - ', self.indepPersonIds

	for pid in self.dependencyPersonIds:
	    indepPersonActivityList = {}
	    person = self.persons[pid]
	    print
	    self.print_activity_list(person)
	    acts = copy.deepcopy(person.listOfActivityEpisodes)
	    for i in range(len(acts)):
    	    	stTime, act = hp.heappop(acts)
	     	
		if act.dependentPersonId <> 0:
		    indepPersonId = act.dependentPersonId
		    if indepPersonId not in indepPersonActivityList.keys():
		    	indepPersonActivityList[indepPersonId] = [act]
		    else:
		    	indepPersonActivityList[indepPersonId] += [act]

	    

	    for indepPersonId in indepPersonActivityList.keys():
		print '\tIndep Person IDs:', indepPersonId, 
	    	indepPerson = self.persons[indepPersonId]
		print 'length of all acts for person:', indepPerson.actCount
	    	activityList = indepPersonActivityList[indepPersonId]
		print '\tdependent persons acts - '
		for ac in activityList:
		    print '\t\t Dep->', ac	
	
	    	indepPersonActs = indepPerson._identify_conflict_activities(activityList)
	    	print 
	    	check = False
	    	for act in indepPersonActs:
		    if act.dependentPersonId == 99:
		    	act.dependentPersonId = 100 + pid
		    else:
		    	act.dependentPersonId = act.dependentPersonId*100 + pid 
		    	check = True
		    	print '\t\t Act Dep', act.dependentPersonId,
		    print '\tIndep->', act


	#self.lineup_ih_pickups_for_dependents()
	#raw_input()


	#    if check:
	#	raw_input()
	#update_depPersonId(self, activity, depPersonId, pid)


    def lineup_ih_pickups_for_dependents(self):
	# This lines up in home pickup episodes for dependent children

        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
	
	if len(self.dependencyPersonIds) == 0:
	    return
	
	for pid in self.indepPersonIds:
	    print '\t\tFor independent person - ', pid, 'and home loc is - ', 
	    person = self.persons[pid]
	    acts = copy.deepcopy(person.listOfActivityEpisodes)

	    subsequentPickups = False

	    stActStTime, stAct = hp.heappop(acts)
	    print stAct.location
	    homeLoc = stAct.location
	
	    for i in range(len(acts)):
		nextActStTime, nextAct = hp.heappop(acts)

	        if (stAct.actType == nextAct.actType and stAct.actType == 600 and 
			stAct.location == nextAct.location and stAct.location == homeLoc):
		   print '\t\tSubsequent pickup acts at home and we need to line them up and make appropriate adjustments to the dependent persons schedule'		
		   print '\t\tfirst Pickup   -', stAct
		   print '\t\tsecond Pickup  -', nextAct

		   stAct = person._identify_match_activity(stAct)[0] #Getting the actual start activity and not the copy for indep person
		   nextAct = person._identify_match_activity(nextAct)[0] # Getting actual next activity and not the copy for indep person



		   nextTwoActs = person._identify_next_activity(nextAct, count=2)
		   print '\t\tfirst dropoff -', nextTwoActs[0]
		   print '\t\tsecond dropoff -', nextTwoActs[1]

		   self.print_activity_list(person)

		   print '\n\t\tThe next two activities and their neighbors are - '
		   for act in nextTwoActs:
			if stAct.dependentPersonId == act.dependentPersonId:
			    stActCombo = act
			if nextAct.dependentPersonId == act.dependentPersonId:
			    nextActCombo = act

		   prevToStAct = person._identify_previous_activity(stAct)[0]
		   print '\t\tPrevAct', prevToStAct
		   print '\t\tPickup', stAct
		   stActDepPers = self.parse_personids(stAct.dependentPersonId)
		   print '\t\tDropof', stActCombo
		


		   print '\n\t\tPickup', nextAct
		   nextActDepPers = self.parse_personids(nextAct.dependentPersonId)
		   print '\t\tDropof', nextActCombo
		   nextToNextAct = person._identify_next_activity(nextActCombo)[0]	   
		   print '\t\tNextAct', nextToNextAct


		   print '\n\tWe will move the subsequent pickup activities and their go alongs to earlier'
		   print '\t\tCombined pickup time - ', stAct.startTime
		   moveBy = nextAct.startTime - stAct.startTime + 1
		   print '\t\tTherefore move the other person(s) everything by - ', 

		   print '\n\tMoving for the indep person - '
		
		   for depPersId in nextActDepPers:
			stAct.dependentPersonId = stAct.dependentPersonId*100 + depPersId # The pickup dependentperson id updated to include everyone

		   nextActCopy = copy.deepcopy(nextAct)
		   nextActComboCopy = copy.deepcopy(nextActCombo)
		   person.move_start_end(nextActCombo, -moveBy)
		   if not person._check_for_conflicts():
			moveConflictCreated = True
		   	person.move_start_end(nextActCombo, 1)			
		   else:
			moveConflictCreated = False

		   person.remove_episodes([nextAct])

		   
		   for depPersId in stActDepPers:
			print '\n\tFor dependent person - ', depPersId
			depPers = self.persons[depPersId]
			prevToPickupSt = depPers._identify_previous_activity(stAct)[0]
			pickUpDropOffActsSt = depPers._identify_match_activities([stAct, stActCombo]) #Getting the actual activities and not the copy for dep person
			nextToDropOffSt = depPers._identify_next_activity(stActCombo)[0]
			print '\t\tPrevious to pickup- ', prevToPickupSt
			print '\t\tPickup            -', pickUpDropOffActsSt[0]
			print '\t\tDropoff           -', pickUpDropOffActsSt[1]
			print '\t\tNext to dropoff   -', nextToDropOffSt

		   

		   for depPersId in nextActDepPers:
		       	print '\n\tFor dependent person - ', depPersId
			depPers = self.persons[depPersId]
			prevToPickup = depPers._identify_previous_activity(nextActCopy)[0]
			pickUpDropOffActs = depPers._identify_match_activities([nextActCopy, nextActComboCopy]) #Getting the actual activities and not the copy for dep person
			nextToDropOff = depPers._identify_next_activity(nextActComboCopy)[0]
			print '\t\tPrevious to pickup- ', prevToPickup
			print '\t\tPickup            -', pickUpDropOffActs[0]
			print '\t\tDropoff           -', pickUpDropOffActs[1]
			print '\t\tNext to dropoff   -', nextToDropOff
		   
			depPers.move_end(prevToPickup, prevToPickup.endTime-moveBy + 1)
			prevToPickup.dependentPersonId = prevToPickupSt.dependentPersonId # since we moved we can allocate this persons 
											  # act before pickup to the same adult as the one we used as reference to move i.e. st
			prevDepAdult = self.persons[prevToPickupSt.dependentPersonId]
			self.print_activity_list(prevDepAdult)
			prevDepAdultPrevToPickup = prevDepAdult._identify_match_activities([prevToPickupSt])[0]
			prevDepAdultPrevToPickup.dependentPersonId = prevDepAdultPrevToPickup.dependentPersonId*100 + depPersId # also update the corresponding act dependency for indep adult


			depPers.move_start_end(pickUpDropOffActs[0], -moveBy)			
			if moveConflictCreated:
			    depPers.move_start_end(pickUpDropOffActs[1], -moveBy+ 1)	
			else:
			    depPers.move_start_end(pickUpDropOffActs[1], -moveBy)				

			nextToDropOffForIndep = person._identify_match_activities([nextToDropOff])
			print nextToDropOffForIndep
			if nextToDropOffForIndep <> []:
			    nextToDropOffForIndep = nextToDropOffForIndep[0]

			if moveConflictCreated:
			    depPers.move_start(nextToDropOff, nextToDropOff.startTime-moveBy+1 + 1)
			    if nextToDropOffForIndep <> []:
			         depPers.move_start(nextToDropOffForIndep, nextToDropOff.startTime-moveBy+1 + 1)
			else:
			    depPers.move_start(nextToDropOff, nextToDropOff.startTime-moveBy+1)
			    if nextToDropOffForIndep <> []:
			    	depPers.move_start(nextToDropOffForIndep, nextToDropOff.startTime-moveBy+1)

			print '\t\tAftAdj: Previous to pickup- ', prevToPickup
			print '\t\tAftAdj: Pickup            -', pickUpDropOffActs[0]
			print '\t\tAftAdj: Dropoff           -', pickUpDropOffActs[1]
			print '\t\tAftAdj: Next to dropoff   -', nextToDropOff


			#MOVE START OR END - goes to a reference value also we need to do a + 1 adjustment for move
			#MOVEBY START AND END - moves start and end of activity by that amount
	           break

		# for each person in the dependent person list now move/adjust the pickup, dropoff and the nexst activity
		    



		stAct = nextAct

	    	#indepPersonActs = indepPerson._identify_conflict_activities(activityList)
	
    def parse_personids(self, tripDep):
	cpTripDep = copy.deepcopy(tripDep)
	modGrt100 = True
	pers = []
	while(modGrt100):
	    cpTripDep, pid = divmod(cpTripDep, 100)
	    #print cpTripDep, pid
	    if pid <> 0 and cpTripDep>0:
		pers.append(pid)
	    if cpTripDep > 100:
		modGrt100 = True
	    else:
		modGrt100 = False
	#print tripDep, pers
	if len(pers) > 1:
	    print 'Exciting picking up more than one persoallocate_dependent_activitiesn ... '
	return pers


    def identify_joint_episodes1(self):
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        print '\tPerson Ids with NO dependencies - ', self.indepPersonIds
	
	
	self.initialize_dependencyStatusObject()
    	self.locked_adults()
	
	for pid in self.dependencyPersonIds:
	    person = self.persons[pid]
	    self.print_activity_list(person, dependent=True)
	self.print_joint_acts()

    def initialize_dependencyStatusObject(self):
	self.depenLocks = {}
	maxPid = max(self.persons.keys())
	for pid in self.persons.keys():
	    statusObject = zeros((maxPid+1, 1440), dtype=int)
	    self.depenLocks[pid] = statusObject
	
    def locked_adults(self):
	locekdAdults = {}
	for pid in self.dependencyPersonIds:
	    person = self.persons[pid]
	    self.locked_adults_for_person(person)


    def locked_adults_for_person(self, person):
	acts = copy.deepcopy(person.listOfActivityEpisodes)
    	depPers = person.pid
	for i in range(len(acts)):
    	    stTime, act = hp.heappop(acts)
	
	    if act.dependentPersonId <> 0:
		stTime = act.startTime
		endTime = act.endTime
		indepPers = act.dependentPersonId
		self.depenLocks[depPers][indepPers][stTime:endTime] = 1 #dependent person tree
		self.depenLocks[indepPers][depPers][stTime:endTime] = 1

    def print_joint_acts(self):
	for pid in self.indepPersonIds:
	    print '\nFor person - ', pid
	    print '\t\tshape', self.depenLocks[pid].sum(0).shape
	    print '\t\taccompaniment', self.depenLocks[pid].sum(0)


    def lineup_allocate_start_of_day_episodes_for_dependents(self):
        print '\tPerson Ids with dependencies - ', self.dependencyPersonIds

	minStart = 1440
	maxStart = -1
	startTimeList = []
	for pid in self.dependencyPersonIds:
	    depPerson = self.persons[pid]
	
	    print depPerson.firstEpisode
	    startTimeList.append(depPerson.firstEpisode.endTime)
	    if depPerson.firstEpisode.endTime < minStart:
		minStart = depPerson.firstEpisode.endTime
	    if depPerson.firstEpisode.endTime > maxStart:
		maxStart = depPerson.firstEpisode.endTime
		
            actsOfDepPerson = copy.deepcopy(depPerson.listOfActivityEpisodes)

	    print 'for person - ', pid
            stActStartTime, stAct = hp.heappop(actsOfDepPerson)
            endActStartTime, endAct = hp.heappop(actsOfDepPerson)
	    print '\tStart - ', stAct
	    print '\tEnd - ', endAct

	    self.create_dummy_activity(pid, stAct, endAct)

	startTimeList.sort()
	print 'School Min Start - %s and Max Start - %s and sorted start - %s' %(minStart, maxStart, startTimeList)
	
    def allocate_dependent_activities(self, seed):
	self.unallocatedActs = {}
	self.lenUnallocatedActs = 0
        self.seed = seed
        self.rndGen = RandomDistribution(int(self.hid + self.seed))

	#print 'Household ID - ', self.hid
        #print '\tPerson Ids with dependencies - ', self.dependencyPersonIds
        #print '\tPerson Ids with fixed activities - ', self.dailyFixedActPersonIds
        #print '\tPerson Ids with no fixed activities - ', self.noDailyFixedActPersonIds

        if len(self.dependencyPersonIds) > 0:
            #print 'DEPENDENCIES EXIST; ACTIVITIES NEED TO BE ALLOCATED TO INDEPENDENT PERSONS'
	    pass

        # For each person identify an adult that has open 
        # periods and then allocate to him
            for pid in self.dependencyPersonIds:
                person = self.persons[pid]

                actsOfDepPerson = copy.deepcopy(person.listOfActivityEpisodes)


                print 'ALLOCATING ACTIVITIES FOR PERSON ID - ', pid
                #self.print_activity_list(person)
                stActStartTime, stAct = hp.heappop(actsOfDepPerson)
                #hp.heappop(person.listOfActivityEpisodes)


                print '\n\t\t1.1. End of Day/Start of Day: Someone needs to be there'
		print '\t\t', stAct
                self.adjust_terminal_activity_episodes(pid, stAct, start=True)

                #raw_input()

                print '\n\t\t1.2. End of Day/Start of Day: Someone needs to be there'
                endAct = person.lastEpisode
		print '\t\t', endAct
                self.adjust_terminal_activity_episodes(pid, endAct, start=False)                    



                actsInTour = []
                inHomeActs = []
                while (len(actsOfDepPerson) > 0):
                    endActStartTime, endAct = hp.heappop(actsOfDepPerson)
                    #hp.heappop(person.listOfActivityEpisodes)
		    print 'NEW END ACTIVITY _ ', endAct
                    



                    if (endAct.location <> stAct.location) and (endAct.actType >= 400 and endAct.actType < 500):
                        print '\n\t\t2.2. OH Act: Activity-travel chain with maintenance activities'
                        print '\t\t\t START-', stAct
                        print '\t\t\t END-  ', endAct
                        actsInTour.append(stAct)
                    elif len(actsInTour) > 0:
                        actsInTour.append(stAct)
                        actsInTour.append(endAct)
                        
                        #self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        #print "TRIP CHAIN IDENTIFIED"
                        #for act in actsInTour:
                        #    print act
                        #raw_input()
                        self.allocate_trip_activity_chain(pid, actsInTour)
			self.print_activity_list(person)
                        if endAct.actType < 200 and endAct.actType > 100:
                            self.allocate_ih_activity(pid, endAct)
                        #raw_input()
                        actsInTour=[]
                        stAct = endAct
                        continue


                    # Building the tour activities
                    if len(actsInTour) > 0:
                        stAct = endAct
                        continue


                    if (endAct.location <> stAct.location)  and (endAct.actType >= 500 or 
                                                                 (endAct.actType < 400 and endAct.actType >= 200) or
                                                                 (endAct.actType <= 100)):
                        print '\n\t\t2.3. OH Act: Terminal activity is not a Maint. activity and end act need not be allocated'
                        print '\t\t\t Terminal Activity-', endAct
                        self.allocate_pickup_dropoff(pid, stAct, endAct)
                        stAct = endAct
                        continue

                    # ALLOCATE PREVIOUS INHOME TO END SOJOURN ADULT - Case1
                    # ALLOCATE PICK-UP DROP-OFF TO END SOJOURN ADULT WHEN PREVIOUS OUTHOME - Case2 (see below started coding)

                    if (endAct.location <> stAct.location)  and (endAct.actType > 100 and endAct.actType < 200):
                        print '\n\t\t2.4. Return Home Act: Allocate the IH activity as well'
                        print '\t\t\t Terminal Activity-', endAct
                        self.allocate_pickup_dropoff_endact(pid, stAct, endAct)
                        stAct = endAct
                        continue

                    if (endAct.location == stAct.location) and (endAct.actType > 100 and endAct.actType < 200):
                        print '\n\t\t2.1. IH Act: Someone needs to be there'
                        print '\t\t\t', endAct
                        self.allocate_ih_activity(pid, endAct)
                        stAct = endAct
                        continue


                    #print 'is it even getting here'

                    stAct = endAct
                    #raw_input()
	    for pid in self.unallocatedActs.keys():
		print 'Unallocated activities for person - ', pid
		
		actList = self.unallocatedActs[pid]
		
		for act in actList:
		    if len(act) == 2:
			print '\tjust a pickup and dropoff for houseid - %s personid - %s' %(self.hid, pid)
		    if len(act) == 3:
			print '\tjust a pickup and dropoff and terminal activity for houseid - %s personid - %s' %(self.hid, pid)
		    if len(act) > 3:
			print '\tactivity chain for houseid - %s personid - %s' %(self.hid, pid)

		    for a in act:
			print '\t    act-', a

	    if len(self.unallocatedActs.keys()) > 0:
	    	print 'lenof unallocated acts - ', self.lenUnallocatedActs
		raw_input()
	


    def print_activity_list(self, person, dependent=False):
        print '\t--> ACTIVITY LIST for person - ', person.hid, person.pid
        acts = copy.deepcopy(person.listOfActivityEpisodes)
        for i in range(len(acts)):
	    stTime, act = hp.heappop(acts)
	    if not dependent:
		print '\t\t', act
	    elif act.dependentPersonId <> 0:
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
        
        #print '\t\t\t\tAdjusting the terminal start-"%s" activity episodes to ensure that the child is taken care of' %(start)
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


        #print """\t\t\t --- > Exception: No person identified that can be with the """\
        #    """dependent child for the terminal episodes in a day"""\

        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities and  then adjust their terminal 
        # episode durations so that children are not abandoned


        if start:
            terminalAct = depPerson.firstEpisode
        else:
            terminalAct = depPerson.lastEpisode


        pid = self.personId_with_terminal_episode_overlap(depPersonId, [terminalAct], 
                                                          self.indepPersonIds)

        #pid = self.personId_with_least_conflict([terminalAct], 
        #                                        self.indepPersonIds)
        if pid is None:
            print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return


        print "\t\t\t\t--Randomly independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #actOfPerson = self.find_terminal_vertex(person, start)


        

        if start:
            person.move_start_of_day(actOfdepPerson.endTime)
        else:
            person.move_end_of_day(actOfdepPerson.startTime)
        
        """
        # Alternative implementation
        if start:
            actOfPerson = person.firstEpisode
            depPerson.move_start_of_day(actOfPerson.endTime)
        else:
            actOfPerson = person.lastEpisode
            depPerson.move_end_of_day(actOfPerson.startTime)

        """

        if not person._check_for_conflicts_with_activity(actOfdepPerson):
            print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies([actOfdepPerson])
            #self.print_activity_list(person)
            #raw_input()

        self.update_depPersonId_for_terminal_episode(start, depPersonId, pid)
        return True


    def update_depPersonId_for_terminal_episode(self, start, depPersonId, pid):
	print '\t--> Terminal episode allocated to - ', pid
        depPerson = self.persons[depPersonId]
        if start:
            depPerson.firstEpisode.dependentPersonId = pid
        else:
            depPerson.lastEpisode.dependentPersonId = pid            
	assignPerson = self.persons[pid]
	#self.print_activity_list(assignPerson)
        
            


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
                #person.remove_episodes([act])
                return True
            else:
                pass
                #person.remove_episodes([act])                
                


        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1
            person.add_episodes([act], temp=True)
            
            if not person._check_for_conflicts_with_activity(act):
                person.remove_episodes([act])
            else:
                print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.update_depPersonId(act, depPersonId, pid)
                return True
                
        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            act.scheduleId = person.actCount + 1            
            person.add_episodes([act], temp=True)

            if not person._check_for_conflicts_with_activity(act):
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
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        act.scheduleId = person.actCount + 1
        person.add_episodes([act], temp=True)
        self.update_depPersonId(act, depPersonId, pid)


        #person._check_for_conflicts()            

        if not person._check_for_conflicts_with_activity(act):
            print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)        
            person.adjust_child_dependencies([act])
            #self.print_activity_list(person)        


        #person.adjust_activity_schedules(self.seed)
        return True        

    def update_depPersonId(self, activity, depPersonId, pid):
	print '\t--> Activity episode allocated to - ', pid
	if not isinstance(activity, list):
	    activityList = [activity]
	else:
	    activityList = activity
	
        depPerson = self.persons[depPersonId]

	for activity in activityList:
            for actStart, act in depPerson.listOfActivityEpisodes:
            	if act.startTime == activity.startTime:
		    #print '------>BEFORE ASSIGN', act			
            	    act.dependentPersonId = pid
	       	    #print '-------------->AFTER ASSIGN', act
        #indAct = depPerson.listOfActivityEpisodes.index((activity.startTime, activity))
        #act = depPerson.listOfActivities[indAct]
        
        #act.dependentPersonId = pid
	
		
	#self.print_activity_list(depPerson)

	assignPerson = self.persons[pid]
	#self.print_activity_list(assignPerson)

        #print pid
        #raw_input('FOUND THE INDEX')

    def allocate_pickup_dropoff(self, depPersonId, stAct, endAct):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:
        dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, stAct, endAct)

        dummyActPickUp.dependentPersonId = 99
        dummyActDropOff.dependentPersonId = 99

        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)           

            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
                #if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff])           
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True
                
        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            dummyActPickUp.scheduleId = person.actCount + 1
            dummyActDropOff.scheduleId = person.actCount + 2     

            person.add_episodes([dummyActPickUp, dummyActDropOff], temp=True)

            #if not person._check_for_conflicts():
            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
                person.remove_episodes([dummyActPickUp, dummyActDropOff])
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, 
                                                [dummyActPickUp, dummyActDropOff], 
                                                self.indepPersonIds)

        if pid is None:
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2
        person.add_episodes([dummyActPickUp, dummyActDropOff])
	"""
	if person._check_for_home_to_home_trips():
	    person.remove_episodes([dummyActPickUp, dummyActDropOff])	    
            print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----'
	    return False
	"""
        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)

        #person._check_for_conflicts()


        if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff]):
            print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
	    #print '\n\tDummy pickup', dummyActPickUp
	    #print '\tDummy dropoff', dummyActDropOff
            person.adjust_child_dependencies([dummyActPickUp, dummyActDropOff])
            #self.print_activity_list(person)

        return True


    def create_dummy_activity_for_chain(self, depPersonId, actsInTour):
        intActCount = len(actsInTour) - 2

        # Building the dummy pickup and drop-offs for the chain
        actIncChauffering = []
        chaufferingEpisodes = []
        for i in range(intActCount + 1):
            dummyActPickUp, dummyActDropOff = self.create_dummy_activity(depPersonId, 
                                                                         actsInTour[i+0], 
                                                                         actsInTour[i+1])

            dummyActPickUp.dependentPersonId = 99
            dummyActDropOff.dependentPersonId = 99
            actsInTour[i+1].dependentPersonId = 99
            actsInTour[i+1].actType += 50
            
            chaufferingEpisodes.append(dummyActPickUp)
            chaufferingEpisodes.append(dummyActDropOff)

            actIncChauffering.append(dummyActPickUp)
            actIncChauffering.append(dummyActDropOff)
            actIncChauffering.append(actsInTour[i+1])
        # Removing the last anchor because that is not 
        # pursued by the allocated dependent person
        actIncChauffering = actIncChauffering[:-1]
        
        return actIncChauffering, chaufferingEpisodes
           
            

    def intermediate_acts(self, actsInTour):
        intActCount = len(actsInTour) - 2
        
        intActs = []
        for i in range(intActCount):
            intActs.append(actsInTour[i+1])
            
        return intActs


    def allocate_trip_activity_chain(self, depPersonId, actsInTour):
        # Create pickup-dropoff for the front end of the activity
        #if pickup:

        actsInTourCopy = copy.deepcopy(actsInTour)
        actIncChauffering, chaufferingEpisodes = self.create_dummy_activity_for_chain(depPersonId, 
                                                                                      actsInTourCopy)
        intActs = self.intermediate_acts(actsInTour)

	print '\t\tActs including chauffering - '
	for act in actIncChauffering:
	    print '\t\t    ',act

        # Person without fixed activities
        #print '\t\t\tScanning person without fixed activities - '
        # We allocate pickup/dropoff to the first person with no fixed activities that we find

        self.rndGen.shuffle_sequence(self.noDailyFixedActPersonIds)

        for pid in self.noDailyFixedActPersonIds:
            # Create dummy travel episodes
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            for actNum in range(len(actIncChauffering)):
                act = actIncChauffering[actNum]
                act.scheduleId = person.actCount + actNum + 1
            person.add_episodes(actIncChauffering, temp=True)           
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            #if not person._check_for_conflicts():
            if not person._check_for_conflicts_with_activity(actIncChauffering):                
                person.remove_episodes(actIncChauffering)           
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
	        #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)
		self.update_depPersonId(actIncChauffering, depPersonId, pid)
                for intAct in intActs:
                    intAct.dependentPersonId = pid
                return True
                
        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
        # We allocate pickup/dropoff to the first person with fixed activities that we find

        self.rndGen.shuffle_sequence(self.dailyFixedActPersonIds)

        for pid in self.dailyFixedActPersonIds:
            person = self.persons[pid]
            #self.print_activity_list(person)
            #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
            for actNum in range(len(actIncChauffering)):
                act = actIncChauffering[actNum]
                act.scheduleId = person.actCount + actNum + 1
            person.add_episodes(actIncChauffering, temp=True)
            #print 'THE ACT COUNT AFTER ADDING', person.actCount, len(person.listOfActivityEpisodes)
            #self.print_activity_list(person)
            #if not person._check_f = 0or_conflicts():
            if not person._check_for_conflicts_with_activity(actIncChauffering):
                person.remove_episodes(actIncChauffering)
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
                #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)
		self.update_depPersonId(actIncChauffering, depPersonId, pid)
                for intAct in intActs:
                    intAct.dependentPersonId = pid
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, 
                                                actIncChauffering, 
                                                self.indepPersonIds)

        if pid is None:
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #self.print_activity_list(person)        
        #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
        for actNum in range(len(actIncChauffering)):
            act = actIncChauffering[actNum]
            act.scheduleId = person.actCount + actNum + 1

        person.add_episodes(actIncChauffering)
        self.add_activity_update_depPersonId(chaufferingEpisodes, depPersonId, pid)
        #self.add_activity_update_depPersonId(actIncChauffering, depPersonId, pid)


	"""
	if person._check_for_home_to_home_trips():
	    person.remove_episodes(actIncChauffering)	    
            print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----'
	    return False
	"""
	self.update_depPersonId(actIncChauffering, depPersonId, pid)
        for intAct in intActs:
            intAct.dependentPersonId = pid

        #person._check_for_conflicts()

        if not person._check_for_conflicts_with_activity(actIncChauffering):
            print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies(actIncChauffering)
            #self.print_activity_list(person)
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
        #print '\t\t\tScanning person without fixed activities - '
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
            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff, 
                                                              endActToNonDependent]):
                #if not person._check_for_conflicts():
                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])           
            else:
                #print '\t\t\t\tPerson with no fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
		self.update_depPersonId([dummyActPickUp, dummyActDropOff, 
                                                              endActToNonDependent], depPersonId, pid)
                endAct.dependentPersonId = pid
                return True
                
        # Person with fixed activities
        #print '\t\t\tScanning person with fixed activities - '
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
            #if not person._check_for_conflicts():
            if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff, 
                                                              endActToNonDependent]):                

                person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            else:
                #print '\t\t\t\tPerson with fixed activities found and id is -- ', pid
                self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
		self.update_depPersonId([dummyActPickUp, dummyActDropOff, 
                                                              endActToNonDependent], depPersonId, pid)

                endAct.dependentPersonId = pid
                return True

        #print "\t\t\t --- > Exception: No person identified; not possible; the dependent acts cause conflicts < --- "


        # Since there are no people that can be identified without causing conflicts
        # we randomly select either a person with no fixed acts 
        # if there are no persons with 0 fixed activities then we randomly select
        # one person with fixed activity/activities


        pid = self.personId_with_least_conflict(depPersonId, 
                                                [dummyActPickUp, dummyActDropOff, endActToNonDependent], 
                                                self.indepPersonIds)

        if pid is None:
            #print "Exception, --There are no independent adults in the household for hid - %s--" %(self.hid)
            return

        #print "\t\t\t\t--Random independent adults in the household is selected and id is --", pid

        person = self.persons[pid]
        #self.print_activity_list(person)        
        #print 'THE ACT COUNT BEFORE ADDING', person.actCount, len(person.listOfActivityEpisodes)
        dummyActPickUp.scheduleId = person.actCount + 1
        dummyActDropOff.scheduleId = person.actCount + 2
        endActToNonDependent.scheduleId = person.actCount + 3       
        person.add_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])

	"""
	if person._check_for_home_to_home_trips():
            print '\t----- CHECKING TO SEE IF THE ADULT WITH LEAST CONFLICT HAS IN_HOME_IN_HOME TRIPS BEING INTRODUCED-----??'
	    person.remove_episodes([dummyActPickUp, dummyActDropOff, endActToNonDependent])	    
            print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----'
	    return False

	"""

        self.add_activity_update_depPersonId([dummyActPickUp, dummyActDropOff], depPersonId, pid)
	self.update_depPersonId([dummyActPickUp, dummyActDropOff, 
                                 endActToNonDependent], depPersonId, pid)

        endAct.dependentPersonId = pid

        #person._check_for_conflicts()

        if not person._check_for_conflicts_with_activity([dummyActPickUp, dummyActDropOff, 
                                                          endActToNonDependent]):
            print '\t----- NEED TO ADJUST THIS PERSONS ACT SCHEDULE -----'
            #self.print_activity_list(person)
            person.adjust_child_dependencies([dummyActPickUp, dummyActDropOff, endActToNonDependent])
            #self.print_activity_list(person)
        return True
            

    def add_activity_update_depPersonId(self, activityList, depPersonId, pid):
	print '\t--> Activity list allocated to - ', pid	
        depPerson = self.persons[depPersonId]

        activityList = copy.deepcopy(activityList)

        for i in range(len(activityList)):
            act = activityList[i]
            act.scheduleId = depPerson.actCount + i + 1
            act.dependentPersonId = pid

        depPerson.add_episodes(activityList)
        depPerson._check_for_conflicts()
        
	assignPerson = self.persons[pid]
	#self.print_activity_list(assignPerson)



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

	    if person._check_for_home_to_home_trips():
                print '\t----- CHECKING TO SEE IF THE ADULT WITH LEAST CONFLICT HAS IN_HOME_IN_HOME TRIPS BEING INTRODUCED-----??', pid
		checkForHomeToHomeTrips = True
            	print '\t----- NOT ALLOCATING TO THIS ADULT WITH LEAST CONFLICT BECAUSE IN_HOME_IN_HOME TRIPS ARE BEING INTRODUCED-----', pid

	    else:
		checkForHomeToHomeTrips = False

            person.remove_episodes(activityList)

            conflictActs = person._identify_conflict_activities(activityList)
            checkForDependencies = self._check_for_dependencies_for_conflictActivities(depPersonId,
                                                                                       conflictActs)

		

            #print 'Conflict acts for person id - ', pid
            #for act in conflictActs:
            #    print '\t', act            



            if not checkForDependencies:
                continue

	    if checkForHomeToHomeTrips == True:
		continue

            personConflict[pid] = conflict
            personConflictActs[pid] = conflictActs

        #print personConflict
        #print personConflictActs

            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid, conflict)

        if len(personConflict) > 0:
            leastConflict = min(personConflict.values())
        else:
	    if depPersonId not in self.unallocatedActs.keys():
	    	self.unallocatedActs[depPersonId] = [activityList]
		self.lenUnallocatedActs += 1
	    else:
	    	self.unallocatedActs[depPersonId].append(activityList)		
		self.lenUnallocatedActs += 1
            return


	personIdsWithConflict = copy.deepcopy(personConflict.keys())
        for pid in personIdsWithConflict:
            #print '\t\t\t\t\tperson - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:
	
                return pid



    def _check_for_dependencies_for_conflictActivities(self, depPersonId, conflictActs):
        #print '\t\t\t\tCHECKING FOR DEPENDENCIES for dep act of person - ', depPersonId

        for act in conflictActs:
            #print '\t\t\t\t\t', act
            print '\tdependencies for conflicts - ', act.dependentPersonId, depPersonId
            if act.startTime == 0 or act.endTime == 1439:
                if (act.dependentPersonId > 0 and act.dependentPersonId < 99 and act.dependentPersonId <> depPersonId):
                    #print act
                    raw_input()
                    raise Exception, 'This should never happen'
                    #return False
            #print 'DEP IDS', act.dependentPersonId, depPersonId
            if act.dependentPersonId == 99:
                #print act, depPersonId
                #raw_input()
                return False
        return True


    def personId_with_terminal_episode_overlap(self, depPersonId, activityList, personIdList):
        #print activityList
        personConflict = {}

        for pid in personIdList:
            #print '\tConflict acts for person id - ', pid
            person = self.persons[pid]
	    #print self.print_activity_list(person)
            person.add_episodes(activityList, temp=True)


            stEpisode = person.firstEpisode
            conflictWithStartEpisode = person._conflict_duration_with_activity(stEpisode)
            
            enEpisode = person.lastEpisode
            conflictWithEndEpisode = person._conflict_duration_with_activity(enEpisode)

            conflictWithTermEpisodes = conflictWithStartEpisode + conflictWithEndEpisode
            conflict = person._conflict_duration()
            person.remove_episodes(activityList)


            conflictActs = person._identify_conflict_activities(activityList)
            checkForDependencies = self._check_for_dependencies_for_conflictActivities(depPersonId,
                                                                                       conflictActs)
	    #print 'check for dependencies', pid, checkForDependencies

            #print 'with start, with end, full conflict'
            #print conflictWithStartEpisode, conflictWithEndEpisode, conflict
            #for act in conflictActs:
            #    print '\t', act

            if not checkForDependencies:
                continue

            
            personConflict[pid] = conflict - conflictWithTermEpisodes


            #print '\t\t\t\t\tPerson - %s has conflict of duration - %s  for above activity' %(pid, 
            #                                                                                  (conflict - 
            #                                                                                   conflictWithTerminalEpisode))
            #print '\t\t\t\t\tConflict - %s and conflict with last episode - %s' %(conflict,
            #                                                                      conflictWithTerminalEpisode)

            leastConflict = min(personConflict.values())

        for pid in personConflict.keys():
            #print 'person - ', pid, 'conflict for person - ', personConflict[pid], 'least conflict', leastConflict
            if personConflict[pid] == leastConflict:
                #print '\t\t\t\tPerson with least conflict with terminal episode is', pid
                return pid
                
                
            
            
            


            

            
    def create_dummy_activity(self, depPersonId, stAct, endAct):
        dummyPickUpAct = copy.deepcopy(stAct)
        dummyDropOffAct = copy.deepcopy(endAct)


        # Pickup overlaps with the end of an activity
        dummyPickUpAct.startTime = dummyPickUpAct.endTime 
        dummyPickUpAct.endTime = dummyPickUpAct.startTime + 1
        dummyPickUpAct.duration = 1
        dummyPickUpAct.actType = 600
        dummyPickUpAct.startOfDay = False
        dummyPickUpAct.endOfDay = False
        dummyPickUpAct.dependentPersonId = 0

        # dropoff overlaps with the start of an activity
        dummyDropOffAct.startTime = dummyDropOffAct.startTime - 1
        dummyDropOffAct.endTime = dummyDropOffAct.startTime + 1
        dummyDropOffAct.duration = 1
        dummyDropOffAct.actType = 601
        dummyDropOffAct.startOfDay = False
        dummyDropOffAct.endOfDay = False
        dummyDropOffAct.dependentPersonId = 0


        print '\n\t\t\tPICKUP ACTIVITY - ', dummyPickUpAct

        print '\t\t\tDropOff ACTIVITY -', dummyDropOffAct


        return dummyPickUpAct, dummyDropOffAct


        










