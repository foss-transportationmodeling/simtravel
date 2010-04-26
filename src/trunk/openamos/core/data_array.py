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
            
        else:
            self.cols = 0
            
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
            raise DataError, """variable name is not a valid string - first """\
                """character is invalid"""
        
        if type(varname) is not str:
            raise DataError, 'variable name is not a valid string'


    def calculate_equation(self, coefficients, rows=None):
        if not isinstance(coefficients, dict):
            raise DataError, """coefficient input is invalid - should be of """\
                """dictionary type"""

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
        
        if rows is not None:
            return result[rows]
        return result
    
    def exp_calculate_equation(self, coefficients):
        result = self.calculate_equation(coefficients)
        return exp(result)

    
    def __repr__(self):
        return repr(self.data)

    def column(self, columname):
        self.check_varname(columname)
        if not isinstance(columname, str):
            raise DataError, 'not a valid column name'
        try:
            colnum = self._colnames[columname.lower()]
            return self.data[:,colnum]
        except KeyError, e:
            raise DataError, 'not a recognized column name'

    def setcolumn(self, columname, values, rows=None):
        
        
        if len(values.shape) > 1:
            #converting the array to one dimensional
            values.shape = (values.shape[0],)

        self.check_varname(columname)
        colnum = self._colnames[columname.lower()]
        try:
            if rows is None:
                self.data[:,colnum] = values
            else:
                self.data[rows,colnum] = values
        except ValueError, e:
            raise DataError, e
        
    def scaledowncolumn(self, columname, scale):
        self.check_varname(columname)
        if type(scale) not in [int, float]:
            raise DataError, 'the scale values is not a valid number'
        colnum = self._colnames[columname.lower()]
        self.data[:,colnum] = self.data[:,colnum]/scale

    def addtocolumn(self, columname, values):
        self.check_varname(columname)
        colnum = self._colnames[columname.lower()]
        try:
            self.data[:,colnum] = self.data[:,colnum] + values
        except ValueError, e:
            raise DataError, e

    def expofcolumn(self, columname):
        self.check_varname(columname)
        colnum = self._colnames[columname.lower()]
        try:
            self.data[:,colnum] = exp(self.data[:,colnum])
        except ValueError, e:
            raise DataError, e


    def columns(self, columnames, rows=None):
        """
        the method retrieves and returns a dataarray of columnames that 
        were passed to the method. 
        """
        if not isinstance(columnames, list):
            return DataError, """the column names input should be a list"""\
                """ of variable names"""
        
        for i in columnames:
            self.check_varname(i)

        columnums = []
        for i in columnames:
            try:
                columnums.append(self._colnames[i.lower()])
            except KeyError, e:
                raise DataError, '%s not a recognized column name' %i

        if rows is not None:
            return DataArray(self.data[rows,:][:,columnums], columnames)
        return DataArray(self.data[:,columnums], columnames)

    def rowsof(self, rows):
        """
        the method retrieves and returns a dataarray of rows that 
        were passed to the method.
        """
        
        if isinstance(rows, ndarray):
            if rows.size <> self.rows:
                raise DataError, """the number of rows is inconsistent with """\
                    """the number of rows in the data"""
            if len(rows.shape) > 1:
                rows = array([i[0] for i in rows])

        rows_type = type(rows)
        if rows_type in [tuple, list]:
            if len(rows) <> self.rows:
                raise DataError, """the number of rows is inconsistent with """\
                    """the number of rows in the data"""
            rows = array(rows)
        
        return DataArray(self.data[rows,:], self.varnames)


    def __lt__(self, value):
        return self.data < value

    def __gt__(self, value):
        return self.data > value

    def __le__(self, value):
        return self.data <= value

    def __ge__(self, value):
        return self.data >= value

    def __eq__(self, value):
        return self.data == value

    def __ne__(self, value):
        return self.data <> value


class DataFilter(object):
    def __init__(self, varname, filter_string, value, coefficients=None):
        
        if not isinstance(varname, str):
            raise DataError, """variable input has to be a valid """\
                """ string object"""
        self.varname = varname
        
        if not isinstance(filter_string, str):
            raise DataError, """the data filter string has to be a valid """\
                """ string object"""

        self.filter_string = filter_string

        value_type = type(value)

        if not value_type in [int, float]:
            raise DataError, """the value has to be a valid numeric object; """\
                """only 'float' and 'int' objects are accepted"""
        self.value = value


        if not isinstance(coefficients, dict) and coefficients is not None:
            raise DataError, """coefficient input is invalid - should be of """\
                """dictionary type"""

        self.coefficients = coefficients

    def compare(self, data):
        if self.filter_string == 'less than':
            valid_rows = data.columns([self.varname]) < self.value
            
        if self.filter_string == 'greater than':
            valid_rows = data.columns([self.varname]) > self.value

        if self.filter_string == 'less than equals':
            valid_rows = data.columns([self.varname]) <= self.value

        if self.filter_string == 'greater than equals':
            valid_rows = data.columns([self.varname]) >= self.value

        if self.filter_string == 'equals':
            valid_rows = data.columns([self.varname]) == self.value

        if self.filter_string == 'not equals':
            valid_rows = data.columns([self.varname]) <> self.value

        #return data.rowsof(valid_rows)
        valid_rows.shape = (valid_rows.shape[0], )
        return valid_rows            


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
        self.assertRaises(DataError, data_array.calculate_equation, 
                          self.coefficients1)
        self.assertRaises(DataError, data_array.calculate_equation, 
                          self.coefficients2)

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

    def testretrievecolumns(self):
        data_array = DataArray(self.data1, self.varnames)
        columnames = ['Var1', 'constant']
        result = data_array.columns(columnames)

        columnames_lower = [i.lower() for i in columnames]
        self.assertEqual(columnames_lower, result.varnames)
        
        rows = data_array.columns(['constant']) == 2
        result = data_array.rowsof(rows)
        print result.varnames
        print result.data.shape[0]

        
if __name__ == '__main__':
    unittest.main()
