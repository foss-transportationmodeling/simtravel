import sys
import multiprocessing

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.core.errors import ArgumentsError

def run():
    """
    Runs the OpenAMOS program to simulate the activity-travel choices as 
    indicated by the models and their specifications in the config file.

    Please refer to OpenAMOS documentation on www.simtravel.wikispaces.asu.edu
    for guidance on setting up the configuration file.
    """
    args = sys.argv[1:]

    
    if len(args) < 1 or len(args) > 2:
        raise ArgumentsError, """The module accepts """\
            """only two arguments which are the location of the configuration """\
            """ file . e.g. /home/config.xml (linux machine) """\
            """or c:/testproject/config.xml (windows machine) and """\
            """and the number of parts to run in parallel """\

    fileLoc = args[0]

    if len(args) == 1:
        simulationManagerObject = SimulationManager(fileLoc = fileLoc)
        queryBrowser = simulationManagerObject.setup_databaseConnection()
        simulationManagerObject.setup_cacheDatabase()
        simulationManagerObject.setup_tod_skims(queryBrowser)
        simulationManagerObject.setup_location_information(queryBrowser)
        simulationManagerObject.close_database_connection(queryBrowser)
        simulationManagerObject.parse_config()
        simulationManagerObject.clean_database_tables()
        simulationManagerObject.run_components()
        simulationManagerObject.close_cache_connection()
    else:
        numParts = int(args[1])
        simulationManagerObject = SimulationManager(fileLoc = fileLoc)
        simulationManagerObject.divide_database(numParts)
        simulationManagerObject.parse_config()
        simulationManagerObject.clean_database_tables()
        
        """
        #Multiprocessing
        pool = multiprocessing.Pool()
        partsList = range(numParts)
        print partsList
        argsParallel = [(fileLoc, i+1) for i in partsList]
        print argsParallel
        pool.map(run_components_in_parallel, argsParallel)
        """
        simulationManagerObject.collate_results(numParts)
        
def run_components_in_parallel(args):
    print args
    
    fileLoc = args[0]
    partId = args[1]
    
    simulationManagerObject = SimulationManager(fileLoc = fileLoc)
    simulationManagerObject.setup_cacheDatabase(partId)
    queryBrowser = simulationManagerObject.setup_databaseConnection()
    simulationManagerObject.setup_tod_skims(queryBrowser)
    simulationManagerObject.setup_location_information(queryBrowser)
    simulationManagerObject.close_database_connection(queryBrowser)    
    simulationManagerObject.parse_config()
    simulationManagerObject.clean_database_tables(partId)
    simulationManagerObject.run_components(partId)
    simulationManagerObject.close_cache_connection()


if __name__ == "__main__":
    sys.exit(run())
