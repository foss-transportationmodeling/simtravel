from scipy import exp

from openamos.core.models.linear_regression_model import LinearRegressionModel

class LogLinearRegressionModel(LinearRegressionModel):
    """
    This is the base class for log-linear regression model in OpenAMOS.
    
    Inputs:
    specification - Specification object
    error_specification - ErrorSpecification object
    """
    
    def __init__(self, specification, error_specification):
        LinearRegressionModel.__init__(self, specification, error_specification)
        
        
    def calc_predvalue(self, data, seed=1):
        """                                                                                                                                 The method returns the predicted value for the different choices in the                                                             specification input.                                                                                                                Inputs:                                                                                                                       
        data - DataArray object                                                                                                             """
        if seed == None:
            raise Exception, "linear"


        expected_value = self.calc_expected_value(data)
        variance = self.error_specification.variance[0,0]
        pred_value = self.calc_errorcomponent(size=(data.rows, 1),
                                              mean=expected_value.data,
                                              sd=variance, seed=seed)
        exp_pred_value = exp(pred_value)
        return DataArray(exp_pred_value, self.specification.choices)

import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.abstract_random_distribution_model import RandomDistribution
from openamos.core.models.error_specification import LinearRegErrorSpecification

class TestLogLinearRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['DURATION']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])
        variance = array([[1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = LinearRegErrorSpecification(variance)


    def testvalues(self):
        model = LogLinearRegressionModel(self.specification, self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        expected_act = self.data.calculate_equation(self.specification.coefficients[0])
        expected_act.shape = (4,1)

        dist = RandomDistribution(seed=1)
        pred_act = exp(dist.return_normal_variables(location=expected_act, scale=1, size=(4,1)))
        
        pred_diff = all(pred_value.data == pred_act)
        self.assertEqual(True, pred_diff)



if __name__ == '__main__':
    unittest.main()

