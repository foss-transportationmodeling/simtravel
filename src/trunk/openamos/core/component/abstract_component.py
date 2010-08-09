from openamos.core.data_array import DataArray
from openamos.core.models.model import SubModel
from openamos.core.errors import ModelError

class AbstractComponent(object):
    """
    This is the base class for implementing components in OpenAMOS
    
    Inputs:
    model_list - list of SubModel objects
    data - DataArray object on which the simulation needs to be carried out
    """
    def __init__(self, component_name, model_list, variable_list):
        for i in model_list:
            if not isinstance(i, SubModel):
                raise ModelError, """all object(s) in the model_list """\
                    """must be valid SubModel objects"""
        self.component_name = component_name
        print '----->>>>>>', self.component_name
        for i in model_list:
            print '----->>>>>\t', i.dep_varname
        self.model_list = model_list

	self.variable_list = variable_list

    #TODO: check for names in the variable list
    #TODO: check for varnames in model specs and in the data

    def create_choiceset(self, shape, criterion, names):
        #TODO: Should setup a system to generate the choicesets dynamically
        #based on certain criterion

        # this choiceset creation criterion must be an attribute of the 
        # SubModel class
        from numpy import ones
        choiceset = ones(shape)
        return DataArray(choiceset, names)

    def run(self, data):
        
        #TODO: check for validity of data and choiceset TYPES
        self.data = data
        
        import copy
        # the variable keeps a running list of models that need to be run
        # this way first we run through all models once.  
        # In the next iteration, only those models are executed
        # as indicated by the run_until_condition
        model_list_duringrun = copy.deepcopy(self.model_list)
        count = 1

        while len(model_list_duringrun) > 0 and count <5:
            print 'ITERATION - ', count
            print model_list_duringrun
            model_list_duringrun = self.iterate_through_the_model_list(
                model_list_duringrun)   
            count = count + 1            

        #print self.data.columns(['choice1', 'choice2', 'choice3', 'choice2_ind'])

    
    def iterate_through_the_model_list(self, model_list_duringrun):
        model_list_forlooping = []
        
        for i in model_list_duringrun:
            print i.dep_varname
            # Creating the subset filter
            if i.data_filter is not None:
                data_subset_filter = i.data_filter.compare(self.data)
            else:
                data_subset_filter = array([True]*self.data.rows)

            # The run condition filter to loop over records for which a certain
            # condition is not satisfied
            if i.run_until_condition is not None:
                # Creating the run condition filter
                run_condition_filter = i.run_until_condition.compare(self.data)
            else:
                run_condition_filter = array([True]*self.data.rows) 

            # Creating the compound filter based on above two conditions 
            data_subset_filter[~run_condition_filter] = False
            data_subset = self.data.columns(self.data.varnames, 
                                            data_subset_filter)

            # Generate a choiceset for the corresponding agents
            choiceset_shape = (data_subset.rows,
                               i.model.specification.number_choices)
            choicenames = i.model.specification.choices
            choiceset = self.create_choiceset(choiceset_shape, 
                                              i.choiceset_criterion, 
                                              choicenames)
            
            result = i.simulate_choice(data_subset, choiceset)
            self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            

            if i.run_until_condition is not None:
                if data_subset.rows > 0:                    
                    model_list_forlooping.append(i)
                result_run_var = self.data.calculate_equation(
                                                              i.run_until_condition.coefficients, 
                                                              data_subset_filter)
                self.data.setcolumn(i.run_until_condition.varname, 
                                    result_run_var, data_subset_filter)
        return model_list_forlooping

        # SOMEWHERE THE DATA HAS TO BE STORED FOR THE VALUES THAT
        # ARE BEING SIMULATED IN BOTH CASES WHERE MODELS RUN IN A LOOP

        # AND IN THE ALTERNATIVE CASE WHERE THEY RUN ONLY ONCE
        # I.E. EITHER UPDATE SELF.DATA OBJECT; WRITE TO AGENT OBJECTS;
        # WRITE TO DATABASE

        # FOR MODELS THAT ARE RUN IN A LOOP SEED NEEDS TO BE MODIFIED
        # BECAUSE EVERYTIME THE PROBABILITYMODEL CLASS IS CALLED
        # LOOP, THE SEED IS BEING SET TO THE DEFAULT VALUE
        # ALTERNATIVELY THE SEED CAN BE SET IN THE COMPONENT

        
import unittest
from numpy import array, zeros, random
from openamos.core.models.error_specification import LinearRegErrorSpecification
from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.logit_choice_model import LogitChoiceModel
from openamos.core.models.model_components import Specification
from openamos.core.data_array import DataFilter

class TestAbstractComponent(unittest.TestCase):
    def setUp(self):
        
        
        data_ = zeros((5,8))
        
        random.seed(1)
        data_[:,:4] = random.rand(5,4)
        
        data_ = DataArray(data_, 
                                    ['Const', 'Var1', 'Var2', 'Var3', 'choice2_ind', 
                                     'choice1', 'choice2', 'choice3'])
        
        variance = array([[1]])
        
        choice1 = ['choice1']
        choice2 = ['choice2']
        choice3 = ['SOV', 'HOV']
        
        coefficients1 = [{'const':2, 'Var1':2.11}]
        coefficients2 = [{'const':1.5, 'var2':-.2, 'var3':16.4}]
        coefficients3 = [{'Const':2, 'Var1':2.11}, {'Const':1.2}]
        
        specification1 = Specification(choice1, coefficients1)
        specification2 = Specification(choice2, coefficients2)
        specification3 = Specification(choice3, coefficients3) 
        
        errorspecification = LinearRegErrorSpecification(variance)

        model1 = LinearRegressionModel(specification1, errorspecification)
        model2 = LinearRegressionModel(specification2, errorspecification)
        model3 = LogitChoiceModel(specification3)
        
        data_filter2 = DataFilter('choice2_ind', 'less than', 25, 
                                  {'choice2_ind':1, 'choice2':1}) #Run Until Condition

        #Subset for the model condition
        data_filter1 = DataFilter('Const', 'less than', 0.3)

        
        model_seq1 = SubModel(model1, 'regression', 'choice1')
        model_seq2 = SubModel(model2, 'regression', 'choice2', 
                              data_filter=data_filter1, run_until_condition=data_filter2)
        model_seq3 = SubModel(model3, 'choice', 'choice3', 
                              run_until_condition=data_filter2)
        model_list = [model_seq1, model_seq2, model_seq3]
    
        # SPECIFY SEED TO REPLICATE RESULTS, DATA FILTER AND 
        # RUN UNTIL CONDITION
        component = AbstractComponent(model_list)
    
        component.run(data_)

        
    def testvarscope(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        

    
    
