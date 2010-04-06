from scipy.stats import norm, halfnorm
from numpy import random
from openamos.core.models.abstract_regression_model import AbstractRegressionModel
from openamos.core.errors import ErrorSpecificationError

class StocFronRegressionModel(AbstractRegressionModel):
    def __init__(self, specification, error_specification):
        AbstractRegressionModel.__init__(self, specification, error_specification)
        
        if not isinstance(error_specification, StochasticRegErrorSpecification):
            raise ErrorSpecification, """incorrect error specification; it should be """\
                """StochasticRegErrroSpecification object"""

        self.seed = self.specification.seed
        random.seed(self.seed)

    def calc_errorcomponent(self, variance_norm, variance_halfnorm, vertex, size):
        err_norm = norm.rvs(scale=variance_norm, size=size)
        err_halfnorm = halfnorm.rvs(scale=variance_halfnorm, size=size)
        
        if vertex == 'start':
            return err_norm + err_halfnorm

        if vertext == 'end':
            return err_norm - err_halfnorm

    def calc_predvalue(self, data):
        expected_value = self.calc_expected_value(data)
        variance_norm = self.error_specification.variance[0,0]
        variance_halfnorm = self.error_specification.variance[1,1]
        vertex = self.error_specification.vertex
        size = (data.rows, 1)

        err = self.calc_errorcomponent(variance_norm, variance_halfnorm, vertex, size)
        
        pred_value = expected_value.data + err

        return DataArray(pred_value, self.specification.choices)

    
import unittest
from numpy import array
from openamos.core.data_array import DataArray
from openamos.core.models.model_components import Specification
from openamos.core.models.error_specification import StochasticRegErrorSpecification

class TestStocFronRegressionModel(unittest.TestCase):
    def setUp(self):
        choice = ['Frontier']
        coefficients = [{'constant':2, 'Var1':2.11}]
        data = array([[1, 1.1], [1, -0.25], [1, 3.13], [1, -0.11]])       
        variance = array([[1., 0], [0, 1.1]])

        self.data = DataArray(data, ['Constant', 'VaR1'])
        self.specification = Specification(choice, coefficients)
        self.errorspecification = StochasticRegErrorSpecification(variance, 'start')


    def testvalues(self):
        model = StocFronRegressionModel(self.specification, self.errorspecification)
        pred_value = model.calc_predvalue(self.data)

        random.seed(1)
        expected_act = self.data.calculate_equation(self.specification.coefficients[0])
        expected_act.shape = (4,1)
        variance = self.errorspecification.variance
        pred_act = (expected_act + 
                    norm.rvs(scale=variance[0, 0], size=(4,1)) + 
                    halfnorm.rvs(scale=variance[1, 1], size=(4,1)))

        pred_diff = all(pred_value.data == pred_act)
        self.assertEquals(True, pred_diff)
        
if __name__ == '__main__':
    unittest.main()
