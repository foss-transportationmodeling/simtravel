from openamos.core.data_array import DataArray
from openamos.core.models.model import SubModel
from openamos.core.errors import ModelError

class BasicController(object):
    def __init__(self, model_list, data):
        for i in model_list:
            if not isinstance(i, SubModel):
                raise ModelError, """all object(s) in the model_list """\
                    """must be valid SubModel objects"""

        self.model_list = model_list
    #TODO: check for validity of dat aand choiceset TYPES
        self.data = data


    #TODO: check for varnames in model specs and in the data

    def create_choiceset(self, shape, criterion, names):
        #TODO: Should setup a system to generate the choicesets dynamically
        #based on certain criterion

        #this choiceset creation criterion must be an attribute of the SubModel class
        from numpy import ones
        choiceset = ones(shape)
        return DataArray(choiceset, names)


    def filter_data(self, data_filter):
        if data_filter is None:
            return self.data
        return data_filter.compare(self.data)
            

    def run(self):
        import copy
        # the variable keeps a running list of models that need to be run
        # this way first we run through all models once.  
        # In the next iteration, only those models are executed
        # as indicated by the run_until_condition
        model_list_duringrun = copy.deepcopy(self.model_list)

        while len(model_list_duringrun) > 0:
            print 'BEFORE THE MODELS ARE LOOPED THROUGH\n', model_list_duringrun
            model_list_duringrun = self.iterate_through_the_model_list(model_list_duringrun)   
            print 'AFTER THE MODELS ARE LOOPED THROUGH\n', model_list_duringrun            
    
    def iterate_through_the_model_list(self, model_list_duringrun):
        model_list_forlooping = []
    
        for i in model_list_duringrun:
            # Retrieving a subset of all agents (e.g., children, adults etc)
            # on which the particular model will be applied
            data_subset = self.filter_data(i.data_filter)

            # this subsection of the method is run when a particular
            # model has to be run until a condition is violated
            if i.run_until_condition is not None:
                # Retrieving the records of those agents
                agents_to_simulate = i.run_until_condition.compare(data_subset)
                if agents_to_simulate.rows > 0:
                    model_list_forlooping.append(i)
            else:
                agents_to_simulate = data_subset
                
                
            # Generate a choiceset for the corresponding agents
            choiceset_shape = (agents_to_simulate.rows,
                               i.model.specification.number_choices)
            choicenames = i.model.specification.choices
            choiceset = self.create_choiceset(choiceset_shape, i.choiceset_criterion, 
                                              choicenames)
            
            # simulate the choice
            result = i.simulate_choice(agents_to_simulate, choiceset)

            # update the results and check 
            # for the condition used to loop the model

            agents_to_simulate.setcolumn(i.dep_varname, result.data)
            
            if i.run_until_condition is not None:
                result_run_var = agents_to_simulate.calculate_equation(i.run_until_condition.coefficients)
                agents_to_simulate.setcolumn(i.run_until_condition.varname, result_run_var)
        print self.data
        return model_list_forlooping 

        # SOMEWHERE THE DATA HAS TO BE STORED FOR THE VALUES THAT
        # ARE BEING SIMULATED IN BOTH CASES WHERE MODELS RUN IN A LOOP
        # AND IN THE ALTERNATIVE CASE WHERE THEY RUN ONLY ONCE
        # I.E. EITHER UPDATE SELF.DATA OBJECT; WRITE TO AGENT OBJECTS;
        # WRITE TO DATABASE


        
import unittest
from numpy import array, zeros, random
from openamos.core.models.error_specification import LinearRegErrorSpecification
from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.model_components import Specification

class TestAbstractComponent(unittest.TestCase):
    def setUp(self):
        
        
        data_ = zeros((5,6))
        
        random.seed(1)
        data_[:,:4] = random.rand(5,4)
        
        data_ = DataArray(data_, 
                                    ['Const', 'Var1', 'Var2', 'Var3', 'choice1', 'choice2'])
        
        variance = array([[1]])
        
        choice1 = ['choice1']
        choice2 = ['choice2']
        
        coefficients1 = [{'const':2, 'Var1':2.11}]
        coefficients2 = [{'const':1.5, 'var2':-.2, 'var3':16.4}]
        
        specification1 = Specification(choice1, coefficients1)
        specification2 = Specification(choice2, coefficients2)
        
        errorspecification = LinearRegErrorSpecification(variance)

        model1 = LinearRegressionModel(specification1, errorspecification)
        model2 = LinearRegressionModel(specification2, errorspecification)
        
        model_seq1 = SubModel(model1, 'regression', 'choice1')
        model_seq2 = SubModel(model2, 'regression', 'choice2')
        
        model_list = [model_seq1, model_seq2]
    
        # SPECIFY SEED TO REPLICATE RESULTS, DATA FILTER AND RUN UNTIL CONDITION
        
        component = BasicController(model_list, data_)
    
        component.run()
        
    def testvarscope(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        

    
    
