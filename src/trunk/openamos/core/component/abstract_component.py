import sys
import copy
import time
from numpy import logical_or, logical_and, ones, ma, zeros, where, vstack
from numpy.ma import masked_equal
from openamos.core.data_array import DataArray
from openamos.core.models.model import SubModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.errors import ModelError
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
import openamos

class AbstractComponent(object):
    """
    This is the base class for implementing components in OpenAMOS
    
    Inputs:
    model_list - list of SubModel objects
    data - DataArray object on which the simulation needs to be carried out
    """
    def __init__(self, component_name, 
                 model_list, variable_list,
                 readFromTable,
                 writeToTable,
                 key,
                 tableOrder,
                 tableKeys,
                 spatialConst_list=None,
                 dynamicspatialConst_list=None,
                 analysisInterval=None,
		 analysisIntervalFilter=None,
                 history_info=None,
                 post_run_filter=None,
                 delete_criterion=None,
                 dependencyAllocationFlag = False,
                 skipFlag=False,
		 aggregate_variable_dict={},
		 delete_dict={},
		 writeToTable2 = None,
		 key2=None,
		 pre_run_filter=None):

        # TODO: HOW TO DEAL WITH CONSTRAINTS?
        # TODO: CHOICESET GENERATION?

        for i in model_list:
            if not isinstance(i, SubModel):
                raise ModelError, """all object(s) in the model_list """\
                    """must be valid SubModel objects"""
        self.component_name = component_name
        self.model_list = model_list
	self.variable_list = variable_list
        self.readFromTable = readFromTable
        self.writeToTable = writeToTable
        self.key = key
        self.tableOrder = tableOrder
        self.tableKeys = tableKeys
        self.spatialConst_list = spatialConst_list
        self.dynamicspatialConst_list = dynamicspatialConst_list
        self.analysisInterval = analysisInterval
	self.analysisIntervalFilter = analysisIntervalFilter
        self.post_run_filter = post_run_filter
        self.delete_criterion = delete_criterion
        self.history_info = history_info
        self.skipFlag = skipFlag
        self.dependencyAllocationFlag = dependencyAllocationFlag
	self.aggregate_variable_dict = aggregate_variable_dict
	self.delete_dict = delete_dict
	self.writeToTable2 = writeToTable2
	self.key2 = key2
	self.pre_run_filter = pre_run_filter

        self.keyColsList()



    def keyColsList(self):
        if self.key[1] is not None:
            self.keyCols = self.key[0] + self.key[1]
        else:
            self.keyCols = self.key[0]

	if self.writeToTable2 is not None:
            if self.key2[1] is not None:
                self.keyCols2 = self.key2[0] + self.key2[1]
            else:
                self.keyCols2 = self.key2[0]


    def pre_process(self, queryBrowser, 
                    skimsMatrix, uniqueIds,
                    db, projectSeed=0):

	self.projectSeed = projectSeed	
	#print skimsMatrix
	#print '\tInside the pre processor and refcount is - ', sys.getrefcount(skimsMatrix), sys.getsizeof(skimsMatrix)


        t_d = time.time()
        # process the variable list to exclude double columns, 
        # return the primary keys, the county keys, 
        # the independent variable dictionary and dependent variables dictionary
        vars_dict, depvars_dict, prim_keys, count_keys = self.prepare_vars()

        #print self.variable_list


	#print 'count keys before', count_keys
	for table in vars_dict:
	    try:
	        keys = self.tableKeys[table]
		#print 'TABLE, KEYS - ', table, keys
	        if len(keys[1]) > 0:
	            count_keys[table] = keys[1]
	    except Exception, e:
		pass
	#print 'count keys after', count_keys
	#raw_input()


        # Prepare Data
        data = self.prepare_data(queryBrowser, vars_dict, depvars_dict, 
                                 count_keys)        


        self.db = db

        # Skip running the component if no records are retrieved
        # to be processed
        if data == None or data.rows == 0:
            return None

        # Append cols for dependent variables
        self.append_cols_for_dependent_variables(data, depvars_dict)

        if data == None or data.rows == 0:
            return None

        # Process and include spatial query information
	t = time.time()
	#print '\tReached point where skims are used'
        data = self.process_data_for_locs(data, self.spatialConst_list, 
                                          skimsMatrix, uniqueIds)
	print ('\tTime taken to process spatial constraints - %.4f' %(time.time()-t))
        if data == None or data.rows == 0:
            return None


	print '\tTime taken to retrieve data - %.4f --' %(time.time()-t_d)
        return data
        

    def create_choiceset(self, shape, criterion, names):
        #TODO: Should setup a system to generate the choicesets dynamically
        #based on certain criterion

        # this choiceset creation criterion must be an attribute of the 
        # SubModel class
        choiceset = ones(shape)
        return DataArray(choiceset, names)

    def run(self, data, skimsMatrix, partId=None):
        #TODO: check for validity of data and choiceset TYPES
        #print 'running for part id --------', partId
        self.data = data
        #raw_input()
        #self.db = db

        # the variable keeps a running list of models that need to be run
        # this way first we run through all models once.  
        # In the next iteration, only those models are executed
        # as indicated by the run_until_condition

	
        model_list_duringrun = copy.deepcopy(self.model_list)
        iteration = 0

	if self.pre_run_filter is not None:
	    self.pre_process_data()


        prim_key = self.key[0]
        count_key = self.key[1]

        nRowsProcessed = 0
        nRowsProcessed2 = 0
        while len(model_list_duringrun) > 0:
            t = time.time()
        
            model_st = copy.deepcopy(model_list_duringrun)
            iteration += 1
            #print '\n\tIteration - ', iteration
            #print model_list_duringrun
            model_list_duringrun, data_filter = self.iterate_through_the_model_list(
                model_list_duringrun, iteration, skimsMatrix)   

            data_filter_count = data_filter.sum()
            data_post_run_filter = self.create_filter(self.post_run_filter, 'and')

            valid_data_rows = logical_and(data_post_run_filter, data_filter)
            valid_data_rows_count = valid_data_rows.sum()

            count_invalid_rows = data_filter_count - valid_data_rows_count

            if count_invalid_rows > 0:
                print """\t\tSome rows (%s) are not valid; they do not """\
                    """satisfy consistency checks - %s""" %(count_invalid_rows, 
                                                            self.post_run_filter)
            nRowsProcessed += valid_data_rows_count

            print "\t\tWriting to cache table %s: records - %s" %(self.writeToTable, valid_data_rows_count)
	    self.write_data_to_cache(valid_data_rows, partId)
	    if self.writeToTable2 is not None:
		data_filter = array([True]*self.data2.rows)
		self.write_data_to_cache2(data_filter, partId)
		nRowsProcessed2 = data_filter.sum()
	    else:
		nRowsProcessed2 = 0
        return nRowsProcessed, nRowsProcessed2

    def pre_process_data(self):
	print 'Pre Process Filter is not None and processing following filter - ', self.pre_run_filter

	print 'Number of rows in the data - ', self.data.rows
	preRunFilter = self.create_filter(self.pre_run_filter, 'or')
	print 'Number of rows to be deleted - ', preRunFilter.sum()

	if preRunFilter.sum() > 0:
            self.data = self.data.columns(self.data.varnames, 
                                                ~preRunFilter)
	print 'Number of rows LEFT in the data - ', self.data.rows

	#raw_input()


    def write_data_to_cache(self, data_filter, partId=None):
	print '\tWriting to primary table - ', self.writeToTable
        # writing to the hdf5 cache
        #print 'writing to cache for ----', partId

	if data_filter.sum() > 0:
	    cacheTableRef = self.db.returnTableReference(self.writeToTable, partId)
            cacheColsTable = cacheTableRef.colnames

            t = time.time()
            convType = self.db.returnTypeConversion(self.writeToTable, partId)
            dtypesInput = cacheTableRef.coldtypes
            data_to_write = self.data.columnsOfType(cacheColsTable, data_filter, dtypesInput)
            #print '\t\tConversion to appropriate record array took - %.4f' %(time.time()-t) 

            ti = time.time()
            cacheTableRef.append(data_to_write.data)
            cacheTableRef.flush()
            #print '\t\tBatch Insert Took - %.4f' %(time.time()-ti) 

        ti = time.time()
        if self.delete_criterion is not None:
            if self.delete_criterion:
                self.data.deleterows(~data_filter)
            else:
                self.data.deleterows(data_filter)          

        #print '\t\t', self.delete_criterion
        #print '\t\tDeleting rows for which processing was complete - %.4f' %(time.time()-ti)
        #print '\t\tSize of dataset', self.data.rows	


    def write_data_to_cache2(self, data_filter, partId=None):
	print '\tWriting to secondary table - ', self.writeToTable2

	if data_filter.sum() > 0:
            cacheTableRef = self.db.returnTableReference(self.writeToTable2, partId)
            cacheColsTable = cacheTableRef.colnames

            convType = self.db.returnTypeConversion(self.writeToTable, partId)
            dtypesInput = cacheTableRef.coldtypes
            data_to_write = self.data2.columnsOfType(cacheColsTable, data_filter, dtypesInput)


            cacheTableRef.append(data_to_write.data)
            cacheTableRef.flush()


        if self.delete_criterion is not None:
            if self.delete_criterion:
                self.data2.deleterows(~data_filter)
            else:
                self.data2.deleterows(data_filter)          


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

        return data_subset_filter


    def iterate_through_the_model_list(self, model_list_duringrun, 
                                       iteration, skimsMatrix):
        ti = time.time()
        model_list_forlooping = []
        
        for j in range(len(model_list_duringrun)):
            i = model_list_duringrun[j]
            #print '\nRunning Model - %s; Seed - %s' %(i.dep_varname, i.seed)
            #print '\t\tChecking for dynamic spatial queries'
            if j >=1:
                prev_model_name = model_list_duringrun[j-1].dep_varname
                current_model_name = i.dep_varname
                
                self.check_for_dynamic_spatial_queries(prev_model_name, 
                                                       current_model_name, skimsMatrix)

            # Creating the subset filter
            data_subset_filter = self.create_filter(i.data_filter, i.filter_type)

            tiii = time.time()
		
	    #print '\t\tFILTER'
	    #print '\t\t', i.data_filter
            if data_subset_filter.sum() > 0:
                data_subset = self.data.columns(self.data.varnames, 
                                                data_subset_filter)
                #print '\t\tData subset extracted is of size %s in %.4f' %(data_subset_filter.sum(),
                #                                                              time.time()-tiii)
                # Generate a choiceset for the corresponding agents
                #TODO: Dummy as of now
                #choiceset_shape = (data_subset.rows,
                #                   i.model.specification.number_choices)
                #choicenames = i.model.specification.choices
                choiceset = None
                    
                #print '    RESULT BEFORE', self.data.columns([i.dep_varname], data_subset_filter).data[:5,0]

                if i.model_type <> 'consistency':
                    result = i.simulate_choice(data_subset, choiceset, iteration)
		    #print '\tFilter and data size - ', self.data.rows, data_subset_filter.sum()
		    if data_subset_filter.sum() == self.data.rows:
			#print '\t\tno filter'
			self.data.setcolumn(i.dep_varname, result.data)            
		    else:
			#print '\t\tthere is filter'
			self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            			

		else:
		    result = i.simulate_choice(data_subset, choiceset, iteration)
		    if self.writeToTable2 <> None:
			self.data2 = result[1]
			result = result[0]

		    self.data = result
		    # Update the filter because the number of rows may have changed in the data
		    # for eg. remove work activties from schedules when daily work status is zero
		    #data_subset_filter = self.create_filter(i.data_filter, i.filter_type)
		    data_subset_filter = array([True]*self.data.rows)
	      
		#print result.varnames
                #print '    RESULT', result.data[:5]
	    """
	    if i.dep_varname == 'tt_from1':
		raw_input()
	    """
        
        # Update hte model list for next iteration within the component

        for i in model_list_duringrun:
            if i.run_until_condition is None:
                i.run_until_condition = []
            if self.data.rows > 0 and len(i.run_until_condition) > 0:
                run_subset_filter = self.create_filter(i.run_until_condition, 
                                                       i.run_filter_type)
                if run_subset_filter.sum() > 0:
                    model_list_forlooping.append(i)

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

    def check_for_dynamic_spatial_queries(self, prev_model_name, current_model_name, skimsMatrix):
	#print self.dynamicspatialConst_list, prev_model_name, current_model_name
	#raw_input()
        if len(self.dynamicspatialConst_list) > 0:
            for const in self.dynamicspatialConst_list:
                if prev_model_name == const.afterModel and current_model_name == const.beforeModel:
                    #print 'FOUND DYNAMICS SPATIAL QUERY'
                    #raw_input()
                    self.process_data_for_locs(self.data, [const], 
                                               skimsMatrix)
                
                
    
    def prepare_vars(self):
        #print variableList                                                                                      
        indep_columnDict = self.prepare_vars_independent()
        
        tempdep_columnDict = {'temp':[]}
        spatialquery_columnDict = {}
        dep_columnDict = {}
        prim_keys = {}
        count_keys = {}

        depVarTable = self.readFromTable
        depVarWriteTable = self.writeToTable


	if self.tableKeys[depVarTable] == self.tableKeys[depVarWriteTable]:
	    if self.key[0] is not None:
                prim_keys[depVarTable] = self.key[0]
            if len(self.key[1]) > 0:
                count_keys[depVarTable] = self.key[1]
                tempdep_columnDict['temp'] += self.key[1]
	#print 'FIRST INSTANCE PROCESSING OF COUNT KEY', count_keys, prim_keys, indep_columnDict
	
	if (self.tableKeys[depVarTable] <> self.tableKeys[depVarWriteTable]) and len(self.aggregate_variable_dict) == 0 :
	    #prim_keys[depVarTable] = tableNamesKeyDict[depVarTable][0]
	    #prim_keys[depVarWriteTable] = self.tableKeys[depVarWriteTable][0]
	    if self.tableKeys[depVarWriteTable][1] <> []:
	    	count_keys[depVarWriteTable] = self.tableKeys[depVarWriteTable][1]
	    prim_keys[depVarTable] = self.tableKeys[depVarTable][0]
	    #count_keys[depVarTable] = tableNamesKeyDict[depVarTable][1]

	#print 'SECOND INSTANCE'	, count_keys, prim_keys, indep_columnDict
        indep_columnDict = self.update_dictionary(indep_columnDict, prim_keys)
        indep_columnDict = self.update_dictionary(indep_columnDict, count_keys)

	indep_columnDict = self.update_dictionary(indep_columnDict, self.aggregate_variable_dict)

        #dep_columnDict = self.update_dictionary(dep_columnDict, count_keys)
	#print 'THIRD INSTANCE'	, count_keys, prim_keys, indep_columnDict	        

	
	#print indep_columnDict
	#raw_input()

        # Needed only when updating to the same table
        # if writing to another table there is no need
        # to include dependent variables in the SQL query
        for submodel in self.model_list:
            depVarName = submodel.dep_varname

            #if depVarTable <> depVarWriteTable:
            #    tempdep_columnDict['temp'].append(depVarName)
            #else:
            if isinstance(submodel.model, InteractionModel):
                tempdep_columnDict['temp'].append(depVarName)
            else:
                #depVarTable = model.table                                                                 
                
                if depVarTable in indep_columnDict:
                    if depVarName in indep_columnDict[depVarTable]:
                        continue
                    
                if depVarTable in dep_columnDict:
                    dep_columnDict[depVarTable].append(depVarName)
                else:
                    dep_columnDict[depVarTable] = [depVarName]

        # Exclude the temp variables
        if 'temp' in indep_columnDict:
            temp_tableEntries = indep_columnDict.pop('temp')
            tempdep_columnDict['temp'] += temp_tableEntries
            
	# for including acolumn of ones
        if 'standard' in indep_columnDict:
            standard_tableEntries = indep_columnDict.pop('standard')
            tempdep_columnDict['standard'] = standard_tableEntries
	
        if 'temp' in tempdep_columnDict or 'standard' in tempdep_columnDict:
            dep_columnDict = self.update_dictionary(dep_columnDict, tempdep_columnDict)

        return indep_columnDict, dep_columnDict, prim_keys, count_keys

    def prepare_vars_independent(self):
        # Here we append attributes for all columns that appear on the RHS in the 
        # equations for the different models
        #print variableList

        indepColDict = {}
        for i in self.variable_list:
            tableName = i[0]
            colName = i[1]
            if tableName in indepColDict:
                indepColDict[tableName].append(colName)
            else:
                indepColDict[tableName] = [colName]

        # pop the runtime variables
        if 'runtime' in indepColDict:
            indepColDict.pop('runtime')

        return indepColDict


    def update_dictionary(self, dict_master, dict_to_merge):
        dict_m = copy.deepcopy(dict_master)

        for key in dict_to_merge:
            if key in dict_m:
                dict_m[key] = list(set(dict_m[key] + dict_to_merge[key]))
            else:
                dict_m[key] = dict_to_merge[key]

        return dict_m


    def process_anchors(self, columnDict, anchor):
        anchor_cols = []
        anchor_cols.append(anchor.locationField)

        if anchor.timeField is not None:
            anchor_cols.append(anchor.timeField)


        if anchor.table in columnDict:
            cols = columnDict[anchor.table]
            columnDict[anchor.table] = list((set(cols) |
                                             set(anchor_cols)))
        else:
            columnDict[anchor.table] = anchor_cols

        return columnDict

    def prepare_data(self, queryBrowser, indepVarDict, depVarDict, 
                     count_keys=None):
        #Get hierarchy of the tables

	#print 'INDEPEDNENT VAR DICTS', indepVarDict
	#print 'DEP VAR DICTS', depVarDict

        # PROCESSING TO INCLUDE THE APPROPRIATE SPATIAL QUERY ANCHORS
        if self.spatialConst_list is not None:
            # Removing those table/column entries which will be processed                                               
            # separately                                                                                                
            spatialQryTables = []
            for i in self.spatialConst_list:
                if i.table not in spatialQryTables:
                    spatialQryTables.append(i.table)

            #print 'SPATIAL QRY TABLES', spatialQryTables
            spatialQryDict = {}
            for i in spatialQryTables:
                if i in indepVarDict:
                    spatialQryDict[i] = indepVarDict.pop(i)
            # Include those variables that will be used to process the spatial                                          
            # queries for example the htaz, wtaz etc.                                                                   


            #Processing Anchors for variables to be included                                                            
            for i in self.spatialConst_list:
                if i.startConstraint.table <> i.endConstraint.table:
                    # Adding the columns that can then be used to retrieve the
                    # respective skims
                    stAnchor = i.startConstraint
                    endAnchor = i.endConstraint
                    indepVarDict = self.process_anchors(indepVarDict, stAnchor)
                    indepVarDict = self.process_anchors(indepVarDict, endAnchor)

                # the above cols are added for travel time type queries as they fit in the current
                # select join query build framework

                # the cols for time space prism vertices will be added to the query in real time
                # as they don't quite fit into the current setup



        orderKeys = self.tableOrder.keys()
        orderKeys.sort()
        
        tableNamesOrderDict = {}
        for i in orderKeys:
            tableNamesOrderDict[self.tableOrder[i][0]] = i

        tableNamesForComponent = indepVarDict.keys()

        found = []
        for i in list(set(tableNamesForComponent) & set(tableNamesOrderDict.keys())):
            order = tableNamesOrderDict[i]
            minOrder = min(tableNamesOrderDict.values())
            found.insert(order-minOrder, i)
            tableNamesForComponent.remove(i)

        #inserting back the ones that have a hierarchy defined
        tableNamesForComponent = found + tableNamesForComponent

        # replacing with the right keys for the main agents so that zeros are not
        # returned by the query statement especially for the variables defining the
        # agent id's
        
        found.reverse() # so that the tables higher in the hierarchy are fixed last; lowest to highest now

        for i in found:
            key = self.tableKeys[i][0] 
            for table in indepVarDict:
                intersectKeyCols = set(key) & set(indepVarDict[table])
                if len(intersectKeyCols) > 0:
                    indepVarDict[table] = list(set(indepVarDict[table]) - intersectKeyCols)
                    
                    if i in indepVarDict:
                        indepVarDict[i] = indepVarDict[i] + list(intersectKeyCols)
                    else:
                        indepVarDict[i] = intersectKeyCols

        found.reverse() # reversing back the heirarchy to go from highest to lowest

        # matching keys
        matchingKey = {}
        mainTable = found[0]
        mainTableKeys = self.tableKeys[mainTable][0]

        for i in indepVarDict.keys():
            if i == mainTable:
                matchingKey[i] = self.tableKeys[i][0]
                continue
            else:
		#print self.tableKeys
		#print 'KEY', i
                matchTableKeys = self.tableKeys[i][0]
            matchingKey[i] = list((set(mainTableKeys) and set(matchTableKeys)))

        # count dictionary or max dictionary
        if len(count_keys) == 0:
            max_dict = None
        else:
            max_dict = count_keys
	print max_dict
	#raw_input('max dict')
        # Cleaning up the independent variables dictionary
        iterIndepDictKeys = indepVarDict.keys()
        for i in iterIndepDictKeys:
            if len(indepVarDict[i]) == 0:
                indepVarDict.pop(i)


	for i in indepVarDict:
	    indepVarDict[i] = list(set(indepVarDict[i]))

        data = queryBrowser.select_join(indepVarDict, 
                                        matchingKey, 
                                        tableNamesForComponent, 
                                        max_dict, 
                                        self.spatialConst_list,
                                        self.analysisInterval,
					self.analysisIntervalFilter,
                                        self.history_info,
					self.aggregate_variable_dict,
					self.delete_dict)
	if data == None:
	    return None

        return data

    def append_cols_for_dependent_variables(self, data, depVarDict):
        numRows = data.rows
        tempValsArr = zeros((numRows,1))
        for i in depVarDict:
            colsInTable = list(set(depVarDict[i]))
            colsInTable.sort()

            for j in colsInTable:
                if j not in data._colnames:
		    if j == 'one':
			data.insertcolumn([j], tempValsArr + 1)
		    else:
                    	data.insertcolumn([j], tempValsArr)
	
	if self.analysisInterval is not None:
	    data.insertcolumn(['analysisinterval'], tempValsArr+self.analysisInterval)


        return data



    def process_data_for_locs(self, data, spatialConst_list, 
                              skimsMatrix, uniqueIds=None):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of 
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """
        # LOAD THE NETWORK SKIMS ON THE MEMORY AS NUMPY ARRAYNeed to e

        t = time.time()

        if spatialConst_list is not None:
            for i in spatialConst_list:
                #print '\n\tProcessing spatial queries'

                tableName = i.table
                originColName = i.originField
                destinationColName = i.destinationField
                skimColName = i.skimField

                if i.countChoices is not None: 
                    #print ("""\t\tNeed to sample location choices for the following""" \
                    #           """model with also location info extracted """)
                    data = self.sample_location_choices(data, skimsMatrix, uniqueIds, i)
                else:
                    #print '\tNeed to extract skims'
                    data = self.extract_skims(data, skimsMatrix, i)

        return data
    
    def create_location_filter(self, location_filter, location_filter_type, locations):
        ti = time.time()
	if location_filter is None:
	    location_filter = []
        if len(location_filter) > 0:
	    if location_filter_type == "and":
	        location_filter_method = logical_and
	        location_subset_filter = array([True]*locations.rows)
	    else:
	        location_filter_method = logical_or
		location_subset_filter = array([False]*locations.rows)
	

            for locFilter in location_filter:
                condition_filter = locFilter.compare(locations)
		location_subset_filter = location_filter_method(location_subset_filter, condition_filter)
	else:
	    location_subset_filter = array([True]*locations)

        return location_subset_filter
                                        
    def sample_location_choices(self, data, skimsMatrix2, uniqueIds, spatialconst):
        # extract destinations subject to the spatio-temporal
        # constraints

        originLocColName = 'st_%s' %(spatialconst.startConstraint.locationField)
        destinationLocColName = 'en_%s' %(spatialconst.endConstraint.locationField)

        originTimeColName = 'st_%s' %(spatialconst.startConstraint.timeField)
        destinationTimeColName = 'en_%s' %(spatialconst.endConstraint.timeField)

        # insert column for data availability
        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)


        originTimeColVals = array(data.columns([originTimeColName]).data, dtype=int)
        destinationTimeColVals = array(data.columns([destinationTimeColName]).data, dtype=int)


        timeAvailable = destinationTimeColVals - originTimeColVals

        sampleVarDict = {'temp':[]}
        sampleVarName = spatialconst.sampleField

        for i in range(spatialconst.countChoices):
            sampleVarDict['temp'].append('%s%s' %(sampleVarName, i+1))
            # Add a tt from destination field for checking heuristics etc...
            sampleVarDict['temp'].append('tt_from%s' %(i+1))

        self.append_cols_for_dependent_variables(data, sampleVarDict)

        # Extract the location variables cache
        if len(spatialconst.locationVariables) > 0:
	    locVariables = []
	    locVariables += spatialconst.locationVariables
	    if len(spatialconst.locationFilterList) > 0:
		for locFilter in spatialconst.locationFilterList:
		    if locFilter.varname not in locVariables:
		    	locVariables.append(locFilter.varname)	
	

            locationsTable, uniqueIds = self.db.returnTable(spatialconst.locationInfoTable, 
                                                            spatialconst.locationIdVar, 
                                                            locVariables)

	    #print locationsTable.varnames
	# Universe of possible locations; to allow for smart sampling

	#print 'shape of uniqueIds', uniqueIds.shape


	if len(spatialconst.locationVariables) > 0:
	    if len(spatialconst.locationFilterList) > 0:
		location_subset_filter = self.create_location_filter(spatialconst.locationFilterList, 
								     spatialconst.locationFilterType, 
								     locationsTable)
		#print 'Only so many possible locations - ', location_subset_filter.sum()
		#print 'shape of filter', location_subset_filter.shape
		uniqueIds = uniqueIds[location_subset_filter]
	


	#print 'Origin - ', originLocColVals[:,0]
	#print 'Destination - ', destinationLocColVals[:,0]
	timeAvailable = timeAvailable.astype(float)
	#print 'Time Available - ', timeAvailable[:,0]	
	

	#print spatialconst.countChoices, data.rows
	skimsMatrix2.create_location_array(data.rows)
	locationChoices = skimsMatrix2.get_location_choices(originLocColVals[:,0], destinationLocColVals[:,0], 
					  		    timeAvailable[:,0], spatialconst.countChoices,
							    uniqueIds)

	#print locationChoices.sum(-1)
	#print locationChoices
	
	for i in range(spatialconst.countChoices):
	    sampleLocColVals = locationChoices[:,i].astype(int)

	    tt_to = skimsMatrix2.get_travel_times(originLocColVals[:,0], sampleLocColVals)
	    tt_from = skimsMatrix2.get_travel_times(sampleLocColVals, destinationLocColVals[:,0])
	
	    #print 'Sampled locations - ', sampleLocColVals
	    #print 'Travel time to - ', tt_to
	    #print 'Travel time from - ', tt_from

	    # Updating the location columns
            colName = '%s%s' %(sampleVarName, i+1)
            data.setcolumn(colName, sampleLocColVals)


	    # Also updating skim values for sampled locations: here the travel time TO sampled location is updated
            if spatialconst.asField:
                colName = spatialconst.asField
            else:
                colName = spatialconst.skimField
            skimLocColName = '%s%s' %(colName, i+1)
	
            data.setcolumn(skimLocColName, tt_to)


	    # Also updating skim values for sampled locations: here the travel time FROM sampled location is updated
            destSkimColName = 'tt_from%s' %(i+1)
            data.setcolumn(destSkimColName, tt_from)


	    # Also updating location attributes for sampled locations
            if len(spatialconst.locationVariables) > 0:
                for j in spatialconst.locationVariables:
                    #print j
                    locationVarName = '%s%s' %(j, i+1)
                    locVarVals = locationsTable.columns([j]).data[sampleLocColVals]
                    data.setcolumn(locationVarName, locVarVals)
                    #print locVarVals


        return data
            
    def extract_skims(self, data, skimsMatrix2, spatialconst):
        # hstack a column for the skims that need to be extracted for the
        # location pair
        originLocColName = spatialconst.startConstraint.locationField
        destinationLocColName = spatialconst.endConstraint.locationField
        
        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)

	tt = skimsMatrix2.get_travel_times(originLocColVals[:,0], destinationLocColVals[:,0])
        if spatialconst.asField:
            colName = spatialconst.asField
        else:
            colName = spatialconst.skimField

        sampleVarDict = {'temp':[colName]}
        self.append_cols_for_dependent_variables(data, sampleVarDict)
        data.setcolumn(colName, tt)	

	#print originLocColVals[:,0]
	#print destinationLocColVals[:,0]
	#print tt

        return data

    def sample_choices(self, data, destLocSetInd, zoneLabels, count, sampleVarName, seed):
        destLocSetInd = destLocSetInd[:,1:]
	#print 'number of choices - ', destLocSetInd.shape
	#raw_input()
        ti = time.time()
        for i in range(count):
            destLocSetIndSum = destLocSetInd.sum(-1)
            #print 'Number of choices', destLocSetIndSum

	
            probLocSet = (destLocSetInd.transpose()/destLocSetIndSum).transpose()

	    zeroChoices = destLocSetIndSum.mask
            #print 'zero choices', zeroChoices
            if (~zeroChoices).sum() == 0:
                continue

	    #probLocSet = probLocSet[zeroChoices,:]
	    #print probLocSet.shape, len(zoneLabels), 'SHAPES -- <<'
            probDataArray = DataArray(probLocSet, zoneLabels)

            # seed is the count of the sampled destination starting with 1
            probModel = AbstractProbabilityModel(probDataArray, self.projectSeed+seed+i)
            res = probModel.selected_choice()
            
            # Assigning the destination
            # We subtract -1 from the results that were returned because the 
            # abstract probability model returns results indexed at 1
            # actual location id = choice returned - 1
            
            colName = '%s%s' %(sampleVarName, i+1)
            nonZeroRows = where(res.data <> 0)
	    #print 'SELECTED LOCATIONS FOR COUNT - ', i+1
            #print res.data[:,0]
            #actualLocIds = res.data[nonZeroRows]
            #actualLocIds[nonZeroRows] -= 1
            #print actualLocIds
            data.setcolumn(colName, res.data)
	    #print data.columns([colName]).data[:,0]
	    #raw_input()

            # Retrieving the row indices
            dataCol = data.columns([colName]).data

            rowIndices = array(xrange(dataCol.shape[0]), int)
	    #rowIndices = 0
            colIndices = res.data.astype(int)

            destLocSetInd.mask[rowIndices, colIndices-1] = True
        #print "\t\t -- Sampling choices took - %.4f" %(time.time()-ti)

    def check_sampled_choices(self, data, sampledVarNames):
        for i in range(len(sampledVarNames)):
            varName = sampledVarNames[i]
            checkAgainstVarNames = sampledVarNames[i+1:]
            for j in checkAgainstVarNames:
                columnI = data.columns([varName]).data
                columnJ = data.columns([j]).data
                check = data.data[where(columnI[where(columnI == columnJ)] <> 0)]
                if check.shape[0] > 0:
                    print '\t -- Warning:Choices are repeated; Repeating location sampling step --'
                    return True

        print '\t -- Choices are not repeated --'
        return False




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
        
        
        
        
        

    
    
