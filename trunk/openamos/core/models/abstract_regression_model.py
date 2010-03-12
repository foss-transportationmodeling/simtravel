from numpy import all, array, zeros
from scipy import exp
from openamos.core.models.abstract_model import Model
from openamos.core.errors import SpecificationError, ErrorSpecificationError

class AbstractRegressionModel(Model):
    def __init__(self, specification, data, error_specification):
        Model.__init__(self, specification, data)
        
        self.error_specification = error_specification

        if specification.number_choices > 1:
            raise SpecificationError, """invalid specification for regression model only"""\
                """ one equation needs to be specified"""

        if not isinstance(self.error_specification, ErrorSpecification):
            raise ErrorSpecificationError, """invalid error specification"""\
                """ it should be of type ErrorSpecification"""
        
        if self.error_specification.num_err_components > 1:
            raise ErrorSpecificationError, """invalid error specification for regression model only"""\
                """ one error component needs to be specified"""

    def calc_expected_value(self):
        return self.calculate_expected_values()

    def calc_exp_expected_value(self):
        return self.calculate_exp_expected_values()

    def calc_errorcomponent(self):
        raise Exception('method not implemented')

    def calc_predvalue(self):
        raise Exception('method not implemented')


import unittest
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification, ErrorSpecification


class TestBadSpecificationRegressionModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])        

        variance = array([[1.1]])
        variance1 = array([[1.1, 1.2], [2.1, 2.2]])
        
        self.data = DataArray(data, ['Constant', 'VAR1'])

        self.specification = Specification(choices, coefficients)

        self.errorspecification = ErrorSpecification(variance)
        self.errorspecification1 = ErrorSpecification(variance1)

    def testtwodependentvars(self):
        self.assertRaises(SpecificationError, AbstractRegressionModel, self.specification,
                          self.data, self.errorspecification)

    def testtwoerrorcomponents(self):
        self.assertRaises(SpecificationError, AbstractRegressionModel, self.specification, 
                          self.data, self.errorspecification1)


class TestAbstractRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['SOV']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])       
        variance = array([[1.1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = ErrorSpecification(variance)        


    def testvalues(self):
        model = AbstractRegressionModel(self.specification, self.data, self.errorspecification)

        model_expected_values = model.calc_expected_value()
        expected_act = zeros((self.data.rows, 1))
        expected_act[:,0] = self.data.data[:,0] * 2 + self.data.data[:,1] * 2.11
        expected_diff = all(expected_act == model_expected_values.data)
        self.assertEqual(True, expected_diff)

        exp_expected_act = exp(expected_act)
        model_exp_expected_values = model.calc_exp_expected_value()
        exp_expected_diff = all(exp_expected_act == model_exp_expected_values.data)
        self.assertEqual(True, exp_expected_diff)
        
                        
    def testerrorspecification(self):
        pass
        

if __name__ == '__main__':
    unittest.main()
