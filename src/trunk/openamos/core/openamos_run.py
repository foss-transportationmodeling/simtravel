import sys

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.core.errors import ArgumentsError

def run_long_term_choices():
    """
    Runs the OpenAMOS program to simulate the activity-travel choices as 
    indicated by the models and their specifications in the config file.

    Please refer to OpenAMOS documentation on www.simtravel.wikispaces.asu.edu
    for guidance on setting up the configuration file.
    """
    args = sys.argv[1:]

    print args

    if len(args) <> 1:
        raise ArgumentsError, """The module accepts """\
            """only one argument which is the location of the configuration """\
            """file. e.g. /home/config.xml (linux machine) """\
            """or c:/testproject/config.xml (windows machine)"""

    
    simulationManagerObject = SimulationManager(fileLoc = args[0])
    simulationManagerObject.setup_databaseConnection()
    simulationManagerObject.setup_cacheDatabase('w')
    simulationManagerObject.setup_location_information()
    #simulationManagerObject.setup_tod_skims()
    simulationManagerObject.parse_config()
    simulationManagerObject.clean_database_tables()
    simulationManagerObject.run_components()
    simulationManagerObject.close_connections()

if __name__ == "__main__":
    sys.exit(run_long_term_choices())
