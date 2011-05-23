import copy
import time
import traceback, sys
from numpy import logical_or, logical_and, ones, ma, zeros, where, vstack
from numpy.ma import masked_equal
from openamos.core.data_array import DataArray
from openamos.core.models.model import SubModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.errors import ModelError
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel

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
		 delete_dict={}):

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
	self.aggregate_variable_dict = aggregate_variable_dict
	self.delete_dict = delete_dict

        self.keyColsList()
        #self.dependencyAllocationFlag = dependencyAllocationFlag
    #TODO: check for names in the variable list
    #TODO: check for varnames in model specs and in the data

    def keyColsList(self):
        if self.key[1] is not None:
            self.keyCols = self.key[0] + self.key[1]
        else:
            self.keyCols = self.key[0]

    def pre_process(self, queryBrowser, 
                    skimsMatrix, uniqueIds, db, fileLoc):

        tableOrderDict = self.tableOrder
	tableNamesKeyDict = self.tableKeys

        t_d = time.time()
        # process the variable list to exclude double columns, 
        # return the primary keys, the county keys, 
        # the independent variable dictionary and dependent variables dictionary
	self.tableOrder = tableOrderDict
	self.tableKeys = tableNamesKeyDict

        vars_dict, depvars_dict, prim_keys, count_keys = self.prepare_vars()

        #print self.variable_list

	for table in vars_dict:
	    try:
	        keys = tableNamesKeyDict[table]
	        if len(keys[1]) > 0:
	            count_keys[table] = keys[1]
	    except Exception, e:
		pass



        # Prepare Data
        data = self.prepare_data(queryBrowser, vars_dict, depvars_dict, 
                                 tableOrderDict, tableNamesKeyDict, 
                                 count_keys)        





	print 'Basic Query complete'


        self.db = db

        # Skip running the component if no records are retrieved
        # to be processed
        if data == None or data.rows == 0:
            return None

        # Append cols for dependent variables
        self.append_cols_for_dependent_variables(data, depvars_dict)

        if data == None or data.rows == 0:
            return None

	print 'Additional Columns added'

        # Process and include spatial query information
        data = self.process_data_for_locs(data, self.spatialConst_list, 
                                          self.analysisInterval, 
					  skimsMatrix, uniqueIds, fileLoc)

        if data == None or data.rows == 0:
            return None

	print 'Location processed'

        #print 'processing dependencies', self.dependencyAllocationFlag
	"""
        if self.dependencyAllocationFlag:
            self.process_adult_allocation(data, queryBrowser, householdStructureObject)
        """

        return data
        print '-- Time taken to retrieve data - %.4f --' %(time.time()-t_d)

    def create_choiceset(self, shape, criterion, names):
        #TODO: Should setup a system to generate the choicesets dynamically
        #based on certain criterion

        # this choiceset creation criterion must be an attribute of the 
        # SubModel class
        choiceset = ones(shape)
        return DataArray(choiceset, names)

    def run(self, data, queryBrowser, skimsMatrix, uniqueIds, fileLoc):
        #TODO: check for validity of data and choiceset TYPES
        self.data = data
	tableNamesKeyDict = self.tableKeys
        #raw_input()
        #self.db = db

        # the variable keeps a running list of models that need to be run
        # this way first we run through all models once.  
        # In the next iteration, only those models are executed
        # as indicated by the run_until_condition
        model_list_duringrun = copy.deepcopy(self.model_list)
        iteration = 0

        prim_key = self.key[0]
        count_key = self.key[1]

        nRowsProcessed = 0
        while len(model_list_duringrun) > 0:
            t = time.time()
        
            model_st = copy.deepcopy(model_list_duringrun)
            iteration += 1
            #print '\n\tIteration - ', iteration
            #print model_list_duringrun
            model_list_duringrun, data_filter = self.iterate_through_the_model_list(
                model_list_duringrun, iteration, skimsMatrix, uniqueIds, fileLoc)   

            data_filter_count = data_filter.sum()
            data_post_run_filter = self.create_filter(self.post_run_filter, 'and')

            valid_data_rows = logical_and(data_post_run_filter, data_filter)
            valid_data_rows_count = valid_data_rows.sum()

            count_invalid_rows = data_filter_count - valid_data_rows_count

            if count_invalid_rows > 0:
                print """\tSome rows (%s) are not valid; they do not """\
                    """satisfy consistency checks - %s""" %(count_invalid_rows, 
                                                            self.post_run_filter)
	    """	
            try:
		print valid_data_rows
	    except Exception, e:
		print 'Error - e'
	    """
            nRowsProcessed += valid_data_rows_count

            #print "\t    Writing to cache table %s: records - %s" %(self.writeToTable, valid_data_rows_count)
	    trips = self.reflectToDatabase(valid_data_rows, tableNamesKeyDict, queryBrowser, fileLoc)
        return trips


    def reflectToDatabase(self, valid_data_filter, tableNamesKeyDict, queryBrowser, fileLoc):
        """
        This will reflect changes for the particular component to the database
        So that future queries can fetch appropriate run-time columns as well
        because the output is currently cached on the hard drive and the queries
        are using tables in the database which only contain the input tables 
        and hence the need to reflect the run-time caches to the database
        """
	# Reflecting the dynamic activity-travel generation to data table and also extracting and passing trips
	try:
	    ti = time.time()
	    tableCols = self.db.returnCols(self.writeToTable)
            
            convType = self.db.returnTypeConversion(self.writeToTable)
	    dtypesInput = self.db.tableColTypes(self.writeToTable)

	    # O and D are not same
	    data = self.data.columnsOfType(tableCols, valid_data_filter, dtypesInput)
	
	    keyCols = tableNamesKeyDict[self.writeToTable][0] 

	    print '--> here are the keyCols for this component', keyCols
	    #raw_input()
	
	    if self.component_name == 'ExtractTravelEpisodes' or self.component_name == 'ExtractBackgroundTravelEpisodes':
 	    	queryBrowser.copy_into_table(data.data, tableCols, self.writeToTable, keyCols, fileLoc, createIndex=False, deleteIndex=True)
	    else:
 	    	queryBrowser.copy_into_table(data.data, tableCols, self.writeToTable, keyCols, fileLoc)		

	    if self.component_name == 'ExtractAllTravelEpisodes':
	        data_array = zeros((valid_data_filter.sum(), len(tableCols)))

	    	dataTempNames = data.data.dtype.names 
	        for i in range(len(dataTempNames)):
		    name = dataTempNames[i]
		    data_array[:,i] = data.data[name]


            if self.delete_criterion is not None:
            	if self.delete_criterion:
                    self.data.deleterows(~valid_data_filter)
            	else:
                    self.data.deleterows(valid_data_filter)          

	
	    print '\t\tNumber of rows processed - ', valid_data_filter.sum()

	except Exception, e:
	    print e
            traceback.print_exc(file=sys.stdout)
	    data_array = zeros((1, 11))

        if self.component_name == 'ExtractAllTravelEpisodes':
	    return data_array

	
	"""
	try:

	    if self.component_name == 'ExtractTravelEpisodes':
	        ti = time.time()
	        tripColsTable = self.db.returnCols('trips_r')
            
                convType = self.db.returnTypeConversion('trips_r')
	        dtypesInput = self.db.tableColTypes('trips_r')

	        # O and D are not same
		trips_filter = valid_data_filter
	        trips_data = self.data.columnsOfType(tripColsTable, trips_filter, dtypesInput)
	
		keyCols = tableNamesKeyDict['trips_r'][0] 

		queryBrowser.copy_into_table(trips_data.data, tripColsTable, 'trips_r', keyCols, fileLoc)
		trips_data_array = zeros((trips_filter.sum(), len(tripColsTable)))
		tripDataTempNames = trips_data.data.dtype.names 
		for i in range(len(tripDataTempNames)):
		    name = tripDataTempNames[i]
		    trips_data_array[:,i] = trips_data.data[name]
		
	        print '\t\tBatch Insert for trips took - %.4f' %(time.time()-ti) 
		print '\t\tNumber of rows processed - ', trips_filter.sum()
	        tripsProcessed = trips_filter.sum()
	    else:
		tripsProcessed = 0
		trips_data_array = zeros((1,9))
	except Exception, e:
	    print '-- Error -- ', e
	    tripsProcessed = 0
	    trips_data_array = zeros((1,9))
	    pass

	print trips_data
	print trips_data._colnames
	return trips_data_array
	"""

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
                                       iteration, skimsMatrix, uniqueIds, fileLoc):
        ti = time.time()
        model_list_forlooping = []
        
        for j in range(len(model_list_duringrun)):
            i = model_list_duringrun[j]
            print '\t    Running Model - %s; Seed - %s' %(i.dep_varname, i.seed)
	    print i.data_filter
            #print '\t\tChecking for dynamic spatial queries'
            if j >=1:
                prev_model_name = model_list_duringrun[j-1].dep_varname
                current_model_name = i.dep_varname
                
                self.check_for_dynamic_spatial_queries(prev_model_name, 
                                                       current_model_name, skimsMatrix, uniqueIds, fileLoc)

            # Creating the subset filter
            data_subset_filter = self.create_filter(i.data_filter, i.filter_type)

            tiii = time.time()

            if data_subset_filter.sum() > 0:
                data_subset = self.data.columns(self.data.varnames, 
                                                data_subset_filter)
                print '\t\tData subset extracted is of size %s in %.4f' %(data_subset_filter.sum(),
                                                                              time.time()-tiii)
                # Generate a choiceset for the corresponding agents
                #TODO: Dummy as of now
                #choiceset_shape = (data_subset.rows,
                #                   i.model.specification.number_choices)
                #choicenames = i.model.specification.choices
                choiceset = None

                if i.model_type <> 'consistency':
                    result = i.simulate_choice(data_subset, choiceset, iteration)
                    self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            
		else:
		    result = i.simulate_choice(data_subset, choiceset, iteration)
		    self.data = result
		    # Update the filter because the number of rows may have changed in the data
		    # for eg. remove work activties from schedules when daily work status is zero
		    data_subset_filter = self.create_filter(i.data_filter, i.filter_type)


		                    
                #result = i.simulate_choice(data_subset, choiceset, iteration)
                print result.data
                #self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            
        
        # Update hte model list for next iteration within the component

        for i in model_list_duringrun:
            if i.run_until_condition is None:
                i.run_until_condition = []
            if self.data.rows > 0 and len(i.run_until_condition) > 0:
                run_subset_filter = self.create_filter(i.run_until_condition, 
                                                       i.run_filter_type)
		#print 'Filter subset sum - ',  run_subset_filter.sum()
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

    def check_for_dynamic_spatial_queries(self, prev_model_name, current_model_name, skimsMatrix, uniqueIds, fileLoc):
        if len(self.dynamicspatialConst_list) > 0:
            for const in self.dynamicspatialConst_list:
                if prev_model_name == const.afterModel and current_model_name == const.beforeModel:
                    #print 'FOUND DYNAMICS SPATIAL QUERY'
                    #raw_input()
                    self.process_data_for_locs(self.data, [const], self.analysisInterval,
                                               skimsMatrix, uniqueIds, fileLoc)
                
                
    
    def prepare_vars(self):
        #print variableList
	if self.analysisIntervalFilter is not None:
	    filtVar = (self.analysisIntervalFilter[0], 
		       self.analysisIntervalFilter[1])
	    if filtVar not in self.variable_list:
		self.variable_list.append(filtVar)
		
		
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
	
	if self.tableKeys[depVarTable] <> self.tableKeys[depVarWriteTable]:
	    #prim_keys[depVarTable] = tableNamesKeyDict[depVarTable][0]
	    prim_keys[depVarWriteTable] = self.tableKeys[depVarWriteTable][0]
	    count_keys[depVarWriteTable] = self.tableKeys[depVarWriteTable][1]
	    prim_keys[depVarTable] = self.tableKeys[depVarTable][0]
	    #count_keys[depVarTable] = tableNamesKeyDict[depVarTable][1]

	
        indep_columnDict = self.update_dictionary(indep_columnDict, prim_keys)
        indep_columnDict = self.update_dictionary(indep_columnDict, count_keys)

        #dep_columnDict = self.update_dictionary(dep_columnDict, count_keys)
        

	
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
            
        if len(tempdep_columnDict['temp']) > 0:
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
                     tableOrderDict=None, tableNamesKeyDict=None, 
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
                    data.insertcolumn([j], tempValsArr)
        return data




    def process_adult_allocation(self, data, queryBrowser, householdStructureObject):

        structuresDict = householdStructureObject.structuresDict

        for structure in structuresDict:
            structureVarVal = structuresDict[structure]
            self.prepare_household_structure_matrix(data, queryBrowser, 
                                                    structureVarVal, householdStructureObject)

            


            

    def process_data_for_locs(self, data, spatialConst_list, 
                              analysisInterval, skimsMatrix, uniqueIds, fileLoc):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of 
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """
        # LOAD THE NETWORK SKIMS ON THE MEMORY AS NUMPY ARRAY
        

        t = time.time()

        if spatialConst_list is not None:
            for i in spatialConst_list:
	
                if i.countChoices is not None: 
                    #print ("""\t\tNeed to sample location choices for the following""" \
                    #           """model with also location info extracted """)
                    data = self.sample_location_choices(data, skimsMatrix, uniqueIds, i, fileLoc)
                else:
                    #print '\tNeed to extract skims'
                    data = self.extract_skims(data, skimsMatrix, i)

        return data
    
                                        
    def sample_location_choices(self, data, skimsMatrix2, uniqueIDs, spatialconst, fileLoc):
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

        destLocSetInd2 = zeros((data.rows, max(uniqueIDs) + 1), dtype=float)


   	#print max(uniqueIDs), 'unique ids---------------'
        zoneLabels = ['geo-%s'%(i+1) for i in range(max(uniqueIDs))]


	# prepping the data matrix to add columns as needed
        sampleVarDict = {'temp':[]}
        sampleVarName = spatialconst.sampleField

        for i in range(spatialconst.countChoices):
            sampleVarDict['temp'].append('%s%s' %(sampleVarName, i+1))
            # Add a tt from destination field for checking heuristics etc...
            sampleVarDict['temp'].append('tt_from%s' %(i+1))

        self.append_cols_for_dependent_variables(data, sampleVarDict)


        for zone in uniqueIDs:
            destZone = zone * ones((data.rows, 1), dtype=int)
            timeToDest = skimsMatrix2[originLocColVals, destZone]
            timeFromDest = skimsMatrix2[destZone, destinationLocColVals]
            rowsLessThan = (timeToDest + timeFromDest < timeAvailable)[:,0]



            if rowsLessThan.sum() > 0:
                destLocSetInd2[rowsLessThan, zone] = 1
            

        print 'Time Available', timeAvailable[:,0]

            #if ma.any(rowsLessThan.mask):
            #    destLocSetInd2[~rowsLessThan.mask, zone] = 1
            #    k2 = rowsLessThan.sum()

        rowsZeroChoices = destLocSetInd2.sum(axis=1) == 0
	print """\t\t%s records were deleted because there """\
        	"""were no location reachable given the spatial/temporal """\
                """constraints""" %(rowsZeroChoices.sum())


	# Prepping up spatial constraint column for the valid records/agents
	"""

        destLocSetInd2 = destLocSetInd2[~rowsZeroChoices, :]


	print 'data before', data.data[:5,:5].astype(int)
	
	dataRowsValid = data.rowsof(~rowsZeroChoices)
	print 'validDataRows - ', dataRowsValid.data[:5,:5].astype(int)
	print 'data after', data.data[:5,:5].astype(int)
	print 'data subset after', dataRowsValid.data[:,:5].astype(int)
	#raw_input()
	"""

        originLocColVals = originLocColVals[~rowsZeroChoices, :]
        destinationLocColVals = destinationLocColVals[~rowsZeroChoices, :]

        originTimeColVals = originTimeColVals[~rowsZeroChoices, :]
        destinationTimeColVals = destinationTimeColVals[~rowsZeroChoices, :]



	# If there are no locations accessible then don't sample locations
        #if dataRowsValid.rows == 0:
        if ~rowsZeroChoices.sum() == 0:
	    print 'no sampling of locations'
	    return data





	# If locations are accessible then sample locations
	destLocSetInd2 = ma.masked_equal(destLocSetInd2, 0)

        seed = spatialconst.seed
        count = spatialconst.countChoices
        sampledChoicesCheck = True
        while (sampledChoicesCheck):
            #print '\t\tSampling Locations'
            #self.sample_choices(dataRowsValid, destLocSetInd2, zoneLabels, count, sampleVarName, seed)
            self.sample_choices(data, destLocSetInd2, zoneLabels, count, sampleVarName, seed, rowsZeroChoices)

            sampledVarNames = sampleVarDict['temp']
            #sampledChoicesCheck = self.check_sampled_choices(data, sampledVarNames)
            sampledChoicesCheck = False
            seed = seed + 1

        # Extract the location variables cache
        if len(spatialconst.locationVariables) > 0:
            locationsTable, uniqueIDs = self.db.returnTable(spatialconst.locationInfoTable, 
                                                            spatialconst.locationIdVar, 
                                                            spatialconst.locationVariables, 
							    fileLoc)



        for i in range(count):
            sampleLocColName = '%s%s' %(sampleVarName, i+1)
            #sampleLocColVals = array(dataRowsValid.columns([sampleLocColName]).data, dtype=int)
	    sampleLocColVals = array(data.columns([sampleLocColName], ~rowsZeroChoices).data, dtype=int)


            #print 'sampled locations - ', dataRowsValid.columns([sampleLocColName]).data[:,0]
            print 'sampled locations - ', data.columns([sampleLocColName], ~rowsZeroChoices).data[:,0]
            #print originLocColVals[:,0], sampleLocColVals[:,0]
            # the default missing value for skim was 9999 but that was causing problems with
            # calculation as aresult it is changed to a small number so that the alternative
            # corresponding to that is very negative. This is for those cases where the number
            # of choices is less than the minimum number of choices to be sampled

            # TO TRAVEL SKIMS
            vals = skimsMatrix2[originLocColVals, sampleLocColVals]
            rowsEqualsDefault = vals.mask
            # If OD pair missing for travel to set it to -9999 to make location
            # unattractive
            vals[rowsEqualsDefault] = 0
            if spatialconst.asField:
                colName = spatialconst.asField
            else:
                colName = spatialconst.skimField
            skimLocColName = '%s%s' %(colName, i+1)

	    sampleLocsZeros = sampleLocColVals == 0
	    vals[sampleLocsZeros] = 99
            #dataRowsValid.setcolumn(skimLocColName, vals)
            data.setcolumn(skimLocColName, vals, ~rowsZeroChoices)
	    #print 'TO VALS', skimLocColName, vals

            # FROM TRAVEL SKIMS
            vals = skimsMatrix2[sampleLocColVals, destinationLocColVals]

            rowsEqualsDefault = vals.mask
            # If OD pair missing for travel from then set it zero
            vals[rowsEqualsDefault] = 0            
            destSkimColName = 'tt_from%s' %(i+1)
            #dataRowsValid.setcolumn(destSkimColName, vals)
	    data.setcolumn(destSkimColName, vals, ~rowsZeroChoices)
	    #print 'FROM VALS', destSkimColName, vals

	    print 'LOCATION ATTRIBUTES'
            # Process Location Information if requested
            if len(spatialconst.locationVariables) > 0:
                for j in spatialconst.locationVariables:
                    #print 'location var', j
                    locationVarName = '%s%s' %(j, i+1)
                    locVarVals = locationsTable.columns([j]).data[sampleLocColVals]
                    #dataRowsValid.setcolumn(locationVarName, locVarVals)
                    data.setcolumn(locationVarName, locVarVals, ~rowsZeroChoices)
		    #print sampleLocColVals[:5]
                    print 'loc variable', locationVarName, 'vals', locVarVals[:5].astype(int)
		    #print locationsTable.varnames
        #raw_input()


	try:
	    print data.columns(['destination1', 'destination2', 'destination3']).data.astype(int)
	    #print dataRowsValid.columns(['destination1', 'destination2', 'destination3']).data.astype(int)
	except Exception, e:
	    print 'Error occurred printing: ', e
	    
		
	#print data.varnames
        colsInTable = sampleVarDict['temp']
        colsInTable.sort()
	#raw_input('spatial constraints processed')
        return data
            
    def extract_skims(self, data, skimsMatrix2, spatialconst):
        # hstack a column for the skims that need to be extracted for the
        # location pair
	print 'processing spatial constraint', spatialconst
        originLocColName = spatialconst.startConstraint.locationField
        destinationLocColName = spatialconst.endConstraint.locationField
        
        originLocColVals = array(data.columns([originLocColName]).data, dtype=int)
        destinationLocColVals = array(data.columns([destinationLocColName]).data, dtype=int)


        vals = skimsMatrix2[originLocColVals, destinationLocColVals]
        
        rowsEqualsDefault = vals.mask
        vals[rowsEqualsDefault] = 0
        #vals.shape = (data.rows,1)
        if spatialconst.asField:
            colName = spatialconst.asField
        else:
            colName = spatialconst.skimField

        sampleVarDict = {'temp':[colName]}
        self.append_cols_for_dependent_variables(data, sampleVarDict)

        #print vals[:,0]
	#print originLocColName, destinationLocColName
	#print 'Origin Loc', originLocColVals[:,0]
        #print 'Destination Loc', destinationLocColVals[:,0]
       	#print 'skims values', vals[:,0]

        #print vals[:,0]
	#print 'NEW IMPLEMENTATION'
        data.setcolumn(colName, vals)
	#print data.columns([colName])

        return data

    def sample_choices(self, data, destLocSetInd, zoneLabels, count, sampleVarName, seed, rowsZeroChoices):
        destLocSetInd = destLocSetInd[:,1:]
	#print 'number of choices - ', destLocSetInd.shape
        ti = time.time()
        for i in range(count):
            destLocSetIndSum = destLocSetInd.sum(-1)
            #print 'Number of choices', destLocSetIndSum
            probLocSet = (destLocSetInd.transpose()/destLocSetIndSum).transpose()

	    zeroChoices = destLocSetIndSum.mask

	    if (~zeroChoices).sum() == 0:
		print 'Zero Choices for some or all cases'
		continue

	    #print probLocSet.shape, len(zoneLabels), 'SHAPES -- <<'
            probDataArray = DataArray(probLocSet, zoneLabels)

            # seed is the count of the sampled destination starting with 1
            probModel = AbstractProbabilityModel(probDataArray, seed+i)
            res = probModel.selected_choice()
            
            # Assigning the destination
            # We subtract -1 from the results that were returned because the 
            # abstract probability model returns results indexed at 1
            # actual location id = choice returned - 1
            
            colName = '%s%s' %(sampleVarName, i+1)
            nonZeroRows = where(res.data <> 0)
	    #print 'SELECTED LOCATIONS FOR COUNT - ', i+1
            #print res.data[:,0]

            #actualLocIds = res.data
            #actualLocIds[nonZeroRows] -= 1
	    print 'data shape', data.data.shape
	    print 'result', res.data	
            data.setcolumn(colName, res.data)
	    #print data.columns([colName]).data[:,0]

            # Retrieving the row indices
            dataCol = data.columns([colName]).data

            rowIndices = array(xrange(dataCol.shape[0]), int)
	    rowIndices = rowIndices[~rowsZeroChoices]
            colIndices = res.data.astype(int)
	    colIndices = colIndices[~rowsZeroChoices]

	    print 'rowIndices', rowIndices
	    #print 'rowIndices', rowIndices[~rowsZeroChoices]

	    print 'colIndices', colIndices

	    print destLocSetInd.shape
            destLocSetInd.mask[rowIndices, colIndices-1] = True
        print "\t\t -- Sampling choices took - %.4f" %(time.time()-ti)

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
        
        
        
        
        

    
    
