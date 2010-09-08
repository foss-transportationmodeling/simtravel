import copy
import time
from lxml import etree
from numpy import array, ma, ones, zeros, random, vstack

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.run.dataset import DB
from multiprocessing import Process

class ComponentManager(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self, configObject=None, fileLoc=None, component=None):
        if configObject is None and fileLoc is None:
                raise ConfigurationError, """The configuration input is not valid; a """\
                """location of the XML configuration file or a valid etree """\
                """object must be passed"""

        if not isinstance(configObject, etree._ElementTree) and configObject is not None:
            print ConfigurationError, """The configuration object input is not a valid """\
                """etree.Element object. Trying to load the object from the configuration"""\
                """ file."""

        try:
            configObject = etree.parse(fileLoc)
        except Exception, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser
        self.projectConfigObject = self.configParser.parse_projectAttributes()
        

    def establish_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        self.queryBrowser.create_mapper_for_all_classes()
        print 'Database Connection Established'


    def close_databaseConnection(self):
        pass
        
    def establish_cacheDatabase(self, fileLoc, mode='w'):
        self.db = DB(fileLoc, mode)
        if mode == 'w':
            self.db.create()
            # placeholders for creating the hdf5 tables 
            # only the network data is read and processed for faster 
            # queries
            #self.db.createTableFromDatabase('travel_skims', self.queryBrowser)
        
        
    def run_components(self):
        t_c = time.time()
        componentList = self.configParser.parse_models()
        
        subsample = self.projectConfigObject.subsample
        
        for i in componentList:
            #self.queryBrowser.dbcon_obj.new_sessionInstance()
            tableName = i.table
            print '\nFor component - %s deleting corresponding table - %s' %(i.component_name, tableName)
            # clean the run time tables
            #delete the delete statement; this was done to clean the tables during testing
            self.queryBrowser.delete_all(tableName)            
        #self.queryBrowser.dbcon_obj.close_sessionInstance()            

        
        for i in componentList:
            # Create New Instance of the Session
            #self.queryBrowser.dbcon_obj.new_sessionInstance()

            t = time.time()
            print '\nRunning Component - %s' %(i.component_name)

            # Prepare variable list/objects for retrieving the corresponding records for processing
            variableList = i.variable_list
            #print '\tVariable List - ', len(variableList)
            vars_inc_dep, prim_keys, count_keys = self.prepare_vars(variableList, i)

            tableName = i.table

            # Prepare Data
            data = self.prepare_data(vars_inc_dep, count_keys=count_keys, subsample=subsample)        
        
            #if i.component_name == 'MorningVertex' or i.component_name == 'EveningVertex':
            #    print 'Data', data.columns(['houseid', 'personid', 'scheduleid']).data

            # Run the component
            nRowsProcessed = i.run(data, self.db)
            
            # Write the data to the database from the hdf5 results cache
            if i.key[1] is not None:
                keyCols = i.key[0] + i.key[1]
            else:
                keyCols = i.key[0]
            self.reflectToDatabase(tableName, keyCols, nRowsProcessed)

            print '-- Finished simulating model --'
            print '-- Time taken to complete - %.4f' %(time.time()-t)
            # Create New Instance of the Session
            #self.queryBrowser.dbcon_obj.close_sessionInstance()
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f' %(time.time()-t_c)

    def reflectToDatabase(self, tableName, keyCols=[], nRowsProcessed=0):
        """
        This will reflect changes for the particular component to the database
        So that future queries can fetch appropriate run-time columns as well
        because the output is currently cached on the hard drive and the queries
        are using tables in the database which only contain the input tables 
        and hence the need to reflect the run-time caches to the database
        """

        #self.queryBrowser.inser_into_table(data.data
        table = self.db.returnTableReference(tableName)
        
        
        #resIterator = table.iterrows()
        #t = time.time()
        #resArr = [row[:] for row in resIterator]
        #print """\tCreating the array object (iterating through the hdf5 results) """\
        #    """to insert into tbale - %.4f""" %(time.time()-t)
        #print type(resArr)
        
        t = time.time()

        print 'WRITING ROWS ------> ', nRowsProcessed
        resArr = list(table[-nRowsProcessed:])
        print """\tCreating the array object (WITHOUR iterating through the hdf5 results) """\
            """to insert into tbale - %.4f""" %(time.time()-t)
        colsToWrite = table.colnames

        #print resArr
        # TODO: delete rows from the local cache
        # In the current implementation, the rows are deleted before every update so that replication is not  done
        # in actual implementation, the local cache should be wiped clean so as to avoid the latency of 
        # inserting old rows and creating indices for them
        
        #self.queryBrowser.delete_all(tableName)            
        self.queryBrowser.insert_into_table(resArr, colsToWrite, tableName, keyCols, chunkSize=100000)

        
    def prepare_vars(self, variableList, component):
        #print variableList
        indep_columnDict = self.prepare_vars_independent(variableList)
        #print '\tIndependent Column Dictionary - ', indep_columnDict

        dep_columnDict = {}
        prim_keys = {}
        count_keys = {}


        depVarTable = component.table

        if component.key[0] is not None:
            prim_keys[depVarTable] = component.key[0]
        if component.key[1] is not None:
            count_keys[depVarTable] = component.key[1]
        

        for model in component.model_list:
            depVarName = model.dep_varname
            #depVarTable = model.table
            if depVarTable in dep_columnDict:
                dep_columnDict[depVarTable].append(depVarName)
            else:
                dep_columnDict[depVarTable] = [depVarName]
        
            """
            if model.key is not None:
                prim = model.key[0]

                if prim is not None:
                    if depVarTable not in prim_keys:
                        prim_keys[depVarTable] = prim
                    else:
                        prim_keys[depVarTable] = prim_keys[depVarTable] + prim
                        
                index = model.key[1]
                if index is not None:
                    if depVarTable not in index_keys:
                        index_keys[depVarTable] = index
                    else:
                        index_keys[depVarTable] = index_keys[depVarTable] + index
             """         
        #print '\tDependent Column Dictionary - ', dep_columnDict
        #print '\tPrimary Keys - ', prim_keys
        #print '\tIndex Keys - ', count_keys
       
        columnDict = self.update_dictionary(indep_columnDict, dep_columnDict)
        columnDict = self.update_dictionary(columnDict, prim_keys)
        columnDict = self.update_dictionary(columnDict, count_keys)

        #print '\tCombined Column Dictionary - ', columnDict
        return columnDict, prim_keys, count_keys
        

    def prepare_vars_independent(self, variableList):
        # Here we append attributes for all columns that appear on the RHS in the 
        # equations for the different models
        #print variableList

        indepColDict = {}
        for i in variableList:
            tableName = i[0]
            colName = i[1]
            if tableName in indepColDict:
                indepColDict[tableName].append(colName)
            else:
                indepColDict[tableName] = [colName]

        return indepColDict


    def update_dictionary(self, dict_master, dict_to_merge):
        dict_m = copy.deepcopy(dict_master)

        for key in dict_to_merge:
            if key in dict_m:
                dict_m[key] = list(set(dict_m[key] + dict_to_merge[key]))
            else:
                dict_m[key] = dict_to_merge[key]

        return dict_m

    def return_keys_toinclude(self, keys, prim_keys_ind=None):
        keysList = []
        keysNoDuplicates = {}
        for i in keys:
            if prim_keys_ind and i.find('_r') > -1:                
                #print 'primary keys and _r (result) table found'
                continue
            if len(set(keys[i]) & set(keysList)) == 0:
                keysNoDuplicates[i] = keys[i]
                keysList = keysList + keys[i]
                #print '%s not in - ' %(i), keysList, i not in keysList
        return keysNoDuplicates
            
            
    def prepare_data(self, columnDict, count_keys=None, subsample=None):
        # get hierarchy of the tables
        tableOrderDict, tableNamesKeyDict = self.configParser.parse_tableHierarchy()
        #print 'TABLE ORDER DICT', tableOrderDict
        #print 'TABLE NAMES KEY DICT', tableNamesKeyDict

        orderKeys = tableOrderDict.keys()
        orderKeys.sort()
        
        tableNamesOrderDict = {}
        #tableNamesKeyDict = {}
        for i in orderKeys:
            tableNamesOrderDict[tableOrderDict[i][0]] = i
            #tableNamesKeyDict[tableOrderDict[i][0]] = tableOrderDict[i][1]

        #print 'TABLE NAMES ORDER', tableNamesOrderDict
        # table order
        tableNamesForComponent = columnDict.keys()
        #print 'TABLE NAMES FOR COMPONENT', tableNamesForComponent

        found = []
        for i in list(set(tableNamesForComponent) & set(tableNamesOrderDict.keys())):
            order = tableNamesOrderDict[i]
            minOrder = min(tableNamesOrderDict.values())
            found.insert(order-minOrder, i)
            tableNamesForComponent.remove(i)

        #print 'COMPONENT TABLES AFTER', tableNamesForComponent
        #print 'HIERARCHY TABLES FOUND - ', found
        #inserting back the ones that have a hierarchy defined
        tableNamesForComponent = found + tableNamesForComponent

        #print '\ttableNamesforComponent - ', tableNamesForComponent

        # replacing with the right keys for the main agents so that zeros are not
        # returned by the query statement especially for the variables defining the
        # agent id's
        #print 'BEFORE FIXING INDEX KEYS', columnDict
        
        found.reverse() # so that the tables higher in the hierarchy are fixed last; lowest to highest now

        for i in found:
            key = tableNamesKeyDict[i][0] 
            for table in columnDict:
                intersectKeyCols = set(key) & set(columnDict[table])
                if len(intersectKeyCols) > 0:
                    columnDict[table] = list(set(columnDict[table]) - intersectKeyCols)
                    
                    if i in columnDict:
                        columnDict[i] = columnDict[i] + list(intersectKeyCols)
                    else:
                        columnDict[i] = intersectKeyCols
        #print 'AFTER FIXING INDEX KEYS', columnDict

        found.reverse() # reversing back the heirarchy to go from highest to lowest

        # matching keys
        matchingKey = {}
        mainTable = found[0]
        #print 'mainTable', mainTable
        mainTableKeys = tableNamesKeyDict[mainTable][0]

        for i in columnDict.keys():
            if i == mainTable:
                continue
            else:
                matchTableKeys = tableNamesKeyDict[i][0]
            matchingKey[i] = list((set(mainTableKeys) and set(matchTableKeys)))
        #print 'MATCHING KEY DICTIONARY', matchingKey
        #raw_input()

        #for i in found:
        #    if i in columnDict:
        #        matchingKey = tableNamesKeyDict[i][0]
        #        break

        #print '\tMATCHING KEY - ', matchingKey
        # count dictionary or max dictionary
        if len(count_keys) == 0:
            max_dict = None
        else:
            max_dict = count_keys

        #print 'COLUMN DICTIONARY', columnDict
        #print 'TABLE HIERARCHY', tableNamesForComponent
        #print 'MATCHING COLUMN', matchingKey
        #maxDict = {'vehicles_r':['vehid']}
        data = self.queryBrowser.select_join(columnDict, 
                                                        matchingKey, 
                                                        tableNamesForComponent, 
                                                        max_dict, 
                                                        subsample)
        return data
    

    """
    def read_data_store_in_hdf5(self):
        t = time.time()
        query_gen, cols = self.queryBrowser.select_all_from_table('travel_skims')
        print 'time to retrieve records %.4f' %(time.time()-t)

        t = time.time()
        
        # Create travelskims table in hdf5
        tableName = 'travel_skims'
        table = self.db.returnTableReference(tableName) 

        tableRow = table.row

        originCol = cols.index('origin')
        destinationCol = cols.index('destination')
        ttCol = cols.index('tt')

        for i in query_gen:
            tableRow['origin'] = i[originCol]
            tableRow['destination'] = i[destinationCol]
            tableRow['tt'] = i[ttCol]
            tableRow.append()
        table.flush()

        # Create households and persons table in hdf5
        print 'time to write to hdf5 format %.4f' %(time.time()-t)
    """ 

    def process_data_for_locs(self):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of 
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """

        
        # LOAD THE NETWORK SKIMS ON THE MEMORY AS NUMPY ARRAY
        t = time.time()

        tableName = 'travel_skims'
        table = self.db.returnTableReference(tableName)

        origin = table.col('origin')
        destination = table.col('destination')
        tt = table.col('tt')

        ttMatrix = zeros((max(origin)+1, max(destination)+1))

        ttMatrix[origin, destination] = tt

        originQ = 110
        destinationQ = 1745
        timeWindow = 45

        randint = random.randint
        
        destMatrix = zeros((10000, max(destination) + 1))


        #print ttToDest.shape, ttFromDest.shape
        for i in range(4000):
            originQ = randint(101, 2095)
            destinationQ = randint(101, 2095)
            timeWindow = randint(15, 60)
            ttToDest = ttMatrix[originQ,:]
            ttFromDest = ttMatrix[:,destinationQ]
            dest = ttToDest + ttFromDest < 45
            #destMatrix[i, dest] = 1

        print 'time taken - %.4f' %(time.time()-t)

        print 'travel skims read'
        raw_input()
        """
        print cols
        queryData = array([i[:] for i in query_gen])

        mask = array == None
        mask = ma.masked_values(queryData, None).mask
        queryData = array(queryData)
        queryData[mask] = 0
        data = DataArray(queryData, cols)
        from numpy import where
        t = time.time()
        print 'start'
        
        print sum(data.columns(['origin']).data == 101), sum(data.columns(['destination']).data == 1994)
        print 'end', time.time()-t
        raw_input()
        """

# Storing data ??                                                                                                             
# Linearizing data for calculating activity-travel choice attributes??                                                        
# how to update data like schedules, open periods etc.??

# create component list object
# iterate through component list
# - read the variable list
# - retrieve data
# - process the data further for retrieving accessibilities <>
# - update model objects/equation specifications for generic choice models
# - simulate
# - 


if __name__ == '__main__':
    fileloc = '/home/kkonduri/simtravel/test/vehown'
    componentManager = ComponentManager(fileLoc = "%s/config.xml" %fileloc)
    componentManager.establish_databaseConnection()
    componentManager.establish_cacheDatabase(fileloc, 'w')
    componentManager.run_components()
    #componentManager.read_data_store_in_hdf5()
    #componentManager.process_data_for_locs()
    raw_input()
    
    

