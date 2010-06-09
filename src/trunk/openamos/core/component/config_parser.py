'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

from lxml import etree
from numpy import array
from openamos.core.component.abstract_controller import BasicController

from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.stochastic_frontier_regression_model import StocFronRegressionModel
from openamos.core.models.count_regression_model import CountRegressionModel
from openamos.core.models.logit_choice_model import LogitChoiceModel
from openamos.core.models.ordered_choice_model import OrderedModel
from openamos.core.models.nested_logit_choice_model import NestedLogitChoiceModel

from openamos.core.models.model_components import Specification
from openamos.core.models.count_regression_model_components import CountSpecification
from openamos.core.models.error_specification import LinearRegErrorSpecification
from openamos.core.models.error_specification import StochasticRegErrorSpecification

from openamos.core.models.model import SubModel
from openamos.core.component.abstract_component import AbstractComponent

from openamos.core.errors import ConfigurationError 

class ConfigParser(object):
    """
	The class defines the parser for translating the model configuration
	file into python objects for execution.  
	"""

    def __init__(self, configObject=None, fileLoc=None, component=None):
        
        #TODO: check for file or object (should be instance of etree)
        # Storing data ??
        # Linearizing data for calculating activity-travel choice attributes??

        if configObject is None and fileLoc is None:
            raise ConfigurationError, """The configuration input is not valid; a """\
                """location of the XML configuration file or a valid etree """\
                """object must be passed"""

        if not isinstance(configObject, etree.ElementBase) and configObject is not None:
            raise ConfigurationError, """The configuration input is not a valid """\
                """etree.Element object""" 
                
        try:
            configObject = etree.parse(fileLoc)
        except:
            raise ConfigurationError, """The path for configuration file was """\
                """invalid"""
                 
        self.configObject = configObject
        
        self.componentName = component

    def parse(self):
        self.iterator = self.configObject.getiterator("Component")
        self.componentList = []
        
        for i in self.iterator:
            component = self.create_component(i)
            self.componentList.append(component)
            if i.attrib['name'] == self.componentName:
                return self.componentList

        return self.componentList
                
    def create_component(self, component_element):
        modelsIterator = component_element.getiterator("Model")
        model_list = []
        
        for i in modelsIterator:
            model = self.create_model_object(i)

            model_list.append(model)
        component = AbstractComponent(model_list)
        return component
        
    def create_model_object(self, model_element):
        model_formulation = model_element.attrib['formulation']
        
        if model_formulation == 'Regression':
            return self.create_regression_object(model_element)
            
        if model_formulation == 'Count':
            return self.create_count_object(model_element)
        
        if model_formulation == 'Multinomial Logit':
            return self.create_multinomial_logit_object(model_element)
    
        if model_formulation == 'Nested Logit':
            return self.create_nested_logit_object(model_element)

        if model_formulation == 'Ordered':
            return self.create_ordered_choice_object(model_element)

        if model_formulation == 'Probability':
            return self.create_probability_object(model_element)


    def create_regression_object(self, model_element):

        # Creating the coefficients input for the regression model
        variableIterator = model_element.getiterator('Variable')
        coefficients = {}
        for i in variableIterator:
            varname = i.get('var')
            coeff = i.get('coeff')
            coefficients[varname] = float(coeff)

        coefficients = [coefficients] 

        # dependent variable
        variable = model_element.get('name')
        choice = [variable]

        # specification object
        specification = Specification(choice, coefficients)

        # Reading the vertex
        vertex = model_element.get('vertex')

        # Creating the variance matrix
        model_type = model_element.get('type')
        
        varianceIterator = model_element.getiterator('Variance')
        
        if model_type == 'Linear Regression':
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance)         
            model = LinearRegressionModel(specification, errorSpec)
            
        
        if model_type == 'Stochastic Frontier':
            for i in varianceIterator:
                variance_type = i.get('type', default=None)
                if variance_type == None:
                    norm_variance = float(i.get('value'))
                elif variance_type == 'Half Normal':
                    half_norm_variance = float(i.get('value'))
                    
            variance = array([[norm_variance, 0],[0, half_norm_variance]])
            errorSpec = StochasticRegErrorSpecification(variance, vertex)
            model = StocFronRegressionModel(specification, errorSpec)                 

        model_type = 'regression'
        dep_varname = variable

                    
        model_object = SubModel(model, model_type, dep_varname)
        
        return model_object

    def create_count_object(self, model_element):
        # Creating the coefficients input for the regression model
        variableIterator = model_element.getiterator('Variable')
        coefficients = {}
        for i in variableIterator:
            varname = i.get('var')
            coeff = i.get('coeff')
            coefficients[varname] = float(coeff)

        coefficients = [coefficients] 

        # dependent variable
        variable = model_element.get('name')
        
        # alternatives        
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)

        # specification object
        specification = CountSpecification(choice, coefficients)
        
        model_type = 'choice'
        dep_varname = variable
        
        
        model = CountRegressionModel(specification)
        
        model_object = SubModel(model, model_type, dep_varname)
        
        return model_object
        

    def create_multinomial_logit_object(self, model_element):
        pass
    
    def create_nested_logit_object(self, model_element):
        pass
    
    def create_ordered_choice_object(self, model_element):
        pass
    
    def create_probability_object(self, model_element):
        pass
    
    
    

if __name__ == '__main__':
    from numpy import zeros, random
    from openamos.core.data_array import DataArray
    fileloc = '/home/karthik/simtravel/test/config.xml' 
    conf_parser = ConfigParser(fileLoc=fileloc)
    component_list = conf_parser.parse()
    
    colnames = ['one', 'age', 'parttime', 'telcomm', 'empserv', 'commtime', 'popres',
                'numchild', 'numdrv', 'respb', 'autoworkmode',
                'daystart', 'dayend', 'numjobs', 'workstart1', 'workend1', 
                'workstart2', 'workend2', 'schstart1', 'schend1', 
                'schstart2', 'schend2', 'preschstart', 'preschend']
    
    cols = len(colnames)
    cols_dep = 13
    
    import time
    
    ti = time.time()
    
    rows = 1000000
    
    rand_input = random.random_integers(1, 4, (rows,cols - cols_dep))
    
    data = zeros((rows, cols))

    data[:,:cols-cols_dep] = rand_input
    data = DataArray(data, colnames)
    
    
    for i in component_list:
        i.run(data)
    print i.data.data[:10]
    
    print 'TIME ELAPSED USING ARRAY FORMAT', time.time()-ti
    
    ti = time.time()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    