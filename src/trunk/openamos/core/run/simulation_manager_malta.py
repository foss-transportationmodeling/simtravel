print '-- INSIDE OPENAMOS --'
import copy
import time
import os
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where, save, load

from openamos.core.component.config_parser_malta import ConfigParser
from openamos.core.database_management.cursor_query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.cache.dataset_malta import DB
from openamos.core.models.abstract_probability_model import AbstractProbabilityModel
from openamos.core.models.interaction_model import InteractionModel

#from multiprocessing import Process

class SimulationManager(object):
    """
    The class reads the configuration file, creates the component and model objects,
    and runs the models to simulate the various activity-travel choice processes.

    If the configObject is invalid, then a valid fileLoc is desired and if that fails
    as well then an exception is raised. In a commandline implementation, fileLoc will
    be passed.
    """

    def __init__(self):
	#, configObject=None, fileLoc=None, component=None):
	#TODO: REMOVE PLACEHOLDER 
	fileLoc = '/media/storage/workspace/openamos/configs/config_mag_malta.xml'
	configObject = None


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
            configObject = etree.parse(fileLoc)
        except AttributeError, e:
            raise ConfigurationError, """The file location is not a valid."""
        except IOError, e:
            print e
            raise ConfigurationError, """The path for configuration file was """\
                """invalid or the file is not a valid configuration file."""

        self.configObject = configObject
        self.configParser = ConfigParser(configObject) #creates the model configuration parser
        self.projectConfigObject = self.configParser.parse_projectAttributes()
        self.projectSkimsObject = self.configParser.parse_skims_tables()
        self.projectLocationsObject = self.configParser.parse_locations_table()
	self.householdStructureObject = self.configParser.parse_household_structure_info()

	self.setup_databaseConnection()
	self.setup_cacheDatabase()
	self.setup_location_information()
	self.setup_tod_skims()
	self.parse_config()
	#self.clean_database_tables()
        self.idCount = 0
        self.idList = []



    def setup_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        #self.queryBrowser.create_mapper_for_all_classes()
        #print 'Database Connection Established'


    """
    def setup_cacheDatabase(self, mode='w'):
        print "-- Creating a hdf5 cache database --"
        fileLoc = self.projectConfigObject.location
        self.db = DB(fileLoc, mode)
        if mode == 'w':
            self.db.create()
        # placeholders for creating the hdf5 tables 
        # only the network data is read and processed for faster 
        # queries
    """
    def setup_cacheDatabase(self):
	self.db = DB()

    def createSkimsTableFromDatabase(self, tableInfo):
        t = time.time()

	tableName = tableInfo.tableName

	colsList = []
	colsList.append(tableInfo.origin_var)
	colsList.append(tableInfo.destination_var)
	colsList.append(tableInfo.skims_var)

        data = self.queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

	fileLoc = self.projectConfigObject.location
	save('%s/%s.npy' %(fileLoc, tableName), data.data)

        print '\tTime taken to write to numpy cache format %.4f' %(time.time()-t)


    def setup_tod_skims(self):
        print "-- Processing Travel Skims --"
        for tableInfo in self.projectSkimsObject.tableDBInfoList:
            self.createSkimsTableFromDatabase(tableInfo)


    def createLocationsTableFromDatabase(self, tableInfo):
        t = time.time()
        
        colsList = [tableInfo.location_id_var] + tableInfo.locations_varsList

        tableName = tableInfo.tableName
        data = self.queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

	fileLoc = self.projectConfigObject.location
	save('%s/%s.npy' %(fileLoc, tableName), data.data)

        print '\tTime taken to write to numpy cache format %.4f' %(time.time()-t)

	    

    def setup_location_information(self):
        print "-- Processing Location Information --"
        self.createLocationsTableFromDatabase(self.projectLocationsObject)

    """
    def setup_household_structures(self):
	print "-- Processing Household Structures --"
	self.db.create
    """
 
    def parse_config(self):
        print "-- Parsing components and model specifications --"
        self.componentList = self.configParser.parse_models()
        #TODO: implement subsample runs 
        self.subsample = self.projectConfigObject.subsample

        # Printing models that were parsed
        modelCount = 0
        for comp in self.componentList:
            print '\n\tFor component - %s ' %(comp.component_name)
            print "\t -- Model list including model formulation and data filters if any  -- "
            print '\tPost Run Filters - ', comp.post_run_filter
            for mod in comp.model_list:
                print "\t\t - name:", mod.dep_varname, ",formulation:", mod.model_type, ",filter:", mod.data_filter
                modelCount += 1

        print "\tTotal of %s components and %s models will be processed" %(len(self.componentList), modelCount)
        print "\t - Note: Some models/components may have been added because of the way OpenAMOS framework is setup."
        #raw_input()

    def clean_database_tables(self):
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
                self.queryBrowser.delete_all(tableName)                            

        
    def run_components(self):
        t_c = time.time()
        
	tableOrderDict, tableNamesKeyDict = self.configParser.parse_tableHierarchy()

        for comp in self.componentList:
            t = time.time()
            print '\nRunning Component - %s; Analysis Interval - %s' %(comp.component_name,
                                                                       comp.analysisInterval)

            if comp.skipFlag:
                print '\tSkipping the run for this component'
                continue
            data = comp.pre_process(self.queryBrowser, self.subsample, 
                                    tableOrderDict, tableNamesKeyDict, 
                                    self.projectSkimsObject, self.householdStructureObject, self.db)
            if data is not None:
                # Call the run function to simulate the chocies(models)
                # as per the specification in the configuration file
                # data is written to the hdf5 cache because of the faster I/O
                nRowsProcessed, tripsProcessed = comp.run(data, self.projectSkimsObject, tableNamesKeyDict)
            
            # Write the data to the database from the hdf5 results cache
            # after running each component because the subsequent components
            # are often dependent on the choices generated in the previous components
            # run
                self.reflectToDatabase(comp.writeToTable, comp.keyCols, nRowsProcessed)
            print '-- Finished simulating component; time taken %.4f --' %(time.time()-t)
            #raw_input()
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f --' %(time.time()-t_c)


    def run_selected_components_for_malta(self, analysisInterval, tripInfoArrivals):
        print '-- INSIDE OpenAMOS generating activity-trvel records -- '
        raw_input ('\t Press any key to continue')
	t_c = time.time()


	tableOrderDict, tableNamesKeyDict = self.configParser.parse_tableHierarchy()


	# Get the two components one for dynamic activity simulation and another for extracting trips
	compObjects = []
        for comp in self.componentList:
	    if comp.component_name in ['ReconcileLongerTermSchedules', 'AfterSchoolActivities', 'DynamicNonMandatoryActivities']:
	        compObjects.append(comp)

	tripInfo = zeros((1,9))
	for comp in compObjects:
	    comp.analysisInterval = analysisInterval
	    t = time.time()
            print '\nRunning Component - %s; Analysis Interval - %s' %(comp.component_name,
                                                                       comp.analysisInterval)

            if comp.skipFlag:
                print '\tSkipping the run for this component'
                continue
	    fileLoc = self.projectConfigObject.location
            data = comp.pre_process(self.queryBrowser, self.subsample, 
                                    tableOrderDict, tableNamesKeyDict, 
                                    self.projectSkimsObject, self.householdStructureObject, self.db, fileLoc)

            if data is not None:
                # Call the run function to simulate the chocies(models)
                # as per the specification in the configuration file
                # data is written to the hdf5 cache because of the faster I/O
                tripInfo = comp.run(data, self.projectSkimsObject, tableNamesKeyDict, 
							self.queryBrowser, fileLoc)
                tripInfo[:,-4] = tripInfo[:,-4] - 100
                tripInfo[:,-3] = tripInfo[:,-4] - 100

	    else:
		tripInfo = zeros((1,9))
            # Write the data to the database from the hdf5 results cache
            # after running each component because the subsequent components
            # are often dependent on the choices generated in the previous components
            # run
                #self.reflectToDatabase(comp.writeToTable, comp.keyCols, nRowsProcessed)
		#tripInfo = self.tripInfoToMalta('trips_r', ['houseid', 'personid'], tripsProcessed)
            print '-- Finished simulating component; time taken %.4f --' %(time.time()-t)
            #raw_input()


        #print tripInfo

        tripInfo = tripInfo.astype(int)




        rowC = tripInfo.shape[0]
        
        ids = zeros((rowC, 4))
        ids[:,:-1] = tripInfo[:,:3]
        ids[:,-1] = array(range(rowC)) + self.idCount + 1

        self.idCount += rowC

        tripInfo = tripInfo[:,2:]
        tripInfo[:,0] = ids[:,-1]
        
        print tripInfo




	return tripInfo
        print '-- TIME TAKEN  TO COMPLETE ALL COMPONENTS - %.4f --' %(time.time()-t_c)




    def tripInfoToMalta(self, tableName, keyCols=[], nRowsProcessed=0):
        fileLoc = self.projectConfigObject.location
        table = self.db.returnTableReference(tableName)
        
        t = time.time()

        print '\tNumber of trips processed  - ', nRowsProcessed
        if nRowsProcessed == 0:
            return
        resArr = table[-nRowsProcessed:]

	colnames = table.colnames
	trips_data_array = zeros((nRowsProcessed, len(colnames)))
	for i in range(len(colnames)):
	    name = colnames[i]
	    trips_data_array[:,i] = resArr[name]

	print 'THIS IS WHAT WILL BE PASSED OVER TO MALTA'
	print trips_data_array
	return trips_data_array


    def reflectToDatabase(self, tableName, keyCols=[], nRowsProcessed=0):
        """
        This will reflect changes for the particular component to the database
        So that future queries can fetch appropriate run-time columns as well
        because the output is currently cached on the hard drive and the queries
        are using tables in the database which only contain the input tables 
        and hence the need to reflect the run-time caches to the database
        """

        fileLoc = self.projectConfigObject.location
        table = self.db.returnTableReference(tableName)
        
        t = time.time()

        print '\tNumber of rows processed for this component - ', nRowsProcessed
        if nRowsProcessed == 0:
            return
        resArr = table[-nRowsProcessed:]
        print """\t    creating the array object to insert into table - %s took - %.4f""" %(tableName,
                                                                                            time.time()-t)
        colsToWrite = table.colnames

        #self.queryBrowser.insert_into_table(resArr, colsToWrite, tableName, keyCols, chunkSize=100000)
        self.queryBrowser.copy_into_table(resArr, colsToWrite, tableName, keyCols, fileLoc)


    def close_connections(self):
        self.queryBrowser.dbcon_obj.close_connection()
        self.db.close()

if __name__ == '__main__':
    simulationObject = SimulationManager()
    simulationObject.run_selected_components_for_malta(195, None)


