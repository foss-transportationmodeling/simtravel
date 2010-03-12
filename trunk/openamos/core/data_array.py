from numpy import ndarray, array, zeros
from scipy import exp
import re

from openamos.core.errors import DataError

class DataArray(object):
    def __init__(self, data, varnames):
        if not isinstance(data, ndarray):
            self.data = array(data)
        else:
            self.data = data

        if len(self.data.shape) > 2:
            raise DataError, 'data should be only two dimensional'

        elif len(self.data.shape) == 2:
            self.cols = self.data.shape[-1]

        self.rows = self.data.shape[0] 
            
        if self.cols <> len(varnames):
            raise DataError, """the number of columns in the data """\
                """are not the same as the number of variable names"""

        self._colnames = {}
        
        for i in range(self.cols):
            varname = varnames[i]
            self.check_varname(varname)
            self._colnames[varname.lower()] = i

        self.varnames = [i.lower() for i in varnames]


    def check_varname(self, varname):
        firstchar = str(varname)[0]
        match = re.match('[0-9]', firstchar)
        if match is not None:
            raise DataError, 'variable name is not a valid string - first character is invalid'
        
        if type(varname) is not str:
            raise DataError, 'variable name is not a valid string'


    def calculate_equation(self, coefficients):
        if not isinstance(coefficients, dict):
            raise DataError, 'coefficient input is invalid - should be of dictionary type'

        for i in coefficients.keys():
            if i.lower() not in self._colnames.keys():
                raise DataError, 'coefficient refers to a column not in the dataset'

        for i in coefficients.values():
            try:
                float(i)
            except ValueError, e:
                raise DataError, 'enter valid values for coefficients'

        result = zeros((self.rows,))
        for i in coefficients.keys():
            colnum = self._colnames[i.lower()]
            result += self.data[:,colnum] * coefficients[i]

        return result
    
    def exp_calculate_equation(self, coefficients):
        result = self.calculate_equation(coefficients)
        return exp(result)

    
    def __repr__(self):
        return repr(self.data)

import unittest
from numpy import all

class TestBadInputsDataArray(unittest.TestCase):
    def setUp(self):
        self.data = array([[1, 1.1],[1, 2.]])
        self.data1 = zeros((3,4,1))


        
        self.varnames = ['constant', 'var1']
        self.varnames1 = [1, 'var2']
        self.varnames2 = ['1wer', 'var2']
        self.varnames3 = ['constant', 'var1', 'var2']

        self.coefficients = {'constant':2.0, 'var1':1.5}
        self.coefficients1 = {'constant1':2.0, 'var1':1.5}
        self.coefficients2 = {'constant':'w2.0', 'var1':1.5}

    def testdata(self):
        self.assertRaises(DataError, DataArray, self.data1, self.varnames)

    def testvarnames(self):
        self.assertRaises(DataError, DataArray, self.data, self.varnames1)
        self.assertRaises(DataError, DataArray, self.data, self.varnames2)
        self.assertRaises(DataError, DataArray, self.data, self.varnames3)
        

    def testcoefficients(self):
        data_array = DataArray(self.data, self.varnames)
        self.assertRaises(DataError, data_array.calculate_equation, self.coefficients1)
        self.assertRaises(DataError, data_array.calculate_equation, self.coefficients2)

class TestDataArray(unittest.TestCase):
    def setUp(self):
        self.data = array([[1, 1.1], [1, 2.]])
        self.data1 = [[1, 1.1], [1, 2.]]
        self.varnames = ['constant', 'var1']
        self.coefficients = {'constant':2.0, 'var1':1.5}

        

    def testdata(self):
        data_array = DataArray(self.data1, self.varnames)
        self.assertEqual(type(self.data), type(data_array.data))
        
        self.assertEqual(self.data.shape[0], data_array.rows)
        self.assertEqual(self.data.shape[-1], data_array.cols)

        result = data_array.calculate_equation(self.coefficients)
        result_actual = self.data[:,0] * 2.0 + self.data[:,1] * 1.5
        diff_result = any(result == result_actual)
        self.assertEqual(True, diff_result)
        
        result_exp = data_array.exp_calculate_equation(self.coefficients)
        result_exp_actual = exp(result_actual)
        diff_result = any(result_exp_actual == result_exp)
        self.assertEqual(True, diff_result)
         
        
if __name__ == '__main__':
    unittest.main()
