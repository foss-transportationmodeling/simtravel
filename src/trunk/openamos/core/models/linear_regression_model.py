from scipy.stats import norm
from numpy import random, all
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.models.abstract_random_distribution_model import RandomDistribution
from openamos.core.errors import ErrorSpecificationError

class LinearRegressionModel(AbstractRegressionModel):
    """
    This is the base class for linear regression model in OpenAMOS.
    
    Inputs:
    specification - Specification object
    error_specification - ErrorSpecification object
    """
    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(self, specification, error_specification)

        if not isinstance(error_specification, LinearRegErrorSpecification):
            raise ErrorSpecificationError, """incorrect error specification; it """\
                """should be LinearRegErrroSpecification object"""        

    def calc_errorcomponent(self, size, mean=0, sd=1, seed=1):
        """
        The method returns the contribution of the error in the calculation 
        of the predicted value for the different choices.
        
        Inputs:
        size - numeric value (number of rows)
        mean - numeric value (mean)
        sd - numeric value (standard deviation)
        """
        dist = RandomDistribution(seed=seed)
        err_norm = dist.return_normal_variables(location=mean, scale=sd, size=size)
        return err_norm

    def calc_predvalue(self, data, seed=1):
        """
        The method returns the predicted value for the different choices in the 
        specification input.
        
        Inputs:
        data - DataArray object
        """
        if seed == None:
            raise Exception, "linear"


        expected_value = self.calc_expected_value(data)
        variance = self.error_specification.variance[0,0]
        pred_value = self.calc_errorcomponent(size=(data.rows, 1),
                                              mean=expected_value.data, 
                                              sd=variance, seed=seed)
        return DataArray(pred_value, self.specification.choices)

    
import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import LinearRegErrorSpecification

class TestLinearRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['DURATION']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])       
        variance = array([[1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = LinearRegErrorSpecification(variance)        


    def testvalues(self):
        model = LinearRegressionModel(self.specification, self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        expected_act = self.data.calculate_equation(
                                                    self.specification.coefficients[0])
        expected_act.shape = (4,1)
        pred_act = norm.rvs(loc=expected_act, scale=1, size=(4,1))

        pred_diff = all(pred_value.data == pred_act)
        self.assertEqual(True, pred_diff)

                        
        
if __name__ == '__main__':
    unittest.main()
