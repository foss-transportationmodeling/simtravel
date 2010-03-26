from scipy.stats import poisson, nbinom
from numpy import array, zeros, random, all

from openamos.core.models.abstract_model import Model
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.count_regression_model_components import CountSpecification
from openamos.core.errors import SpecificationError

class CountRegressionModel(Model):
    def __init__(self, count_specification, data):
        if not isinstance(count_specification, CountSpecification):
            raise SpecificationError, 'the specification is not a valid CountSpecification object'

        Model.__init__(self, count_specification, data)

        self.distribution = count_specification.distribution

    def calc_expected_value(self):
        return self.data.calculate_equation(self.coefficients[0])

    def calc_probabilities(self):
        #TODO: what are the parameters for the negative binomial distribution
        #[shape_param] = [1,]*nbinom.numargs
        expected_value = self.calc_expected_value()
        num_choices = self.specification.number_choices
        probabilities = zeros((self.data.rows, num_choices))
        for i in range(num_choices-1):
            if self.distribution == 'poisson':
                probabilities[:,i] = poisson.pmf(i, expected_value)
            else:
                #TODO: implement negative binomial probabilities
                pass

        if self.distribution == 'poisson':
            probabilities[:,-1] = 1 - probabilities.cumsum(-1)[:,-1]
        else:
            #TODO: implement negative binomial probabilities
            pass
        return probabilities

    def calc_chosenalternative(self):
        probabilities = DataArray(self.calc_probabilities(), self.specification.choices)
        prob_model = AbstractProbabilityModel(probabilities, self.specification.seed)
        return prob_model.selected_choice()
        

import unittest
from openamos.core.data_array import DataArray

class TestBadInputCountRegressionModel(unittest.TestCase):
    def setUp(self):
        choices = ['Episodes1', 'Episodes2', 'Episodes3']
        coefficients = [{'Constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data = DataArray(data, ['CONSTANT', 'VAR1'])
        
        self.specification = CountSpecification(choices, coefficients)
        self.specification1 = [choices, coefficients]

    def testspecification(self):
        self.assertRaises(SpecificationError, CountRegressionModel, self.specification1,
                          self.data)



class TestCountRegressionModel(unittest.TestCase):
    def setUp(self):
        choices = ['Episodes1', 'Episodes2', 'Episodes3']
        self.coefficients = [{'Constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data = DataArray(data, ['CONSTANT', 'VAR1'])
        
        self.specification = CountSpecification(choices, self.coefficients)
        self.model = CountRegressionModel(self.specification, self.data)
        
    def testprobabilitiespoisson(self):
        prob = zeros((4,3))
        exp_value = self.data.calculate_equation(self.coefficients[0])
        prob[:,0] = poisson.pmf(0, exp_value)
        prob[:,1] = poisson.pmf(1, exp_value)
        prob[:,2] = 1 - poisson.cdf(1, exp_value)

        prob_model = self.model.calc_probabilities()
        prob_diff = all(prob == prob_model)
        self.assertEqual(True, prob_diff)

    def testselectionpoisson(self):
        choice_act = array([['episodes3'], ['episodes3'], ['episodes1'], ['episodes2']])
        choice_model = self.model.calc_chosenalternative()
        choice_diff = all(choice_act == choice_model)
        self.assertEqual(True, choice_diff)

if __name__ == '__main__':
    unittest.main()
