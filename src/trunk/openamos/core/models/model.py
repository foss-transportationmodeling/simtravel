from openamos.core.errors import ModelError
from openamos.core.data_array import DataFilter
from openamos.core.models.abstract_model import Model
from openamos.core.errors import CoefficientsError, SeedError

from numpy import random



class SubModel(object):
    """
    This is the base class for specifying models in the Component
    framework for building the OpenAMOS components.
    """
    def __init__(self, 
                 model, 
                 model_type, 
                 dep_varname,
                 data_filter=None,
                 run_until_condition=None,
                 choiceset_criterion=None,
                 #table=None,
                 #key=None,
                 values=None, 
                 seed=1):

        if not isinstance(model, Model):
            raise ModelError, 'the model input is not a valid Model object'
        self.model = model

        if self.check_string(model_type, ['regression', 'choice']):
            self.model_type = model_type.lower()

        if self.check_string(dep_varname, [dep_varname.lower()]):
            self.dep_varname = dep_varname.lower()

        if data_filter is not None:
            if not isinstance(data_filter, DataFilter):
                raise ModelError, 'the model input is not a valid DataFilter object'
        self.data_filter = data_filter
        
        if run_until_condition is not None:
            if not isinstance(run_until_condition, DataFilter):
                raise ModelError, """the model input - run_until_cindition is not """\
                    """a valid DataFilter object"""
        self.run_until_condition = run_until_condition 
        
        #TODO: Checks for table and key need to be included
        #self.table = table
        #self.key = key
        #TODO: ADD CODE TO CHECK CHOICESET_CRITERION
        self.choiceset_criterion = choiceset_criterion
        if type(seed) not in [int, float, long]:
            raise SeedError, """the seed input is not a valid number - only """\
                """floats, integers, and long number types are allowed"""
        self.seed = seed

        if values is not None:
            if not isinstance(values, list):
                raise ModelError, """the category-value lookup is not a valid"""\
                    """python list object"""
            if len(model.choices) <> len(values):
                raise ModelError, """the number of alternatives and the number of """\
                    """values are not consistent. They both should be of the same """\
                    """size."""
        self.values = values
        #print model.choices, values

    def check_string(self, value, valid_values):
        if not isinstance(value, str):
            raise ModelError, """the model input - %s is not a valid string """\
                %(value)
        
        if not value.lower() in valid_values:
            raise ModelError, """the model input - %s is not in the """\
                """list of valid values - %s""" %(value, valid_values)
    
        return True
    
    def simulate_choice(self, data, choiceset, iteration):
        # Setting the seed
        seed = self.seed + iteration

        if self.model_type == 'regression':
            result = self.model.calc_predvalue(data, seed)

        if self.model_type == 'choice':
            result = self.model.calc_chosenalternative(data, choiceset, seed)
            if self.values is not None:
                for i in range(len(self.values)):
                    rows = result == i+1
                    result.data[rows] = self.values[i]
                    
                    
            

        # In case of regression model, an DataArray object is returned
        # the column contains the values predicted for the dependent 
        # variable and the column name is the same as the dependent 
        # variable

        # In case of choice model, an array is returned that contains
        # the text for the chosen alternative for each row(agent)
        # Maybe this has to be modified to return a DataArray object
        # with column of values; and a dictionary is also returned
        # that contains the correspondence between the values and the
        # chosen alternative or should we fix the values and categories?
        # in the next step how are values identified?
      
        return result
    
    def __repr__(self):
        return 'Model Type - %s; Dependent Variable - %s' \
            %(self.model_type, self.dep_varname)


