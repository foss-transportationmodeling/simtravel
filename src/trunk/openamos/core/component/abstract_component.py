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
                 readFromTable,
                 writeToTable,
                 key,
                 spatialConst_list=None,
                 analysisInterval=None,
                 post_run_filter=None,
                 delete_criterion=None):

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
        self.spatialConst_list = spatialConst_list
        self.analysisInterval = analysisInterval
        self.post_run_filter = post_run_filter
        self.delete_criterion = delete_criterion
        self.keyColsList()
    #TODO: check for names in the variable list
    #TODO: check for varnames in model specs and in the data

    def keyColsList(self):
        if self.key[1] is not None:
            self.keyCols = self.key[0] + self.key[1]
        else:
            self.keyCols = self.key[0]

    def pre_process(self, queryBrowser, subsample, 
                    tableOrderDict, tableNamesKeyDict,
                    projectSkimsObject, db):
        t_d = time.time()
        # process the variable list to exclude double columns, 
        # return the primary keys, the county keys, 
        # the independent variable dictionary and dependent variables dictionary
        vars_dict, depvars_dict, prim_keys, count_keys = self.prepare_vars()

        print self.variable_list

        # Prepare Data
        data = self.prepare_data(queryBrowser, vars_dict, depvars_dict, 
                                 tableOrderDict, tableNamesKeyDict, 
                                 count_keys, subsample)        


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
        data = self.process_data_for_locs(data, self.spatialConst_list, 
                                          self.analysisInterval, projectSkimsObject)

        if data == None or data.rows == 0:
            return None


        return data
        print '-- Time taken to retrieve data - %.4f --' %(time.time()-t_d)

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
            print '\n\tIteration - ', iteration
            #print model_list_duringrun
            model_list_duringrun, data_filter = self.iterate_through_the_model_list(
                model_list_duringrun, iteration)   

            data_filter_count = data_filter.sum()
            data_post_run_filter = self.create_filter(self.post_run_filter, 'and')

            valid_data_rows = logical_and(data_post_run_filter, data_filter)
            valid_data_rows_count = valid_data_rows.sum()

            count_invalid_rows = data_filter_count - valid_data_rows_count

            if count_invalid_rows > 0:
                print """\tSome rows (%s) are not valid; they do not """\
                    """satisfy consistency checks - %s""" %(count_invalid_rows, 
                                                            self.post_run_filter)
            nRowsProcessed += valid_data_rows_count

            print "\t    Writing to cache table %s: records - %s" %(self.writeToTable, valid_data_rows_count)
            self.write_data_to_cache(valid_data_rows)

        return nRowsProcessed

    def write_data_to_cache(self, data_filter):
        # writing to the hdf5 cache

        if data_filter.sum() < 1:
            return

        cacheTableRef = self.db.returnTableReference(self.writeToTable)
        cacheColsTable = cacheTableRef.colnames

        t = time.time()
        convType = self.db.returnTypeConversion(self.writeToTable)
        dtypesInput = cacheTableRef.coldtypes
        data_to_write = self.data.columnsOfType(cacheColsTable, data_filter, dtypesInput)
        print '\t\tConversion to appropriate record array took - %.4f' %(time.time()-t) 

        ti = time.time()
        cacheTableRef.append(data_to_write.data)
        cacheTableRef.flush()
        print '\t\tBatch Insert Took - %.4f' %(time.time()-ti) 

        ti = time.time()
        if self.delete_criterion is not None:
            if self.delete_criterion:
                self.data.deleterows(~data_filter)
            else:
                self.data.deleterows(data_filter)          

        print '\t\t', self.delete_criterion
        print '\t\tDeleting rows for which processing was complete - %.4f' %(time.time()-ti)
        print '\t\tSize of dataset', self.data.rows


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


    def iterate_through_the_model_list(self, model_list_duringrun, iteration):
        ti = time.time()
        model_list_forlooping = []
        
        for i in model_list_duringrun:
            print '\t    Running Model - %s; Seed - %s' %(i.dep_varname, i.seed)

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
                choiceset_shape = (data_subset.rows,
                                   i.model.specification.number_choices)
                choicenames = i.model.specification.choices
                choiceset = None
                    
                result = i.simulate_choice(data_subset, choiceset, iteration)
                print result.data[:,0]
                self.data.setcolumn(i.dep_varname, result.data, data_subset_filter)            
        
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

        if self.key[0] is not None:
            prim_keys[depVarTable] = self.key[0]
        if self.key[1] is not None:
            count_keys[depVarTable] = self.key[1]


        indep_columnDict = self.update_dictionary(indep_columnDict, prim_keys)
        indep_columnDict = self.update_dictionary(indep_columnDict, count_keys)

        # Needed only when updating to the same table
        # if writing to another table there is no need
        # to include dependent variables in the SQL query
        for submodel in self.model_list:
            depVarName = submodel.dep_varname

            if depVarTable <> depVarWriteTable:
                tempdep_columnDict['temp'].append(depVarName)
            else:
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
                     tableOrderDict, tableNamesKeyDict, 
                     count_keys=None, subsample=None):
        #Get hierarchy of the tables

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



        orderKeys = tableOrderDict.keys()
        orderKeys.sort()
        
        tableNamesOrderDict = {}
        for i in orderKeys:
            tableNamesOrderDict[tableOrderDict[i][0]] = i

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
            key = tableNamesKeyDict[i][0] 
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
        mainTableKeys = tableNamesKeyDict[mainTable][0]

        for i in indepVarDict.keys():
            if i == mainTable:
                continue
            else:
                matchTableKeys = tableNamesKeyDict[i][0]
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

        data = queryBrowser.select_join(indepVarDict, 
                                        matchingKey, 
                                        tableNamesForComponent, 
                                        max_dict, 
                                        self.spatialConst_list,
                                        self.analysisInterval,
                                        subsample)
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
                data.insertcolumn([j], tempValsArr)
        return data

    def process_data_for_locs(self, data, spatialConst_list, 
                              analysisInterval, projectSkimsObject):
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
                print '\n\tProcessing spatial queries'

                tableName = i.table
                originColName = i.originField
                destinationColName = i.destinationField
                skimColName = i.skimField

                if analysisInterval is not None:
                    tableName = projectSkimsObject.lookup_table(analysisInterval)
                else:
                    tableName = projectSkimsObject.tableNamesList[0]
                
                print '\t\tAnalysis Interval - %s, Skims table name - %s ' %(analysisInterval, tableName)

                ti = time.time()
                skimsMatrix2, uniqueIDs = self.db.returnTableAsMatrix(tableName,
                                                                      originColName,
                                                                      destinationColName,
                                                                      skimColName)
                print '\t\tSkims Matrix Extracted in %.4f s' %(time.time()-ti)
                if i.countChoices is not None: 
                    print '\t\tNeed to sample location choices for the following model'
                    data = self.sample_location_choices(data, skimsMatrix2, uniqueIDs, i)
                else:
                    print '\tNeed to extract skims'
                    data = self.extract_skims(data, skimsMatrix2, i)

        return data
    
                                        
    def sample_location_choices(self, data, skimsMatrix2, uniqueIDs, spatialconst):
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

        for zone in uniqueIDs:
            destZone = zone * ones((data.rows, 1), dtype=int)
            timeToDest = skimsMatrix2[originLocColVals, destZone]
            timeFromDest = skimsMatrix2[destZone, destinationLocColVals]
            rowsLessThan = (timeToDest + timeFromDest < timeAvailable)[:,0]

            if ma.any(rowsLessThan.mask):
                destLocSetInd2[~rowsLessThan.mask, zone] = 1
                k2 = rowsLessThan.sum()

        rowsZeroChoices = destLocSetInd2.sum(axis=1) == 0
        print """\t\t%s records were deleted because there """\
            """were no location reachable given the spatial/temporal """\
            """constraints""" %(rowsZeroChoices.sum())


        # Deleting records for zero choices
        data.deleterows(~rowsZeroChoices)

        originLocColVals = originLocColVals[~rowsZeroChoices, :]
        destinationLocColVals = destinationLocColVals[~rowsZeroChoices, :]

        originTimeColVals = originTimeColVals[~rowsZeroChoices, :]
        destinationTimeColVals = destinationTimeColVals[~rowsZeroChoices, :]

        destLocSetInd2 = destLocSetInd2[~rowsZeroChoices, :]


        print """\t\tResulting records in the dataset - %s """%(data.rows)

        if data.rows == 0:
            return

        destLocSetInd2 = ma.masked_equal(destLocSetInd2, 0)

        zoneLabels = ['geo-%s'%(i+1) for i in range(max(uniqueIDs)+1)]

        sampleVarDict = {'temp':[]}
        sampleVarName = spatialconst.sampleField

        for i in range(spatialconst.countChoices):
            sampleVarDict['temp'].append('%s%s' %(sampleVarName, i+1))
            # Add a tt from destination field for checking heuristics etc...
            sampleVarDict['temp'].append('tt_from%s' %(i+1))

        self.append_cols_for_dependent_variables(data, sampleVarDict)


        seed = spatialconst.seed
        count = spatialconst.countChoices
        sampledChoicesCheck = True
        while (sampledChoicesCheck):
            print '\t\tSampling Locations'
            self.sample_choices(data, destLocSetInd2, zoneLabels, count, sampleVarName, seed)
            sampledVarNames = sampleVarDict['temp']
            #sampledChoicesCheck = self.check_sampled_choices(data, sampledVarNames)
            sampledChoicesCheck = False
            seed = seed + 1


        for i in range(count):
            sampleLocColName = '%s%s' %(sampleVarName, i+1)
            sampleLocColVals = array(data.columns([sampleLocColName]).data, dtype=int)


            
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
            vals[rowsEqualsDefault] = -9999
            if spatialconst.asField:
                colName = spatialconst.asField
            else:
                colName = spatialconst.skimField
            skimLocColName = '%s%s' %(colName, i+1)
            data.setcolumn(skimLocColName, vals)


            # FROM TRAVEL SKIMS
            vals = skimsMatrix2[sampleLocColVals, destinationLocColVals]

            rowsEqualsDefault = vals.mask
            # If OD pair missing for travel from then set it zero
            vals[rowsEqualsDefault] = 0            
            destSkimColName = 'tt_from%s' %(i+1)
            data.setcolumn(destSkimColName, vals)

        colsInTable = sampleVarDict['temp']
        colsInTable.sort()

        return data
            
    def extract_skims(self, data, skimsMatrix2, spatialconst):
        # hstack a column for the skims that need to be extracted for the
        # location pair
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

        data.insertcolumn([colName], vals)

        return data

    def sample_choices(self, data, destLocSetInd, zoneLabels, count, sampleVarName, seed):
        ti = time.time()
        for i in range(count):
            destLocSetIndSum = destLocSetInd.sum(-1)
            probLocSet = (destLocSetInd.transpose()/destLocSetIndSum).transpose()

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
            actualLocIds = res.data
            actualLocIds[nonZeroRows] -= 1
            data.setcolumn(colName, actualLocIds)

            # Retrieving the row indices
            dataCol = data.columns([colName]).data

            rowIndices = array(xrange(dataCol.shape[0]), int)
            colIndices = actualLocIds.astype(int)

            destLocSetInd.mask[rowIndices, colIndices] = True
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
        
        
        
        
        

    
    
