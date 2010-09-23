from numpy import zeros
from numpy.random.mtrand import RandomState

class RandomDistribution(RandomState):
    def __init__(self, seed):
        RandomState.__init__(self, seed)
        self.seed = seed

    def return_normal_variables(self, location, scale, size):
        if scale == 0:
            return zeros(size) + location

        err = self.normal(size=(3,1))
        f = open('test_res', 'a')
        f.write('linearNormal - %s' %self.seed)
        f.write(str(list(err[:,0])))
        f.write('\n')
        f.close()

        norm_vars = self.normal(loc=location, 
                                scale=scale, 
                                size=size)

        return norm_vars
        
    def return_random_variables(self, size):
        err = self.random_sample(size=(3,1))
        f = open('test_res', 'a')
        f.write('RANDOM UNIFORM - %s' %self.seed)
        f.write(str(list(err[:,0])))
        f.write('\n')
        f.close()
        rand_vars = self.random_sample(size)
        return rand_vars
