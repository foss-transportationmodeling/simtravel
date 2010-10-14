import sys

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.core.errors import ArgumentsError

def main():
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
    simulationManagerObject.establish_databaseConnection()
    simulationManagerObject.establish_cacheDatabase('w')
    simulationManagerObject.run_components()
    simulationManagerObject.close_connections()
    
if __name__ == "__main__":
    sys.exit(main())
