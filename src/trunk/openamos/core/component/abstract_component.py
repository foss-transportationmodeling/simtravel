import copy
import time
from numpy import logical_or, logical_and
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
                 analysisInterval=None,
                 post_run_filter=None,
                 delete_criterion=None):

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
        self.post_run_filter = post_run_filter
        self.delete_criterion = delete_criterion
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

	"""
	print data.varnames
	try:
	    print data.columns(['tt_to'])
	except:
	    pass

	"""
        nRowsProcessed = 0
        while len(model_list_duringrun) > 0:
            t = time.time()
        
            model_st = copy.deepcopy(model_list_duringrun)
            iteration += 1
            print '\n\tIteration - ', iteration
            #print model_list_duringrun
            model_list_duringrun, data_filter = self.iterate_through_the_model_list(
                model_list_duringrun, iteration)   

            data_filter_count = data_filter.sum()

            data_post_run_filter = self.create_filter(self.post_run_filter, 'and')

            print 'POST RUN FILTER ', data_post_run_filter[data_filter]
            #print 'MODEL RUN FILTER', data_filter
            valid_data_rows = logical_and(data_post_run_filter, data_filter)
            valid_data_rows_count = valid_data_rows.sum()

            count_invalid_rows = data_filter_count - valid_data_rows_count

            if count_invalid_rows > 0:
                print """\tSome rows (%s) are not valid; they do not """\
                    """satisfy consistency checks - %s""" %(count_invalid_rows, 
                                                            self.post_run_filter)
                #raw_input()
            

            nRowsProcessed += valid_data_rows_count

            print "\t    Writing to cache table %s: records - %s" %(self.table, valid_data_rows_count)
            self.write_data_to_cache(db, valid_data_rows)

        return nRowsProcessed

    def write_data_to_cache(self, db, data_filter):
        # writing to the hdf5 cache

        cacheTableRef = db.returnTableReference(self.table)
        cacheColsTable = cacheTableRef.colnames
        print '\t    Columns - ', cacheColsTable
        #print '\t\tSequence in cache', cacheColsTable

        t = time.time()
        convType = db.returnTypeConversion(self.table)
        #print '\t\tConversion Type - ', convType
        dtypesInput = cacheTableRef.coldtypes
        #print dtypesInput
        data_to_write = self.data.columnsOfType(cacheColsTable, data_filter, dtypesInput)
        #data_to_write.data = data_to_write.data.astype(convType)
        print '\t\tConversion to appropriate record array took - %.4f' %(time.time()-t) 

        #print data_to_write

        ti = time.time()
        cacheTableRef.append(data_to_write.data)
        cacheTableRef.flush()
        print '\t\tBatch Insert Took - %.4f' %(time.time()-ti) 

        ti = time.time()
        if self.delete_criterion is not None:
            if self.delete_criterion:
                #deleterows where the condition is satisfied
                # repeat only for those that did not satisfy
                self.data.deleterows(~data_filter)
                print 'INSIDE VALUE EQUAL TO TRUE CRITERION'
            else:
                #deleterows where the condition is not satisfied
                # repeat only for those that do satisfy
                self.data.deleterows(data_filter)          
                print 'INSIDE VALUE EQUAL TO FALSE CRITERION'      
        print '\t\t', self.delete_criterion
        print '\t\tDeleting rows for which processing was complete - %.4f' %(time.time()-ti)
        print '\t\tSize of dataset', self.data.rows
        #raw_input()

    def create_filter(self, data_filter, filter_type):
        ti = time.time()
	if data_filter is None:
	    data_filter = []
        if len(data_filter) > 0:
	    if filter_type == "and":
	        filter_method = logical_and
	        data_subset_filter = array([True]*self.data.rows)
	    else:
	        filter_method = logical_or
		data_subset_filter = array([False]*self.data.rows)
	

            for filterInst in data_filter:
                condition_filter = filterInst.compare(self.data)
		data_subset_filter = filter_method(data_subset_filter, condition_filter)
	else:
	    data_subset_filter = array([True]*self.data.rows)

        #print '\t\tData Filter returned %s number of rows for above model took - %.4f' %(data_subset_filter.sum(),
        #                                                                                 time.time()-ti)
        return data_subset_filter


    def iterate_through_the_model_list(self, model_list_duringrun, iteration):
        ti = time.time()
        model_list_forlooping = []
        
        for i in model_list_duringrun:
            print '\t    Running Model - %s; Seed - %s' %(i.dep_varname, i.seed)
            #f = open('test_res', 'a')
            #f.write('%s,' %i.dep_varname)
            #f.close()

            # Creating the subset filter
            data_subset_filter = self.create_filter(i.data_filter, i.filter_type)
            tiii = time.time()
            if data_subset_filter.sum() > 0:
                #print '\t RUN UNTIL CONDITION FILTER'
                # The run condition filter to loop over records for which a certain
                # condition is not satisfied
                #if i.run_until_condition is not None:
                #    # Creating the run condition filter
                #    run_condition_filter = i.run_until_condition.compare(self.data)
                #else:
                #    run_condition_filter = array([True]*self.data.rows) 

                #run_condition_filter = ~run_condition_filter
                #print '\t\t', self.delete_criterion
                    
    
                # Creating the compound filter based on above two conditions 
                #data_subset_filter[~run_condition_filter] = False
                data_subset = self.data.columns(self.data.varnames, 
                                                data_subset_filter)
                print '\t\tData subset extracted is of size %s in %.4f' %(data_subset_filter.sum(),
                                                                              time.time()-tiii)
               # Generate a choiceset for the corresponding agents
                choiceset_shape = (data_subset.rows,
                                   i.model.specification.number_choices)
                choicenames = i.model.specification.choices
                #print '-----', choicenames, '--------'
                #print i
                #choiceset = self.create_choiceset(choiceset_shape, 
                #                                  i.choiceset_criterion, 
                #                                  choicenames)
                choiceset = None
                #print "DATA SUBSET"
                #print data_subset
                #print data_subset.varnames
                

                if data_subset.rows > 0:                    
                    if i.run_until_condition is not None:
                        model_list_forlooping.append(i)


                    result = i.simulate_choice(data_subset, choiceset, iteration)
		    print result.data[:,0]
                    self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            
                    #print result.data
                    
        #if data_subset.rows > 0:
        #    self.data.deleterows(~data_subset_filter)
        print '\t-- Iteration complete for one looping of models in %.4f--' %(time.time()-ti)
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
        
        
        
        
        

    
    
