import sys
import multiprocessing

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.core.errors import ArgumentsError

def run(fileLoc=None):
    """
    Runs the OpenAMOS program to simulate the activity-travel choices as 
    indicated by the models and their specifications in the config file.

    Please refer to OpenAMOS documentation on www.simtravel.wikispaces.asu.edu
    for guidance on setting up the configuration file.
    """
    print 'File location is %s'%fileLoc
    
    if fileLoc is not None:
	args = [fileLoc]
    else:
	args = sys.argv[1:]

    
    if len(args) < 1 or len(args) > 3:
        raise ArgumentsError, """The module accepts """\
            """only two arguments which are the location of the configuration """\
            """ file . e.g. /home/config.xml (linux machine) """\
            """or c:/testproject/config.xml (windows machine) and """\
            """skims flag and the number of parts to run in parallel """\

    fileLoc = args[0]

    if len(args) < 3:
	if len(args) == 2:
	    skipSettingSkimsLoc = int(args[1])
	else:
	    skipSettingSkimsLoc = 0	
        simulationManagerObject = SimulationManager(fileLoc = fileLoc)
	if skipSettingSkimsLoc == 0:
            queryBrowser = simulationManagerObject.setup_databaseConnection()
            simulationManagerObject.setup_cacheDatabase()
	    simulationManagerObject.setup_inputCacheTables()
	    simulationManagerObject.setup_outputCacheTables()
            simulationManagerObject.setup_tod_skims(queryBrowser)
            simulationManagerObject.setup_location_information(queryBrowser)
            simulationManagerObject.close_database_connection(queryBrowser)
	else:
	    simulationManagerObject.read_cacheDatabase()
        simulationManagerObject.parse_config()
        simulationManagerObject.clean_database_tables()
        simulationManagerObject.run_components()
        simulationManagerObject.close_cache_connection()
    else:
        numParts = int(args[2])
        simulationManagerObject = SimulationManager(fileLoc = fileLoc)
        simulationManagerObject.divide_database(numParts)
        simulationManagerObject.parse_config()
        simulationManagerObject.clean_database_tables()
	
	
	simulationManagerObject.setup_cacheDatabase()
	simulationManagerObject.setup_inputCacheTables()
    	queryBrowser = simulationManagerObject.setup_databaseConnection()
	simulationManagerObject.setup_tod_skims(queryBrowser)
    	simulationManagerObject.setup_location_information(queryBrowser)
    	simulationManagerObject.close_database_connection(queryBrowser)    
	

	# Everything related to parts from here on ....
        partsList = range(numParts)

	# Creating the output cache branches
	for partId in partsList:
            simulationManagerObject.setup_outputCacheTables(partId+1)
	    simulationManagerObject.clean_database_tables(partId+1)

       
        #Multiprocessing
        pool = multiprocessing.Pool()
        print partsList
        argsParallel = [(fileLoc, i+1) for i in partsList]
        print argsParallel

        pool.map(run_components_in_parallel, argsParallel)
        
        simulationManagerObject.collate_results(numParts)
        
def run_components_in_parallel(args):
    print args
    
    fileLoc = args[0]
    partId = args[1]
    simulationManagerObject = SimulationManager(fileLoc = fileLoc)
    simulationManagerObject.read_cacheDatabase()
    simulationManagerObject.parse_config()
    simulationManagerObject.run_components(partId)
    simulationManagerObject.close_cache_connection()
    


if __name__ == "__main__":
    sys.exit(run())
