import copy
import time
import os
import traceback, sys
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.cursor_query_browser import QueryBrowser
from openamos.core.database_management.cursor_divide_data import DivideData
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.cache.dataset import DB
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.interaction_model import InteractionModel

from multiprocessing import Process

class SimulationManager(object):
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
            fileLoc = fileLoc.lower()
            self.fileLoc = fileLoc
            configObject = etree.parse(fileLoc)
        except AttributeError, e:
            raise ConfigurationError, """The file location is not a valid."""
        except IOError, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.fileLoc = fileLoc
        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser
        self.projectConfigObject = self.configParser.parse_projectAttributes()
        self.projectSkimsObject = self.configParser.parse_skims_tables()
        self.projectLocationsObject = self.configParser.parse_locations_table()


    def divide_database(self, numParts):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.divideDatabaseObj = DivideData(dbConfigObject)
        self.divideDatabaseObj.partition_data(numParts, 'households', 
                                              'persons', 'houseid')

    def collate_results(self, numParts):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.divideDatabaseObj = DivideData(dbConfigObject)
        self.divideDatabaseObj.collate_full_results(numParts)
        

    def setup_databaseConnection(self, partId=None):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        if partId is not None:
            dbConfigObject.database_name += '_%s' %(partId)
        
        queryBrowser = QueryBrowser(dbConfigObject)
        queryBrowser.dbcon_obj.new_connection()
        return queryBrowser

    def setup_cacheDatabase(self, partId=None, mode='w'):
        print "-- Creating a hdf5 cache database --"
        fileLoc = self.projectConfigObject.location
        if mode == 'w':
            self.db = DB(fileLoc)
            """
            if partId is not None:
                self.db = DB(fileLoc, partId)
            else:
                self.db = DB(fileLoc)
            #self.db.create()
            """

    def read_cacheDatabase(self):
        fileLoc = self.projectConfigObject.location
        self.db = DB(fileLoc, mode='a')

    def setup_inputCacheTables(self):
        self.db.create_inputCache()

    def setup_outputCacheTables(self, partId=None):
        self.db.create_outputCache(partId)

                
        # placeholders for creating the hdf5 tables 
        # only the network data is read and processed for faster 
        # queries


    def open_cacheDatabase(self, partId):
        fileLoc = self.projectConfigObject.location
        self.db = DB(fileLoc)
        self.db.load_input_output_nodes(partId)
        


    def setup_tod_skims(self, queryBrowser):
        print "-- Processing Travel Skims --"
	ti = time.time()
        for tableInfo in self.projectSkimsObject.tableDBInfoList:
	    if tableInfo.importFlag == "True":
		self.import_tod_skims(tableInfo, queryBrowser)
            
            self.db.createSkimsTableFromDatabase(tableInfo,
                       	                         queryBrowser)

	print "-- Caching and importing took a total of - %.4f" %(time.time()-ti)

    def import_tod_skims(self, tableInfo, queryBrowser):
	table_name = tableInfo.tableName
	# Delete contents
	queryBrowser.delete_all(table_name)                            

	# Insert records
	cols_listStr = "(%s, %s, %s)" %(tableInfo.origin_var,
					tableInfo.destination_var,
					tableInfo.skims_var)

	loc = tableInfo.fileLocation
	delimiter = tableInfo.delimiter

        try:
            ti = time.time()
    	    insert_stmt = ("""copy %s %s from '%s' """
                           """ delimiters '%s'""" %(table_name, cols_listStr, loc, 
	                                          delimiter))
	    print insert_stmt                                                                       
            result = queryBrowser.dbcon_obj.cursor.execute(insert_stmt)
            queryBrowser.dbcon_obj.connection.commit()
	    print "\t Time taken to insert skims into table - %s was 0.4f " %(table_name, time.time()-ti)
        except Exception, e:
            print e


    def setup_location_information(self, queryBrowser):
        print "-- Processing Location Information --"
        self.db.createLocationsTableFromDatabase(self.projectLocationsObject, 
                                                 queryBrowser)


    def parse_config(self):
        print "-- Parsing components and model specifications --"
        self.componentList = self.configParser.parse_models()
        #TODO: implement subsample runs 

        # Printing models that were parsed
        modelCount = 0
        for comp in self.componentList:
            #print '\n\tFor component - %s ' %(comp.component_name)
            #print "\t -- Model list including model formulation and data filters if any  -- "
            #print '\tPost Run Filters - ', comp.post_run_filter
            for mod in comp.model_list:
                #print "\t\t - name:", mod.dep_varname, ",formulation:", mod.model_type, ",filter:", mod.data_filter
                modelCount += 1

        print "\tTotal of %s components and %s models will be processed" %(len(self.componentList), modelCount)
        print "\t - Note: Some models/components may have been added because of the way OpenAMOS framework is setup."
        #raw_input()

    def clean_database_tables_for_parts(self, numParts):
        for i in range(numParts):
            self.clean_database_tables(partId=i+1)
            


    def clean_database_tables(self, partId=None):
        queryBrowser = self.setup_databaseConnection(partId)
            
        tableNamesDelete = []
        for comp in self.componentList:
	    if comp.skipFlag:
                continue
            # clean the run time tables
            #delete the delete statement; this was done to clean the tables during testing
            tableName = comp.writeToTable
            if tableName not in tableNamesDelete:
                tableNamesDelete.append(tableName)
                print "\tDeleting records in the output table - %s before simulating choices again" %(tableName)
                queryBrowser.delete_all(tableName)                            
        self.close_database_connection(queryBrowser)
        

    def run_components_for_parts(self, numParts):
        for i in range(numParts):
            self.run_components(partId=i+1)        

    def run_components(self, partId=None):
        configParser = copy.deepcopy(self.configParser)

        queryBrowser = self.setup_databaseConnection(partId)
        t_c = time.time()
        
	#tableOrderDict, tableNamesKeyDict = self.configParser.parse_tableHierarchy()

        try:
            lastTableName = None
            skimsMatrix = None
            uniqueIds = None
            for comp in self.componentList:
                t = time.time()
                print '\nRunning Component - %s; Analysis Interval - %s' %(comp.component_name,
                                                                           comp.analysisInterval)

                if comp.skipFlag:
                    print '\tSkipping the run for this component'
                    continue
                
                #Load skims matrix outside so that when there is temporal aggregation
                # of tod skims then loading happens only so many times

                tableName = self.identify_skims_matrix(comp)
                
                if tableName <> lastTableName and len(comp.spatialConst_list) > 0:
                    # Load the skims matrix
                    print """\tThe tod interval for the the previous component is not same """\
                        """as current component. """\
                        """Therefore the skims matrix should be reloaded."""
                    skimsMatrix, uniqueIds = self.load_skims_matrix(comp, tableName)
                    lastTableName = tableName

                elif tableName == lastTableName:
                    print """\tThe tod interval for the the previous component is same """\
                        """as current component. """\
                        """Therefore the skims matrix need not be reloaded."""

                data = comp.pre_process(queryBrowser,  
                                        skimsMatrix, uniqueIds,
                                        self.db)

                if data is not None:
                    # Call the run function to simulate the chocies(models)
                    # as per the specification in the configuration file
                    # data is written to the hdf5 cache because of the faster I/O
                    nRowsProcessed = comp.run(data, skimsMatrix, partId)
            
                    # Write the data to the database from the hdf5 results cache
                    # after running each component because the subsequent components
                    # are often dependent on the choices generated in the previous components
                    # run
	    
		    if (comp.readFromTable <> comp.writeToTable):
			if comp.analysisInterval == 1439:
			    createIndex = True
			elif comp.analysisInterval == None:
			    createIndex = True
			else:
			    createIndex = False
		    else:
		        createIndex = True

		    deleteIndex = True
					    
			

                    self.reflectToDatabase(queryBrowser, comp.writeToTable, comp.keyCols, 
                                           nRowsProcessed, partId, createIndex, deleteIndex)
                    #if nRowsProcessed > 0:
		    # 	raw_input()
                configParser.update_completedFlag(comp.component_name, comp.analysisInterval)
        
            
                print '-- Finished simulating component - %s; time taken %.4f --' %(comp.component_name,
                                                                                    time.time()-t)
        except Exception, e:
            print 'Exception occurred - %s' %e
            traceback.print_exc(file=sys.stdout)

        self.save_configFile(configParser, partId)
        self.close_database_connection(queryBrowser)
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f --' %(time.time()-t_c)


    def identify_skims_matrix(self, comp):
        ti = time.time()
        if len(comp.spatialConst_list) == 0:
            # When there are no spatial constraints to be processed
            # return an empty skims object
            tableName = None
            pass
        else:
            analysisInterval = comp.analysisInterval
        
            if comp.analysisInterval is not None:
                tableName = self.projectSkimsObject.lookup_table(analysisInterval)
            else:
                # Corresponding to the morning peak
                # currently fixed can be varied as need be
                tableName = self.projectSkimsObject.lookup_table(240)

        print '\tSkims Matrix Loaded in - %s' %(time.time()-ti)

        return tableName

    def load_skims_matrix(self, comp, tableName):
        const = comp.spatialConst_list[0]
        
        originColName = const.originField
        destinationColName = const.destinationField
        skimColName = const.skimField


        skimsMatrix, uniqueIds = self.db.returnTableAsMatrix(tableName,
                                                             originColName,
                                                             destinationColName,
                                                             skimColName)
        return skimsMatrix, uniqueIds
        





    def save_configFile(self, configParser, partId):
        if partId is not None:
            fileLoc = '%s_par_%s.xml' %(self.fileLoc[:-4], partId)
        else:
            fileLoc = self.fileLoc
        configFile = open(fileLoc, 'w')
        configParser.configObject.write(configFile, pretty_print=True)
        configFile.close()



    def reflectToDatabase(self, queryBrowser, tableName, keyCols=[], nRowsProcessed=0, partId=None, createIndex=True, deleteIndex=True):
        """
        This will reflect changes for the particular component to the database
        So that future queries can fetch appropriate run-time columns as well
        because the output is currently cached on the hard drive and the queries
        are using tables in the database which only contain the input tables 
        and hence the need to reflect the run-time caches to the database
        """

	

        fileLoc = self.projectConfigObject.location
        table = self.db.returnTableReference(tableName, partId)
        
        t = time.time()

	#print 'Create index - %s and Delete Index - %s' %(createIndex, deleteIndex)

        print '\tNumber of rows processed for this component - ', nRowsProcessed
        if nRowsProcessed == 0:
            return
        resArr = table[-nRowsProcessed:]
        print """\t    creating the array object to insert into table - %s took - %.4f""" %(tableName,
                                                                                            time.time()-t)
        colsToWrite = table.colnames

        #self.queryBrowser.insert_into_table(resArr, colsToWrite, tableName, keyCols, chunkSize=100000)
        queryBrowser.copy_into_table(resArr, colsToWrite, tableName, keyCols, fileLoc, partId, createIndex, deleteIndex)

        
    def close_database_connection(self, queryBrowser):
        queryBrowser.dbcon_obj.close_connection()
    
    def close_cache_connection(self):
        self.db.close()

if __name__ == '__main__':
    pass

