from numpy import zeros
from numpy.random.mtrand import RandomState

class RandomDistribution(RandomState):
    def __init__(self, seed):
        RandomState.__init__(self, seed)
        self.seed = seed

    def return_normal_variables(self, location, scale, size):
        if scale == 0:
            return zeros(size) + location
        
        #err = self.normal(size=(3,1))
        #f = open('test_res', 'a')
        #f.write('linearNormal - %s' %self.seed)
        #f.write(str(list(err[:,0])))
        #f.write('\n')
        #f.close()
        
        norm_vars = self.normal(loc=location, 
                                scale=scale, 
                                size=size)

        return norm_vars
        
    def return_random_variables(self, size):
        """"
        err = self.random_sample(size=(3,1))
        f = open('test_res', 'a')
        f.write('RANDOM UNIFORM - %s' %self.seed)
        f.write(str(list(err[:,0])))
        f.write('\n')
        f.close()
        """
        rand_vars = self.random_sample(size)
        return rand_vars

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
