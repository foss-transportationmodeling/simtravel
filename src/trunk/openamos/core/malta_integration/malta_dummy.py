from numpy import array, zeros
from numpy.random import randint, seed


from openamos.core.malta_integration.simulation_manager_malta import SimulationManager


class DummyMALTA(object):
    def __init__(self):
	self.trips = {}
	self.tripsAct = {}

	self.manager = SimulationManager()

    def request_trips(self):
	
	for i in range(1440):
	    seed(i)
	    time = i
	
	    if time in self.tripsAct.keys():
		print 'Following trips have reached the destination in time - %s' %time, self.tripsAct[time]
		tripIdsArrived = self.tripsAct.pop(time)
		tripInfoArrivals = array(tripIdsArrived)
	    else:
		tripInfoArrivals = array([-1])
		

	    trips = self.manager.run_selected_components_for_malta(analysisInterval=time, tripInfoArrivals=tripInfoArrivals)

	    if trips[0,0] <> 0:
		print trips.astype(int)
		for trip in trips:
		    #key = endtime and val list = trips
		    if trip[8] not in self.trips.keys():
			self.trips[trip[8]] = [trip[0]]
		    else:
			self.trips[trip[8]] += [trip[0]]


		    actArrival = randint(trip[7]+2, trip[8]+15)

		    if actArrival not in self.tripsAct.keys():
			self.tripsAct[actArrival]  = [trip[0]]
		    else:
			self.tripsAct[actArrival] += [trip[0]]

		    #if trip[0] >= 70 and trip[0] <=80:
		    #	print 'tripid - %s, expected arrival - %s and actual arrival - %s' %(trip[0], trip[8], actArrival)
		    #	raw_input()

	    
	

if __name__ == '__main__':
    d = DummyMALTA()

    d.request_trips()
