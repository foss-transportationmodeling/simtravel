from scipy.stats import genlogistic, norm
from numpy import array, zeros, random, all

from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.ordered_choice_model_components import OLSpecification
from openamos.core.errors import SpecificationError


class OrderedModel(AbstractChoiceModel):
    def __init__(self, ol_specification, data):
        AbstractChoiceModel.__init__(self, ol_specification, data)
        
        if not isinstance(ol_specification, OLSpecification):
            raise SpecificationError, 'the specification is not a valid OLSpecification object'

        self.thresholds = ol_specification.thresholds
        self.distribution = ol_specification.distribution

    def calc_observed_utilities(self):
        return self.data.calculate_equation(self.coefficients[0])

    def calc_probabilities(self):
        [shape_param] = [1,]*genlogistic.numargs
        observed_utility = self.calc_observed_utilities()
        num_choices = self.specification.number_choices
        probabilities = zeros((self.data.rows, num_choices))
        lower_bin = 0
        for i in range(num_choices-1):
            value = self.thresholds[i] - observed_utility
            if self.distribution == 'logit':
                upper_bin = genlogistic.cdf(value, shape_param)
            else:
                upper_bin = norm.cdf(value)
            
            probabilities[:,i] = upper_bin - lower_bin
            lower_bin = upper_bin

        probabilities[:,i+1] = 1 - upper_bin
        return probabilities

    def calc_chosenalternative(self):
        probabilities = self.calc_probabilities()
        prob_model = AbstractProbabilityModel(probabilities, self.specification.seed)
        return prob_model.selected_choice()
        

import unittest
from openamos.core.data_array import DataArray


class TestBadInputOrderedProbitModel(unittest.TestCase):
    def setUp(self):
        choices = ['Veh1', 'Veh2', 'Veh3']
        coefficients = [{'Constant':2, 'Var1':2.11}]
        thresholds = [1.2, 2.1]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data = DataArray(data, ['CONSTANT', 'VAR1'])
        
        self.specification = OLSpecification(choices, coefficients, thresholds)
        self.specification1 = [choices, coefficients, thresholds]

    def testolspecification(self):
        self.assertRaises(SpecificationError, OrderedModel, self.specification1,
                          self.data)

class TestOrderedProbitModel(unittest.TestCase):
    def setUp(self):
        choices = ['Veh1', 'Veh2', 'Veh3']
        self.coefficients = [{'Constant':2, 'Var1':2.11}]
        self.thresholds = [1.2, 2.1]
        self.data = DataArray(array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]]), 
                         ['CONSTANT', 'VAR1'])
        
        specification = OLSpecification(choices, self.coefficients, self.thresholds)
        self.model = OrderedModel(specification, self.data)

        specification1 = OLSpecification(choices, self.coefficients, self.thresholds, distribution='probit')
        self.model1 = OrderedModel(specification1, self.data)
        

        

    def testprobabilitieslogit(self):
        prob = zeros((4,3))
        obs_utility = self.data.calculate_equation(self.coefficients[0])
        [shape_param] = [1,]*genlogistic.numargs
        prob[:,0] = genlogistic.cdf(self.thresholds[0] - obs_utility, shape_param)
        prob[:,1] = (genlogistic.cdf(self.thresholds[1] - obs_utility, shape_param) - 
                     genlogistic.cdf(self.thresholds[0] - obs_utility, shape_param))
        prob[:,2] = 1 - genlogistic.cdf(self.thresholds[1] - obs_utility, shape_param)

        prob_model = self.model.calc_probabilities()
        prob_diff = all(prob == prob_model)
        self.assertEqual(True, prob_diff)

    def testselectionlogit(self):
        choice_act = array([[3], [3], [1], [1]])
        choice_model = self.model.calc_chosenalternative()
        choice_diff = all(choice_act == choice_model.data)
        self.assertEqual(True, choice_diff)

    def testprobabilitiesprobit(self):
        prob = zeros((4,3))
        obs_utility = self.data.calculate_equation(self.coefficients[0])
        prob[:,0] = norm.cdf(self.thresholds[0] - obs_utility)
        prob[:,1] = (norm.cdf(self.thresholds[1] - obs_utility) - 
                     norm.cdf(self.thresholds[0] - obs_utility))
        prob[:,2] = 1 - norm.cdf(self.thresholds[1] - obs_utility)

        prob_model = self.model1.calc_probabilities()
        prob_diff = all(prob == prob_model)
        self.assertEqual(True, prob_diff)

    def testselectionlogit(self):
        choice_act = array([[3], [2], [3], [2]])
        choice_model = self.model1.calc_chosenalternative()
        choice_diff = all(choice_act == choice_model.data)
        self.assertEqual(True, choice_diff)
        
if __name__ == '__main__':
    unittest.main()

    

