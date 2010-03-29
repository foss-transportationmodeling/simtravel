from numpy import zeros, ndarray
from scipy import exp
from openamos.core.errors import DataError, SpecificationError
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification

class Model(object):
    def __init__(self, specification, data):
        self.specification = specification
        self.data = data

        if not isinstance(self.data, DataArray):
            raise DataError, 'data input is not a valid DataArray object'


        self.choices = self.specification.choices
        self.coefficients = self.specification.coefficients
        self.check()


    def check(self):
        self.unique_variable_names()


    def unique_variable_names(self):
        unique_variables = []
        for i in self.coefficients:
            for j in i.keys():
                if not j in unique_variables:
                    unique_variables.append(j.lower())
                    
        for i in unique_variables:
            if i not in self.data.varnames:
                raise DataError, 'data incomplete; %s variable not found in the data' %i

    def calculate_expected_values(self):
        num_choices = self.specification.number_choices
        expected_value_array = DataArray(zeros((self.data.rows, num_choices)), 
                                         self.choices)

        for i in range(num_choices):
            coefficients = self.coefficients[i]
            expected_value_array.data[:,i] = self.data.calculate_equation(coefficients)

        return expected_value_array
    

    def calculate_exp_expected_values(self):
        expected_values = self.calculate_expected_values()
        expected_values.data = exp(expected_values.data)
        return expected_values
        

import unittest
from numpy import array, all


class TestBadInputsModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']

        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]
        coefficients1 = [{'Constant':2, 'Var1':2.11, 'Var2':3.27}, {'Constant':1.2}]

        self.data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        self.data2 = DataArray(array([[1, 1.1], [1, -0.25]]), ['Constant', 'Var1'])

        self.specification = Specification(choices, coefficients1)

    def testdatatype(self):
        self.assertRaises(DataError, Model, self.specification, self.data)

    def testdataarraycolnames(self):
        self.assertRaises(DataError, Model, self.specification, self.data2)




class TestAbstractModel(unittest.TestCase):
    def setUp(self):
        choices = ['SOV', 'HOV']
        variables = [['Constant', 'Var1'], ['Constant']]
        coefficients = [{'Constant':2, 'Var1':2.11}, {'Constant':1.2}]

        self.data = DataArray(array([[1, 1.1], [1, -0.25]]), ['Constant', 'Var1'])
        self.specification = Specification(choices, coefficients)
        self.model = Model(self.specification, self.data)
        

    def testexpectedvalue(self):
        value_array_act = zeros((self.data.rows,self.specification.number_choices))
        value_array_act[:,0] = self.data.data[:,0]*2 + self.data.data[:,1]*2.11
        value_array_act[:,1] = self.data.data[:,0]*1.2

        expected_value_array = self.model.calculate_expected_values()
        self.assertEqual(True, isinstance(expected_value_array, DataArray))
        self.assertEqual(self.specification.choices, expected_value_array.varnames)
        diff_values = all(value_array_act == expected_value_array.data)
        self.assertEqual(True, diff_values)

        exp_expected_value_array = self.model.calculate_exp_expected_values()
        self.assertEqual(True, isinstance(exp_expected_value_array, DataArray))
        self.assertEqual(self.specification.choices, exp_expected_value_array.varnames)
        diff_values = all(exp(value_array_act) == exp_expected_value_array.data)
        self.assertEqual(True, diff_values)

if __name__ == '__main__':
    unittest.main()
