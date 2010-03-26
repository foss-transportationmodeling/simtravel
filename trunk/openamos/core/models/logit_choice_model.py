from numpy import ma, float32, dtype, ndarray, array, all, any
from scipy import exp
from openamos.core.models.model_components import Specification
from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.errors import DataError, SpecificationError

class LogitChoiceModel(AbstractChoiceModel):
    def __init__(self, specification, data, choiceset=None):
        if not isinstance(specification, Specification):
            raise SpecificationError, 'the specification input is not a valid Specification object'
        AbstractChoiceModel.__init__(self, specification, data, choiceset)

        
    def calc_observed_utilities(self):
        values = self.calculate_expected_values()
        values.data = ma.array(values.data)
        return values

    def validchoiceutilities(self):
        valid_values = self.calc_observed_utilities()
        for i in self.choiceset.varnames:
            mask = self.choiceset.column(i) == 0
            if any(mask == True):
                valid_values.setcolumn(i, ma.masked, mask)
        return valid_values


    def calc_exp_choice_utilities(self):
        values = self.validchoiceutilities()
        values.data = exp(values.data)
        return values

    def calc_probabilities(self):
        exp_expected_utilities = self.calc_exp_choice_utilities()
        exp_utility_sum = exp_expected_utilities.data.cumsum(-1)
        exp_utility_sum_max = exp_utility_sum.max(-1)
        probabilities = (exp_expected_utilities.data.transpose()/exp_utility_sum_max).transpose()
        return probabilities
        
    def calc_chosenalternative(self):
        probabilities = DataArray(self.calc_probabilities(), self.specification.choices)
        prob_model = AbstractProbabilityModel(probabilities, self.specification.seed)
        return prob_model.selected_choice()

import unittest
from numpy import zeros
from openamos.core.data_array import DataArray
class TestBadInputLogitChoiceModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.choiceset1 = DataArray(ma.array([[0,1],[1, 'we']]), ['first', 'second'])
        self.choiceset2 = DataArray(ma.array([[0,2], [2,3]]), ['first', 'second'])
        self.choiceset3 = DataArray(array([[0,0], [1,1]]), ['first', 'second'])


        self.data = DataArray(data, ['Constant','Var1'])
        self.specification = Specification(choices, coefficients)
        self.specification1 = (choices, coefficients)

    def testchoicesetvalidentries(self):
        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset1)

        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset2)

        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset3)

    def testspecificationvalidtype(self):
        self.assertRaises(SpecificationError, LogitChoiceModel, self.specification1, self.data, self.choiceset3)


class TestLogitChoiceModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.choiceset1 = DataArray(ma.array([[0, 1], [0, 1], [1, 1], [1, 1]]), ['SOV', 'HOV'])

        self.data = DataArray(data, ['Constant','Var1'])
        self.specification = Specification(choices, coefficients)

        self.utils_array_act = zeros((self.data.rows,self.specification.number_choices))
        self.utils_array_act[:,0] = self.data.data[:,0]*2 + self.data.data[:,1]*2.11
        self.utils_array_act[:,1] = self.data.data[:,0]*1.2
        self.exp_utils_array_act = exp(self.utils_array_act)
        self.prob_array_act = (self.exp_utils_array_act.transpose()/self.exp_utils_array_act.cumsum(-1)[:,-1]).transpose()
        
        # for the selected data, and seed = 1, chosen alternatives are
        self.selected_act = array([['sov'], ['hov'], ['sov'], ['sov']])
        self.selected_act1 = array([['hov'], ['hov'], ['sov'], ['sov']])
        

    def testmodelresults(self):
        model = LogitChoiceModel(self.specification, self.data)
        probabilities_model = model.calc_probabilities()
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative()
        selected_diff = all(self.selected_act == selected_model)
        self.assertEqual(True, selected_diff)

        
    def testmodelresultswithchoicesets(self):
        model = LogitChoiceModel(self.specification, self.data, self.choiceset1)
        probabilities_model = model.calc_probabilities()

        # Calculating actual values with mask included and then compare it against outputs from model
        mask = self.choiceset1.data == 0
        self.exp_utils_array_act[mask] = ma.masked
        self.prob_array_act = (self.exp_utils_array_act.transpose()/self.exp_utils_array_act.cumsum(-1)[:,-1]).transpose()
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative()
        selected_diff = all(self.selected_act1 == selected_model)
        self.assertEqual(True, selected_diff)



if __name__ == '__main__':
    unittest.main()
