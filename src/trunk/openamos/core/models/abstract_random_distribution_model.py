from numpy import zeros, array
from numpy.random.mtrand import RandomState

class RandomDistribution(object):
    def __init__(self, seed):
        #RandomState.__init__(self, seed)
        self.seed = seed

    def return_normal_variables(self, location, scale, size):
        if scale == 0:
            return zeros(size) + location

	norm_vars = []
	
	
	#print 'Here is the size - ', size
	for count in range(size[0]):
	    i = self.seed[count]

	    try:
	    	locI = location[count]
	    except TypeError, e:
		locI = location

	    randStObj = RandomState(i)
	    norm_vars.append(randStObj.normal(loc=locI, scale=scale))

	norm_vars = array(norm_vars)
	norm_vars.shape = (size[0],1)

	#print 'Returning shape', norm_vars.shape


        return norm_vars

        
    def return_random_variables(self, size=None):
	#print 'this is size in random variables - ', size
	#print 'this is seed - ', self.seed
    	rand_vars = []
	for count in range(size):
	    i = self.seed[count]

	    randStObj = RandomState(i)
	    rand_vars.append(randStObj.random_sample())

	rand_vars = array(rand_vars)

        return rand_vars

    def return_random_integers(self, low, high=None, size=None):
	rand_vars = []
	for count in range(size[0]):
	    i = self.seed[count]

	    randStObj = RandomState(i)
	    rand_vars.append(randStObj.random_intergers(low, high))

	rand_vars = array(rand_vars)
	return rand_vars

    def return_half_normal_variables(self, location, scale, size=1):
	norm_vars = self.return_normal_variables(location, scale, size)
	half_norm_vars = abs(norm_vars)
	
	return half_norm_vars

    def shuffle_sequence(self, sequence):
	
	randStObj = RandomState(self.seed)
	return randStObj.shuffle(sequence)

    def return_uniform(self, low=0.0, high=1.0, size=1):
	unif_vars = []
	for count in range(size[0]):
	    i = self.seed[count]

	    randStObj = RandomState(i)
	    unif_vars.append(randStObj.uniform(low, high))

	    randStObj = RandomState(i)
	    print 'Repeat 1 ', randStObj.uniform(low, high)
	
	    randStObj = RandomState(i)
	    print 'Repeat 2 ', randStObj.uniform(low, high)
	    raw_input('repeat uniform')
	unif_vars = array(unif_vars)
	return unif_vars




import unittest


class TestRandomDistribution(unittest.TestCase):
    def setUp(self):
        pass
    def testValues(self):
        for i in range(100):
            self.dist1 = RandomDistribution(seed=1)
            self.dist2 = RandomDistribution(seed=1)
            
            
            dist1Vals = self.dist1.return_normal_variables(location=0, scale=1, size=(10000,1))
            dist2Vals = self.dist2.return_normal_variables(location=0, scale=1, size=(10000,1))
            
            pred_diff = all(dist1Vals == dist2Vals)
            if not pred_diff:
                print 'Run:%s' %(i+1)

                print dist1Vals, dist2Vals
            self.assertEquals(True, pred_diff)



if __name__ == '__main__':
    unittest.main()
