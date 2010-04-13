from openamos.core.errors import ModelError
from openamos.core.data_array import DataFilter



class SubModel(object):
    def __init__(self, 
                 model, 
                 model_type, 
                 dep_varname,
                 data_filter,
                 run_until_condition,
                 choiceset_criterion=None):

        if not isinstance(model, AbstractModel):
            raise ModelError, 'the model input is not a valid Model object'

        if not model_type in ['regression', 'choice']:
            raise ModelError, """the model input is not a valid model type; """\
                """the valid model types are 'regression' and 'choice'"""
        
        self.model_type = model_type

        if not isinstance(data_filter, DataFilter):
            raise ModelError, 'the model input is not a valid DataFilter object'

        self.data_filter = data_filter

        if not isinstance(run_until_condition, DataFilter):
            raise ModelError, """the model input - run_until_cindition is not """\
                """a valid DataFilter object"""
        

        #ADD CODE TO CHECK CHOICESET_CRITERION
        self.choiceset_criterion = choiceset_criterion

    def simulate_choice(self, data, choiceset):
        if self.model_type == 'regression':
            result = self.calc_predvalue(data)

        if self.model_type == 'choice':
            result = self.calc_chosenalternative(data, choiceset)

        # In case of regression model, an DataArray object is returned
        # the column contains the values predicted for the dependent 
        # variable and the column name is the same as the dependent 
        # variable

        # In case of choice model, an array is returned that contains
        # the text for the chosen alternative for each row(agent)
        # Maybe this has to be modified to return a DataArray object
        # with column of values; and a dictionary is also returned
        # that contains the correspondence between the values and the
        # chosen alternative
            
        print '\nSIMULATED CHOICE/PREDICTED VALUE'
        
        print result


