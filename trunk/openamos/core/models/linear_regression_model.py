from scipy.stats import norm
from numpy import random
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.errors import ErrorSpecificationError

class LinearRegressionModel(AbstractRegressionModel):
    def __init__(self, specification, data, error_specification):
        AbstractRegressionModel.__init__(self, specification, data, error_specification)

        if self.error_specification.distribution <> 'normal':
            raise ErrorSpecificationError, """incorrect error specification distribution """\
                """for linear regression model; supported error specification is normal distribution"""

        self.seed = self.specification.seed
        random.seed(self.seed)

    def calc_errorcomponent(self, size, mean=0, sd=1):
        return norm.rvs(loc=mean, scale=sd, 
                        size=(self.data.rows, 1))

    def calc_predvalue(self):
        expected_value = self.calc_expected_value()
        variance = self.error_specification.variance[0,0]
        pred_value = self.calc_errorcomponent(size=(self.data.rows, 1),
                                              mean=expected_value.data, sd=variance)
        return DataArray(pred_value, self.specification.choices)

    
import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification, ErrorSpecification

class TestLinearRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['DURATION']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])       
        variance = array([[1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = ErrorSpecification(variance)        


    def testvalues(self):
        model = LinearRegressionModel(self.specification, self.data, self.errorspecification)

        pred_value = model.calc_predvalue()
        
                        
        
if __name__ == '__main__':
    unittest.main()
