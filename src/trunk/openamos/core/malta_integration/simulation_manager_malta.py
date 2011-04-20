print '-- INSIDE OPENAMOS --'
import copy
import time
import os
from lxml import etree
from numpy import array, ma, ones, zeros, vstack, where, save, load

from openamos.core.malta_integration.config_parser_malta import ConfigParser
from openamos.core.database_management.cursor_query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray
from openamos.core.malta_integration.dataset_malta import DB
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
	fileLoc = '/home/kkonduri/simtravel/openamos/configs/config_mag_malta_dynamic.xml'
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

	self.setup_databaseConnection()
	self.setup_cacheDatabase()
	#self.setup_location_information()
	#self.setup_tod_skims()
	self.parse_config()
	self.clean_database_tables()
        self.idCount = 0
        self.idList = []



    def setup_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        #self.queryBrowser.create_mapper_for_all_classes()
        #print 'Database Connection Established'


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
	    if tableInfo.importFlag == "True":
		self.import_tod_skims(tableInfo)
            
            self.createSkimsTableFromDatabase(tableInfo)


    def import_tod_skims(self, tableInfo):
	table_name = tableInfo.tableName
	# Delete contents
	self.queryBrowser.delete_all(table_name)                            

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
	    #print insert_stmt                                                                       
            result = self.queryBrowser.dbcon_obj.cursor.execute(insert_stmt)
            self.queryBrowser.dbcon_obj.connection.commit()
        except Exception, e:
            print e


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


 
    def parse_config(self):
        print "-- Parsing components and model specifications --"
        self.componentList = self.configParser.parse_models()
        #TODO: implement subsample runs 
        self.subsample = self.projectConfigObject.subsample

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

    def clean_database_tables(self):
        tableNamesDelete = []
        for comp in self.componentList:
	    #if comp.skipFlag or comp.writeToTable == 'schedule_final_r' or comp.writeToTable == 'persons_arrived_r':
            #    continue
	    if comp.skipFlag or comp.writeToTable == 'schedule_final_r':
                continue
            # clean the run time tables
            #delete the delete statement; this was done to clean the tables during testing
            tableName = comp.writeToTable
            if tableName not in tableNamesDelete:
                tableNamesDelete.append(tableName)
                print "\tDeleting records in the output table - %s before simulating choices again" %(tableName)
                self.queryBrowser.delete_all(tableName)                            


    def run_selected_components_for_malta(self, analysisInterval, tripInfoArrivals=array([])):
        print '-- INSIDE OpenAMOS generating activity-trvel records -- '
        
        # To test python simulation_manager_cursor.py use dummy arrival info
        #tripInfoArrivals = array([1,2,3])

	if tripInfoArrivals <> array([]):
            dataVals = zeros((tripInfoArrivals.shape[0], 2))
            dataVals[:,0] = tripInfoArrivals
            dataVals[:,1] = analysisInterval - 1

            data = DataArray(dataVals, ['tripid', 'arrivaltime'])
            
	    print 'Following vehicles arrived and the corresponding arrival interval - '
	    print data
        else:
            data = None
            #raw_input ('\t Press any key to continue')
	t_c = time.time()

        # The analysis interval returned is the end of the analysis interval
        # In openamos everything is referenced to the start of the analysis Interval
        # openamos analysisInterval = above_analysisInterval - 1

	# Get the two components one for dynamic activity simulation and another for extracting trips
	compObjects = []
        for comp in self.componentList:
	    # Integrated application

	    """
	    if comp.component_name in ['DynamicNonMandatoryActivities', 'FinalReconciliationOfActivityTravelStartAdj', 
					'FinalReconciliationOfActivityTravelEndAdj', 'ExtractTravelEpisodes', 
					'ExtractBackgroundTravelEpisode', 'ExtractAllTravelEpisodes']:
	    """
	    # Sequential application
	    if comp.component_name in ['ArrivalTimeInformation', 'PersonsArrived', 'ArrivalTimeProcessing', 
					'DynamicNonMandatoryActivities', 'ExtractTravelEpisodes', 
					'ExtractBackgroundTravelEpisodes', 'ExtractAllTravelEpisodes']:

	        compObjects.append(comp)

        fileLoc = self.projectConfigObject.location
	for comp in compObjects:
            t = time.time()
            comp.analysisInterval = analysisInterval - 1
            print '\nRunning Component - %s; Analysis Interval - %s' %(comp.component_name,
                                                                       comp.analysisInterval)

                
            if comp.component_name == 'ArrivalTimeInformation':
                comp.db = self.db
            
            else:
                if comp.skipFlag:
                    print '\tSkipping the run for this component'
                    continue

                data = comp.pre_process(self.queryBrowser, 
                                        self.projectSkimsObject, self.db, fileLoc)

            if data is not None:
                #print 'inside here for component - ', comp.component_name
                # Call the run function to simulate the chocies(models)
                # as per the specification in the configuration file
                # data is written to the hdf5 cache because of the faster I/O
                tripInfo = comp.run(data, self.projectSkimsObject, 
                                    self.queryBrowser, fileLoc)

            else:
                tripInfo = zeros((1,10))
            print '\t-- Finished simulating component; time taken %.4f --' %(time.time()-t)

	if comp.component_name == 'ExtractAllTravelEpisodes':
	    # Reduce 100 to match TAZ notation of MALTA
	    tripInfo = tripInfo.astype(int)

	    #print 'RECORDS TO BE PASSED TO MALTA FROM COMPONENT WITHOUT ALTERING THE TAZ IDs- ',  comp.component_name
	    #print tripInfo

	    tripInfo[:,-5] = tripInfo[:,-5] - 100
            tripInfo[:,-4] = tripInfo[:,-4] - 100



	    print 'RECORDS TO BE PASSED TO MALTA FROM COMPONENT %s AFTER ALTERING THE TAZ IDs ' %(comp.component_name)
	    print tripInfo.shape
            print tripInfo[-3:, [0, -5, -4]]
            #raw_input('This is the shape --')

	return tripInfo





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

    def close_connections(self):
        self.queryBrowser.dbcon_obj.close_connection()
        self.db.close()

if __name__ == '__main__':
    simulationObject = SimulationManager()

    simulationObject.run_selected_components_for_malta(0)
    simulationObject.run_selected_components_for_malta(1)
    simulationObject.run_selected_components_for_malta(2)


