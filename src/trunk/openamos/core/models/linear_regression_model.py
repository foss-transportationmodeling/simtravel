from scipy.stats import norm
from numpy import random, all
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.errors import ErrorSpecificationError

class LinearRegressionModel(AbstractRegressionModel):
    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(self, specification, error_specification)

        if not isinstance(error_specification, LinearRegErrorSpecification):
            raise ErrorSpecificationError, """incorrect error specification; it """\
                """should be LinearRegErrroSpecification object"""        

        self.seed = self.specification.seed
        random.seed(self.seed)

    def calc_errorcomponent(self, size, mean=0, sd=1):
        return norm.rvs(loc=mean, scale=sd, 
                        size=size)

    def calc_predvalue(self, data):
        expected_value = self.calc_expected_value(data)
        variance = self.error_specification.variance[0,0]
        pred_value = self.calc_errorcomponent(size=(data.rows, 1),
                                              mean=expected_value.data, sd=variance)
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

        random.seed(1)
        expected_act = self.data.calculate_equation(
                                                    self.specification.coefficients[0])
        expected_act.shape = (4,1)
        pred_act = norm.rvs(loc=expected_act, scale=1, size=(4,1))

        pred_diff = all(pred_value.data == pred_act)
        self.assertEqual(True, pred_diff)

                        
        
if __name__ == '__main__':
    unittest.main()
