import copy
from lxml import etree
from numpy import array

from openamos.core.component.config_parser import ConfigParser
from openamos.core.database_management.query_browser import QueryBrowser
from openamos.core.errors import ConfigurationError
from openamos.core.data_array import DataArray


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


    def establish_databaseConnection(self):
        dbConfigObject = self.configParser.parse_databaseAttributes()
        self.queryBrowser = QueryBrowser(dbConfigObject)
        self.queryBrowser.dbcon_obj.new_connection()
        self.queryBrowser.create_mapper_for_all_classes()
        print 'Database Connection Established'

        
        """
        Example Query:
        hhld_class_name = 'households'
        query_gen, cols = queryBrowser.select_all_from_table(hhld_class_name)
        
        c = 0
        for i in query_gen:
            c = c + 1
            if c > 10:
                break
            print i.houseid
        print dir(i)
        """
        
        

    def run_components(self):
        componentList = self.configParser.parse_models()
        for i in componentList:
            print '\nRunning Component - %s' %(i.component_name)
            variableList = i.variable_list
            print '\tVariable List - ', len(variableList)
            data = self.prepare_data(variableList)        
            i.run(data)
            
        print data.data[:10]
            




    def prepare_data(self, variableList):
        columnDict = self.prepare_column_dictionary(variableList)
        print '\tColumn Dictionary: Tables - ', columnDict

        """
        queryColumnDict = {}
        for i in columnDict:
            if i.rfind('_r') == -1:
                queryColumnDict[i] = columnDict[i]
        print queryColumnDict
        """
        query_gen, cols = self.queryBrowser.select_join(columnDict, 'houseid')

        data = []
        c = 1
        for i in query_gen:
            c = c + 1
            if c > 10:
                break
            data.append(i)
        data = DataArray(array(data), cols)
            
        print '\tNumber of records fetched - ', data.data.shape
        return data
    
    def prepare_column_dictionary(self, variableList):
        columnDictionary = {}
        for i in variableList:
            tableName = i[0]
            colName = i[1]
            if tableName in columnDictionary:
                columnDictionary[tableName].append(colName)
            else:
                columnDictionary[tableName] = [colName]
                
        return columnDictionary

    def process_data_for_locs(self):
        """
        This method is called whenever there are location type queries involved as part
        of the model run. Eg. In a Destination Choice Model, if there are N number of 
        random location choices, and there is a generic MNL specifcation then in addition
        to generating the choices, one has to also retrieve the travel skims corresponding
        to the N random location choices.
        """
        pass


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
    fileloc = '/home/kkonduri/simtravel/test/VehOwn.xml'
    componentManager = ComponentManager(fileLoc = fileloc)
    componentManager.establish_databaseConnection()
    componentManager.run_components()

