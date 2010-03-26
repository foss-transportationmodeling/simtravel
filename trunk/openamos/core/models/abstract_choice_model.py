from numpy import all, array, zeros
from scipy import exp
from openamos.core.models.abstract_model import Model
from openamos.core.errors import DataError

class AbstractChoiceModel(Model):
    def __init__(self, specification, data, choiceset=None):
        Model.__init__(self, specification, data)

        if choiceset is None:
            self.choiceset = DataArray(array([]),[])
            #self.choiceset = array([])
        else:
            self.choiceset = choiceset

        if not isinstance(self.choiceset, DataArray):
            raise DataError, 'the choiceset data is not a valid DataArray object'


        if choiceset is not None:
            if choiceset.rows <> self.data.rows:
                raise DataError, 'the number of rows in the choiceset is not consistent with the data array'

            if (self.choiceset.data == 0).sum() + (self.choiceset.data == 1).sum() <> self.choiceset.data.size:
                raise DataError, 'choiceset is invalid, elements must be of either bool type or numbers - 0/1 only'
            
            #if self.choiceset.cols <> self.specification.number_choices:
            #    raise DataError, """size of choiceset is not consistent with the number """\
            #        """of choices provided in the specification"""

            if not all(self.choiceset.data.cumsum(-1)[:,-1] > 0):
                raise DataError, """choiceset implies agents with no choices, atleast one """\
                    """choice should be available to each agent"""

    def calc_observed_utilities(self):
        return self.calculate_expected_values()

    def validchoiceutilities(self):
        raise Exception('method not implemented')

    def calc_exp_choice_utilities(self):
        return self.calculate_exp_expected_values()

    def calc_probabilities(self):
        raise Exception('method not implemented')

    def calc_chosenalternative(self):
        raise Exception('method not implemented')


import unittest
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification

class TestBadInputAbstractChoiceModel(unittest.TestCase):
    def setUp(self):
        choice = ['SOV']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])        

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.data1 = data
        self.specification = Specification(choice, coefficients)

    def testdatatype(self):
        self.assertRaises(DataError, AbstractChoiceModel, self.specification, self.data1)


class TestAbstractChoiceModel(unittest.TestCase):
    def setUp(self):
        choice = ['SOV']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])        

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        
    def testvalues(self):
        model = AbstractChoiceModel(self.specification, self.data)

        model_expected_values = model.calc_observed_utilities()
        expected_act = zeros((self.data.rows, 1))
        expected_act[:,0] = self.data.data[:,0] * 2 + self.data.data[:,1] * 2.11
        expected_diff = all(expected_act == model_expected_values.data)
        self.assertEqual(True, expected_diff)

        exp_expected_act = exp(expected_act)
        model_exp_expected_values = model.calc_exp_choice_utilities()
        exp_expected_diff = all(exp_expected_act == model_exp_expected_values.data)
        self.assertEqual(True, exp_expected_diff)
        
        
                        



if __name__ == '__main__':
    unittest.main()
