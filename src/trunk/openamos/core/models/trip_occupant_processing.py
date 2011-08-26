import copy

from numpy import array, logical_and, histogram, zeros, amax, unique


from openamos.core.models.abstract_model import Model
from openamos.core.data_array import DataArray



class TripOccupantProcessing(Model):
    def __init__(self, specification):
        Model.__init__(self, specification)
        self.specification = specification

	self.idSpec = specification.idSpec
	self.tripDepAttribSpec = specification.tripDepAttribSpec



    def create_col_numbers(self, colnamesDict):
        #print colnamesDict
	self.hidCol = colnamesDict[self.idSpec.hidName]
	self.pidCol = colnamesDict[self.idSpec.pidName]

	self.tripPurposeFromNameCol = colnamesDict[self.tripDepAttribSpec.tripPpurposeFromName]
	self.tripDepNameCol = colnamesDict[self.tripDepAttribSpec.tripDepName]
	self.lastTripDepNameCol = colnamesDict[self.tripDepAttribSpec.lastTripDepName]
	self.stActDepNameCol = colnamesDict[self.tripDepAttribSpec.stActDepName]
	self.enActDepNameCol = colnamesDict[self.tripDepAttribSpec.enActDepName]


    def resolve_consistency(self, data, seed):
        self.create_col_numbers(data._colnames)
	
	print '--------------------------------------------'
	for rowId in range(data.rows):
	    row = data.data[rowId,:]   
	    hid = row[self.hidCol]
	    pid = row[self.pidCol]
	    tripPurposeFrom = row[self.tripPurposeFromNameCol]
	    lastTripDep = row[self.lastTripDepNameCol]
	    stActDep = row[self.stActDepNameCol]
	    enActDep = row[self.enActDepNameCol]
	
	    print 'For hid - %s and pid - %s' %(hid, pid)
	    print '     The trip purpose from is - ', tripPurposeFrom
	    if tripPurposeFrom == 600 or tripPurposeFrom == 601:
		if stActDep > 100:
		    print '\ta.2. The occupancy of the trip changed and processing occupancy now ... stActDep - %s' %stActDep
		    tripDepPers = self.parse_trip_dependentpersonid(lastTripDep, stActDep, tripPurposeFrom)
		    print '\t-->New dependentperson - %s<--' %tripDepPers, type(tripDepPers)

		else:
		    print '\ta.2. No need to process occupancy this is a dependent person ... stActDep - %s' %stActDep
		    tripDepPers = stActDep	
	    else:
		print '\ta.1. The occupancy of the trip did not change and occupancy is - ', lastTripDep
		tripDepPers = lastTripDep
	

	    data.data[rowId, self.tripDepNameCol] = tripDepPers

        return data

    def parse_trip_dependentpersonid(self, lastTripDep, stActDep, tripPurposeFrom):
	print '\t\tStart Activity Dep - %s' %(stActDep)

	lastTripPersons = self.parse_personids(lastTripDep)	
	print '\t\tThe number of people on the previous trip is - %s and they are - %s and depid is - %s' %(len(lastTripPersons), lastTripPersons, lastTripDep)

	
	if tripPurposeFrom == 600:
	    pickupPersons = self.parse_personids(stActDep)	    
	    print '\t\tThis is a pickup so we should take all people from dummy pickup loc; count of people - %s and they are - %s ... ' %(len(pickupPersons), pickupPersons)


	    lastTripPersons += pickupPersons



	if tripPurposeFrom == 601:
	    dropoffPersons = self.parse_personids(stActDep)	    
	    print '\t\tThis is a dropoff so we should take all people from dummy pickup loc; count of people - %s and they are - %s ... ' %(len(dropoffPersons), dropoffPersons)
		
	    for person in dropoffPersons:
		try:
		    lastTripPersons.remove(person)
		except ValueError, e:
		    raise Exception, 'The person - %s should be on the trip check again error occurred and last trip persons - %s' %(person, lastTripPersons)
	
	lastTripPersonsNum = 1
	for person in lastTripPersons:
	    lastTripPersonsNum = lastTripPersonsNum*100 + person

	return lastTripPersonsNum
	
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
	    print 'Exciting picking up more than one person ... '
	return pers
	
    def add_dependentpersonid(self,):
	pass


    def remove_dependentpersonid(self,):
	pass
        
