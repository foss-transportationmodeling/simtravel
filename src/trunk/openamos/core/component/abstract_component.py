import copy
import time

from openamos.core.data_array import DataArray
from openamos.core.models.model import SubModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.errors import ModelError

class AbstractComponent(object):
    """
    This is the base class for implementing components in OpenAMOS
    
    Inputs:
    model_list - list of SubModel objects
    data - DataArray object on which the simulation needs to be carried out
    """
    def __init__(self, component_name, 
                 model_list, variable_list,
                 table,
                 key,
                 spatialConst_list=None,
                 analysisInterval=None):

        # TODO: DEAL WITH TAGGING COMPONENTS THAT NEED EXTRA PROCESSING
        # MAYBE JUST DO IT USING THE MODEL NAMES IN THE
        # SIMULATION MANAGER??
        
        # TODO: WHAT OTHER ADDITIONAL DATA IS NEEDED?

        # TODO: HOW TO DEAL WITH CONSTRAINTS?

        # TODO: CHOICESET GENERATION?

        # TODO: SEED


        for i in model_list:
            if not isinstance(i, SubModel):
                raise ModelError, """all object(s) in the model_list """\
                    """must be valid SubModel objects"""
        self.component_name = component_name
        #print '----->>>>>>', self.component_name
        #for i in model_list:
            #print '----->>>>>\t', i.dep_varname
        self.model_list = model_list

	self.variable_list = variable_list
        self.table = table
        self.key = key
        self.spatialConst_list = spatialConst_list
        self.analysisInterval = analysisInterval
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

    def run(self, data, db):
        #TODO: check for validity of data and choiceset TYPES
        self.data = data
        self.db = db

        # the variable keeps a running list of models that need to be run
        # this way first we run through all models once.  
        # In the next iteration, only those models are executed
        # as indicated by the run_until_condition
        model_list_duringrun = copy.deepcopy(self.model_list)
        iteration = 0

        prim_key = self.key[0]
        count_key = self.key[1]

        #table = self.table

        nRowsProcessed = 0
        while len(model_list_duringrun) > 0:
            t = time.time()
        
            model_st = copy.deepcopy(model_list_duringrun)
            iteration += 1
            print '\n\tIteration - ', iteration
            #print model_list_duringrun
            model_list_duringrun, data_filter = self.iterate_through_the_model_list(
                model_list_duringrun, iteration)   
            cols_to_write = [] + prim_key
            for model in model_st:
                dep_varname = model.dep_varname
                dep_varModel = model.model
                # Creating column list for caching
                if dep_varname not in cols_to_write and not isinstance(dep_varModel, InteractionModel):
                    cols_to_write.append(dep_varname)
            print "\t-- Iteration - %d took %.4f --" %(iteration, time.time()-t)
            print "\t    Writing to %s: records - %s" %(self.table, sum(data_filter))

            if count_key is not None and count_key not in cols_to_write:
                cols_to_write = cols_to_write + count_key
            
            self.write_data_to_cache(db, cols_to_write, data_filter)

            nRowsProcessed += sum(data_filter)
        return nRowsProcessed

    def write_data_to_cache(self, db, cols_to_write, data_filter):
        print '\t    Columns - ', cols_to_write
        data_to_write = self.data.columns(cols_to_write)
        
        t = time.time()
            # writing to the hdf5 cache
        cacheTableRef = db.returnTableReference(self.table)
        cacheTableRow = cacheTableRef.row
        
        for i in data_to_write.data[data_filter,:]:
            for j in xrange(len(cols_to_write)):
                cacheTableRow[cols_to_write[j]] = i[j]
            cacheTableRow.append()
        cacheTableRef.flush()
        print """\t    Writing to hdf5 cache format (appending one record at a time) """\
            """%.4f""" %(time.time()-t)
            

    def create_filter(self, data_filter):
        data_subset_filter = array([True]*self.data.rows)
        if data_filter is None:
            return data_subset_filter
        
        for filterInst in data_filter:
            condition_filter = filterInst.compare(self.data)
            data_subset_filter[~condition_filter] = False
        print '\t\tData Filter returned %s number of rows for above model' %sum(data_subset_filter)
        return data_subset_filter

    def iterate_through_the_model_list(self, model_list_duringrun, iteration):
        model_list_forlooping = []
        
        for i in model_list_duringrun:
            print '\t    Running Model - %s; Seed - %s' %(i.dep_varname, i.seed)
            #f = open('test_res', 'a')
            #f.write('%s,' %i.dep_varname)
            #f.close()

            # Creating the subset filter
            data_subset_filter = self.create_filter(i.data_filter)
            if data_subset_filter.sum() > 0:
                #print '\t RUN UNTIL CONDITION FILTER'
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
            #print '-----', choicenames, '--------'
            #print i
                choiceset = self.create_choiceset(choiceset_shape, 
                                                  i.choiceset_criterion, 
                                                  choicenames)
                #print "DATA SUBSET"
                #print data_subset
                #print data_subset.varnames
                
                result = i.simulate_choice(data_subset, choiceset, iteration)
                self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            
            #print result.data

                if i.run_until_condition is not None:
                    if data_subset.rows > 0:                    
                        model_list_forlooping.append(i)
                # Indiciator variable updating no longer happens in the ABSTRACT COMPONENT
                # Instead they are specified as simple regression models with the appropriate
                # specifications
                """
                print i.run_until_condition.coefficients, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                result_run_var = self.data.calculate_equation(i.run_until_condition.coefficients, 
                                                              data_subset_filter)
                self.data.setcolumn(i.run_until_condition.varname, 
                                    result_run_var, data_subset_filter)
                """
            #else:
            #    data_subset_filter = array([True]*self.data.rows)
            
        print '\t-- Iteration Complete --'
        #raw_input()
        return model_list_forlooping, data_subset_filter

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
        
        data_ = DataArray(data_, ['Const', 'Var1', 'Var2', 'Var3', 'choice2_ind', 
                                  'choice1', 'choice2', 'choice3'])

        var_list = [('table1', 'Var1'),
                    ('table1', 'Var2'),
                    ('table1', 'Var3'),
                    ('table1', 'Const')]
        
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
        component = AbstractComponent('DummyComponent', model_list, var_list)
    
        component.run(data_)
        print component.data.data

        
    def testvarscope(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        

    
    
