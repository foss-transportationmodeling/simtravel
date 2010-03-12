from numpy import ma, float32, dtype, ndarray, array, all, any
from scipy import exp
from openamos.core.models.abstract_choice_model import AbstractChoiceModel
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.errors import DataError

class LogitChoiceModel(AbstractChoiceModel):
    def __init__(self, specification, data, choiceset=None):
        AbstractChoiceModel.__init__(self, specification, data)

        if choiceset is None:
            self.choiceset = array([])
        else:
            self.choiceset = choiceset
            if choiceset.shape[0] <> self.data.rows:
                raise DataError, 'the number of rows in the choiceset is not consistent with the data array'

        if not isinstance(self.choiceset, ndarray):
            raise DataError, 'the choiceset data is not a valid entry'

        choiceset_type = self.choiceset.dtype
        if choiceset_type not in [int, float]:
            raise DataError, 'the choiceset contains string entries'

        if choiceset is not None:
            if (self.choiceset == 0).sum() + (self.choiceset == 1).sum() <> self.choiceset.size:
                raise DataError, 'choiceset is invalid, elements must be of either bool type or numbers - 0/1 only'
        
            if self.choiceset.shape[-1] <> self.specification.number_choices:
                raise DataError, """size of choiceset is not consistent with the number """\
                    """of choices provided in the specification"""

            if not all(self.choiceset.cumsum(-1)[:,-1] > 0):
                raise DataError, """choiceset implies agents with no choices, atleast one """\
                    """choice should be available to each agent"""

        
    def calc_observed_utilities(self):
        values = self.calculate_expected_values()
        values.data = ma.array(values.data)
        return values


    def calc_exp_observed_utilities(self):
        exp_values = self.calculate_exp_expected_values()
        exp_values.data = ma.array(exp_values.data)
        return exp_values

    def validchoiceutilities(self):
        # creating a valid choices set based on a indicator matrix choiceset
        expected_utilities = self.calc_observed_utilities()
        mask = self.choiceset == 0

        if any(mask == True):
            expected_utilities.data[mask] = ma.masked
        return expected_utilities

        
    def validexpchoiceutilities(self):
        exp_expected_utilities = self.calc_exp_observed_utilities()
        mask = self.choiceset == 0

        if any(mask == True):
            exp_expected_utilities.data[mask] = ma.masked
        return exp_expected_utilities


    def calc_probabilities(self):
        exp_expected_utilities = self.validexpchoiceutilities()
        exp_utility_sum = exp_expected_utilities.data.cumsum(-1)
        exp_utility_sum_max = exp_utility_sum.max(-1)
        probabilities = (exp_expected_utilities.data.transpose()/exp_utility_sum_max).transpose()
        return probabilities
        


    def calc_chosenalternative(self):
        probabilities = self.calc_probabilities()
        prob_model = AbstractProbabilityModel(probabilities, self.specification.seed)
        return prob_model.selected_choice()


import unittest
from numpy import zeros
from openamos.core.models.model_components import Specification
from openamos.core.data_array import DataArray
class TestBadInputLogitChoiceModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.choiceset1 = ma.array([[0,1],[1, 'we']])
        self.choiceset2 = ma.array([[0,2], [2,3]])
        self.choiceset3 = array([[0,0], [1,1]])


        self.data = DataArray(data, ['Constant','Var1'])
        self.specification = Specification(choices, coefficients)

    def testchoicesetvalidentries(self):
        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset1)

        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset2)

        self.assertRaises(DataError, LogitChoiceModel, self.specification, self.data, self.choiceset3)


class TestLogitChoiceModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])

        self.choiceset1 = ma.array([[0, 1], [0, 1], [1, 1], [1, 1]])

        self.data = DataArray(data, ['Constant','Var1'])
        self.specification = Specification(choices, coefficients)

        self.utils_array_act = zeros((self.data.rows,self.specification.number_choices))
        self.utils_array_act[:,0] = self.data.data[:,0]*2 + self.data.data[:,1]*2.11
        self.utils_array_act[:,1] = self.data.data[:,0]*1.2
        self.exp_utils_array_act = exp(self.utils_array_act)
        self.prob_array_act = (self.exp_utils_array_act.transpose()/self.exp_utils_array_act.cumsum(-1)[:,-1]).transpose()
        
        # for the selected data, and seed = 1, chosen alternatives are
        self.selected_act = array([[1], [2], [1], [1]])
        self.selected_act1 = array([[2], [2], [1], [1]])
        

    def testmodelresults(self):
        model = LogitChoiceModel(self.specification, self.data)
        probabilities_model = model.calc_probabilities()
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative()
        selected_diff = all(self.selected_act == selected_model.data)
        self.assertEqual(True, selected_diff)

        
    def testmodelresultswithchoicesets(self):
        model = LogitChoiceModel(self.specification, self.data, self.choiceset1)
        probabilities_model = model.calc_probabilities()

        # Calculating actual values with mask included and then compare it against outputs from model
        mask = self.choiceset1 == 0
        self.exp_utils_array_act[mask] = ma.masked
        self.prob_array_act = (self.exp_utils_array_act.transpose()/self.exp_utils_array_act.cumsum(-1)[:,-1]).transpose()
        probabilities_diff = all(self.prob_array_act == probabilities_model)
        self.assertEqual(True, probabilities_diff)

        selected_model = model.calc_chosenalternative()
        selected_diff = all(self.selected_act1 == selected_model.data)
        self.assertEqual(True, selected_diff)



if __name__ == '__main__':
    unittest.main()
