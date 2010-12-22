'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

import copy
import time
import re
from lxml import etree
from numpy import array

from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.log_linear_regression_model import LogLinearRegressionModel
from openamos.core.models.stochastic_frontier_regression_model import StocFronRegressionModel
from openamos.core.models.log_stochastic_frontier_regression_model import LogStocFronRegressionModel
from openamos.core.models.count_regression_model import CountRegressionModel
from openamos.core.models.logit_choice_model import LogitChoiceModel
from openamos.core.models.ordered_choice_model import OrderedModel
from openamos.core.models.probability_distribution_model import ProbabilityModel
from openamos.core.models.nested_logit_choice_model import NestedLogitChoiceModel
from openamos.core.models.interaction_model import InteractionModel
from openamos.core.models.model_components import Specification
from openamos.core.models.count_regression_model_components import CountSpecification
from openamos.core.models.ordered_choice_model_components import OLSpecification
from openamos.core.models.nested_logit_model_components import NestedChoiceSpecification, NestedSpecification
from openamos.core.models.error_specification import LinearRegErrorSpecification
from openamos.core.models.error_specification import StochasticRegErrorSpecification
from openamos.core.models.model import SubModel

from openamos.core.component.abstract_component import AbstractComponent

from openamos.core.activity_travel.activity_travel_components import HistoryInfo, HouseholdStructureInfo

from openamos.core.spatial_analysis.spatial_query_components import SpatioTemporalConstraint, PrismConstraints

from openamos.core.travel_skims.travel_skims_components import TravelSkimsInfo
from openamos.core.travel_skims.locations_components import LocationsInfo

from openamos.core.database_management.database_configuration import DataBaseConfiguration

from openamos.core.project_configuration import ProjectConfiguration
from openamos.core.data_array import DataArray, DataFilter
from openamos.core.errors import ConfigurationError 

class ConfigParser(object):
    """
    The class defines the parser for translating the model configuration
    file into python objects for execution.  
    """

    def __init__(self, configObject, component=None):
        """
        The configObject should be an etree.ElementBase object, component is the
        keyword for the component until which componentList is desired. The component
        entry will be updated further to pick and choose components to run.
        """
        #TODO: filter_conditons, run_until conditions

        
        if not isinstance(configObject, etree._ElementTree):
            raise ConfigurationError, """The configuration input is not a valid """\
                """etree.ElementBase object""" 
                
        self.configObject = configObject
        self.componentName = component

    def update_completedFlag(self, component_name, analysisInterval=None):
        self.iterator = self.configObject.getiterator('Component')

        for compElement in self.iterator:
            if compElement.get('name') == component_name:
                if analysisInterval is None:
                    print 'OLD FLAG _ ', compElement.get('completed')
                    compElement.set('completed', "True")
                    compElement.set('skip', "True")
                    print 'NEW FLAG _ ', compElement.get('completed')


                if analysisInterval is not None:
                    analysisIntervalElement = compElement.find('AnalysisInterval')
                    print 'OLD ANALYSIS INTERVAL START _ ', analysisIntervalElement.get('start')
                    analysisIntervalElement.set('start', str(analysisInterval + 1))
                    print 'updated ANALYSIS INTERVAL START _ ', analysisIntervalElement.get('start')
                    print dir(analysisIntervalElement)
                
                    endIntervalValue = int(analysisIntervalElement.get('end'))
                    
                    if endIntervalValue == analysisInterval + 1:
                        print 'OLD FLAG _ ', compElement.get('completed')
                        compElement.set('completed', "True")
                        compElement.set('skip', "True")
                        print 'NEW FLAG _ ', compElement.get('completed')                    


    def parse_models(self):
        self.iterator = self.configObject.getiterator("Component")
        componentList = []
        
        for i in self.iterator:
            componentIntermediateList = self.parse_analysis_interval_and_create_component(i)
            componentList += componentIntermediateList
            if i.attrib['name'] == self.componentName:
                return componentList

        return componentList

    def parse_projectAttributes(self):
        print "-- Parse project attributes --"
        projectElement = self.configObject.find('Project')
        projectName = projectElement.get('name')
        projectLocation = projectElement.get('location')
        projectSubsample = projectElement.get('subsample')
        if projectSubsample is not None:
            projectSubsample = int(projectSubsample)

        projectConfigObject = ProjectConfiguration(projectName,
                                                   projectLocation,
                                                   projectSubsample)
            
        return projectConfigObject

    def parse_databaseAttributes(self):
        print "-- Parse database attributes --"
        dbConfig_element = self.configObject.find('DBConfig')
        protocol = dbConfig_element.get('dbprotocol')
        host = dbConfig_element.get('dbhost')
        dbname = dbConfig_element.get('dbname')
        username = dbConfig_element.get('dbusername')
        password = dbConfig_element.get('dbpassword')

        dbConfigObject = DataBaseConfiguration(protocol,
                                               username,
                                               password,
                                               host,
                                               dbname)
        return dbConfigObject
        
    def parse_tableHierarchy(self):
        print "-- Parse table hierarchy --"
        dbTables_element = self.configObject.find('DBTables')
        tableIterator = dbTables_element.getiterator("Table")
        tableOrderDict = {}
        tableNamesKeyDict = {}
        for table_element in tableIterator:
            tableName = table_element.get("table")
            tableKeys = table_element.get("key")
            tableKeys = re.split('[,]', tableKeys)
            countKeys = table_element.get("count_key")
            if countKeys is not None:
                countKeys = re.split('[,]', countKeys)
            else:
                countKeys = []

            tableOrder = table_element.get("order")
            if tableOrder is not None:
                tableOrder = int(tableOrder)
                tableOrderDict[tableOrder] = [tableName, tableKeys]
            tableNamesKeyDict[tableName] = [tableKeys, countKeys]
        return tableOrderDict, tableNamesKeyDict


    def parse_skims_tables(self):
        print "-- Parse skims tables' Time of Day information --"
        skims_element = self.configObject.find("TravelSkims")
        referenceTablename = skims_element.get("reference_tablename")
        indb_flag = skims_element.get("indb")

        periodIterator = skims_element.getiterator("Period")

        travelSkimsLookup = TravelSkimsInfo(referenceTablename, indb_flag)
        
        travelSkimsPeriodDBInfoList = []
        for period_element in periodIterator:
            tablename = period_element.get("tablename")
            target_tablename = period_element.get("target_tablename")
            origin_var = period_element.get("origin_var")
            destination_var = period_element.get("destination_var")
            skim_var = period_element.get("skim_var")
            interval_start = int(period_element.get("intervalStart"))
            interval_end = int(period_element.get("intervalEnd"))

            travelSkimsLookup.add_tableInfoToList(tablename, origin_var,
                                                  destination_var,
                                                  skim_var,
                                                  interval_start,
                                                  interval_end,
                                                  target_tablename)
                                                  
        return travelSkimsLookup


    def parse_locations_table(self):
        print "-- Parse locations table --"
        locations_element = self.configObject.find("Locations")
        referenceTablename = locations_element.get("reference_tablename")
        tablename = locations_element.get("tablename")
        location_var = locations_element.get("location_var")
        indb_flag = locations_element.get("indb")
	
	variablesIterator = locations_element.getiterator("LocationVariable")
	
	variablesList = []
	for var_element in variablesIterator:
	    varName = var_element.get("var")
	    variablesList.append(varName)


        locationsInfo = LocationsInfo(tablename, referenceTablename, 
                                      location_var, variablesList)

        return locationsInfo


    def parse_household_structure_info(self):
        print "-- Parse household structures --"
        structures_element = self.configObject.find("HouseholdStructure")
        tablename = structures_element.get('tablename')
        houseid = structures_element.get('houseid')
        personid = structures_element.get('personid')

        #prim_keys = re.split('[,]', keys_element)
        
        structuresIterator = structures_element.getiterator('Structure')
        
        structuresDict = {}
        for structure in structuresIterator:
            name = structure.get("name")
            var = structure.get("var")
            value = structure.get("value")
            
            structuresDict[name] = [var,int(value)]
            
        householdStructureInfoObject = HouseholdStructureInfo(tablename,
                                                              houseid,
                                                              personid,
                                                              structuresDict)
        return householdStructureInfoObject

    def parse_analysis_interval_and_create_component(self, component_element):
        ti = time.time()
        interval_element = component_element.find("AnalysisInterval")
        componentList = []
        if interval_element is not None:
            startInterval = interval_element.get("start")
            startInterval = int(startInterval)

            endInterval = interval_element.get("end")
            endInterval = int(endInterval)



            repeatComponent = self.create_component(component_element)

            for i in range(endInterval - startInterval):
                tempComponent = copy.deepcopy(repeatComponent)
                for model in tempComponent.model_list:
                    model.seed +=  i 
                tempComponent.analysisInterval = startInterval + i
                componentList.append(tempComponent)

        else:
            component = self.create_component(component_element)
            componentList.append(component)
        print '\t\tTime taken to parse across all analysis intervals %.4f' %(time.time()-ti)

        return componentList

    def return_delete_records_criterion(self, component_element):
        delete_records_element = component_element.find("DeleteRecords")
        if delete_records_element is not None:
            delete_criterion = delete_records_element.get("value")
            if delete_criterion == "True":
                delete_criterion = True
            elif delete_criterion == "False":
                delete_criterion = False
        else:
            delete_criterion = None

        return delete_criterion

    
    def create_component(self, component_element):
        comp_name, comp_read_table, comp_write_table, comp_keys = self.return_component_attribs(component_element)

        deleteCriterion = self.return_delete_records_criterion(component_element)
        
	print "Parsing Component - %s" %(comp_name)

        spatialConstIterator = component_element.getiterator("SpatialConstraints")
        spatialConst_list = []
        for i in spatialConstIterator:
            spatialConst = self.return_spatial_query(i)
            spatialConst_list.append(spatialConst)


        dynamicSpatialConstIterator = component_element.getiterator("DynamicSpatialConstraints")
        dynamicSpatialConst_list = []
        for i in dynamicSpatialConstIterator:
            dynamicSpatialConst = self.return_spatial_query(i)
            dynamicSpatialConst_list.append(dynamicSpatialConst)

            
        consistencyChecks_element = component_element.find("ConsistencyChecks")
        if consistencyChecks_element is not None:
            post_run_filter = self.return_filter_condition_list(consistencyChecks_element)
        else:
            post_run_filter = None
            
        historyInfo_element = component_element.find("HistoryInformation")
        if historyInfo_element is not None:
            historyInfoObject = self.return_history_info(historyInfo_element)
        else:
            historyInfoObject = None
        

        modelsIterator = component_element.getiterator("Model")
        self.model_list = []
        self.component_variable_list = []
        for i in modelsIterator:
            self.create_model_object(i)
            self.create_linear_object_for_locations(i, spatialConst_list)
            #component_variable_list = (component_variable_list 
            #                           + variable_list)
            #model_list.append(model)
        #print self.component_variable_list


        #if spatialConst_list == []:
        #    spatialConst_list = None


        dependencyAllocationFlag = component_element.get("dependency")
        if dependencyAllocationFlag == "True":
            dependencyAllocationFlag = True
        else:
            dependencyAllocationFlag = False

        skipFlag = component_element.get("skip")
        if skipFlag == "True":
            skipFlag = True
        else:
            skipFlag = False


        self.component_variable_list = list(set(self.component_variable_list))
        component = AbstractComponent(comp_name, self.model_list, 
                                      self.component_variable_list, 
                                      comp_read_table,
                                      comp_write_table,
                                      comp_keys,
                                      spatialConst_list,
                                      dynamicSpatialConst_list,
                                      history_info = historyInfoObject,
                                      post_run_filter=post_run_filter,
                                      delete_criterion=deleteCriterion,
                                      dependencyAllocationFlag = dependencyAllocationFlag,
                                      skipFlag = skipFlag)
        return component



        
    def return_history_info(self, history_element):
        historyVarsIterator = history_element.getiterator("HistoryVar")
        histTableName = history_element.get('table')

        histAggVar = history_element.get('history_var')

        histVarAggConditions = {}
        for histVar_element in historyVarsIterator:
            conditions = self.return_var_values_list(histVar_element)
            histVar = histVar_element.get('var')
            histVarAggConditions[histVar] = conditions

        historyInfoObject = HistoryInfo(histTableName, histAggVar, histVarAggConditions)
        return historyInfoObject


    def return_var_values_list(self, histVar_element):
        histVarValuesIterator = histVar_element.getiterator('Aggregate')
        
        conditions = []
        for i in histVarValuesIterator:
            value = i.get('value')
            conditionVariable = i.get('condition_var')
            if value is not None:
                conditions.append('%s=%s' %(conditionVariable, value))

        return conditions




    def create_model_object(self, model_element):
        model_formulation = model_element.attrib['formulation']
	print "\tParsing model - %s, formulation - %s " %(model_element.get('name'), model_element.get('formulation'))
        #print model_formulation
        
        if model_formulation == 'Regression':
            self.create_regression_object(model_element)
            
        if model_formulation == 'Count':
            self.create_count_object(model_element)
        
        if model_formulation == 'Multinomial Logit':
            if model_element.find('AlternativeSet') is None:
                self.create_multinomial_logit_object(model_element)
            else:
                self.create_multinomial_logit_object_generic_locs(model_element)
    
        if model_formulation == 'Nested Logit':
            self.create_nested_logit_object(model_element)

        if model_formulation == 'Ordered':
            self.create_ordered_choice_object(model_element)

        if model_formulation == 'Probability Distribution':
            self.create_probability_object(model_element)


    def process_seed(self, model_element):
        seed = model_element.get('seed')
        if seed is not None:
            return int(seed)
        else:
            return 1

    def create_regression_object(self, model_element):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element)

        #variable list required for running the model
        variable_list = []

        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)
        dep_varname = depvariable_element.get('var')

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #print dep_varname, '----variable Name -----'
        choice = [dep_varname]

        # Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = coeff_dict 

        variable_list = variable_list + vars_list

        #print choice, coefficients
        # specification object
        specification = Specification(choice, coefficients)

        # Reading the vertex
        vertex = model_element.get('vertex')

        # Reading the threshold for the stochastic frontier
        threshold = model_element.get('threshold')

	if threshold == None:
            threshold = 0
        else:
            threshold = float(threshold)

        
        # Creating the variance matrix
        model_type = model_element.get('type')
        
        varianceIterator = model_element.getiterator('Variance')
        
        if model_type in ['Linear', 'Log Linear'] :
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance, vertex, threshold)         
            if model_type == 'Linear':
                model = LinearRegressionModel(specification, errorSpec)
            else:
                model = LogLinearRegressionModel(specification, errorSpec)
        """
        if model_type == 'Log Linear':
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance)         
            model = LogLinearRegressionModel(specification, errorSpec)
        """

        if model_type in ['Stochastic Frontier', 'Log Stochastic Frontier']:
            for i in varianceIterator:
                variance_type = i.get('type', default=None)
                if variance_type == None:
                    norm_variance = float(i.get('value'))
                elif variance_type == 'Half Normal':
                    half_norm_variance = float(i.get('value'))
                    
            variance = array([[norm_variance, 0],[0, half_norm_variance]])
            errorSpec = StochasticRegErrorSpecification(variance, vertex, threshold)

            if model_type == 'Stochastic Frontier':
                model = StocFronRegressionModel(specification, errorSpec)                 
            else:
                model = LogStocFronRegressionModel(specification, errorSpec)                                 

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model_type = 'regression'
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)
        
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_count_object(self, model_element):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element)
        #variable list required for running the model
        variable_list = []
        
        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = coeff_dict

        variable_list = variable_list + vars_list

        # dependent variable
        variable = model_element.get('name')
        
        # alternatives and values-categorues lookup
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            #print alternative, value

        if len(values) == 0:
            values = None

        # specification object
        specification = CountSpecification(choice, coefficients)
        
        # filters
        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)


        model_type = 'choice'
        model = CountRegressionModel(specification)
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter, 
                                values=values, seed=seed, filter_type=filter_type,
                                run_filter_type=run_filter_type)
        
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list
        

    def create_multinomial_logit_object(self, model_element):
        """
        Accomodates both generic and alternative specific where the
        alternatives are spelled out
        """
        #print 'INSIDE LOGIT MODEL NOTTTT FOR LOCATIONS'

        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element)

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #print dep_varname, "inside, regiular"

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        coefficients_list = []
        values = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            if model_type == 'Alternative Specific':
                coeff_dict, vars_list = self.return_coeff_vars(i)
                coefficients_list = coefficients_list + coeff_dict
                variable_list = variable_list + vars_list
        if model_type <> 'Alternative Specific':
            coeff_dict, vars_list = self.return_coeff_vars(model_element)
            coefficients_list = coefficients_list + coeff_dict
            coefficients_list = coefficients_list*len(choice)
            variable_list = variable_list + vars_list
        
        if len(values) == 0:
            values = None

        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)
    
        model = LogitChoiceModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, values=values, seed=seed, 
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)#Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_multinomial_logit_object_generic_locs(self, model_element):
        """
        Accomodates alternative specific where the
        alternatives are not spelled out. Like for location choices
        """

        #print 'INSIDE LOGIT MODEL FOR LOCATIONS'

        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element)

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #print dep_varname, 'other one'
        # alternatives
        altSetElement = model_element.find('AlternativeSet')
        alternativeSet = int(altSetElement.get('count'))
        #print 'alternativeSet --->', alternativeSet
        choice = []
        coefficients_list = []
        values = []
        
        for i in range(alternativeSet):
            alternative = dep_varname + str(i+1)
            choice.append(alternative)
            value = i + 1
            values.append(float(value))
            #variable_list.append(('temp', alternative))
            
        coeff_list, vars_list = self.return_coeff_vars(model_element, alternativeSet)
        #print vars_list, 'VARIABLES LISTTTTTTTT'
        #print coeff_list, 'COEFFICIENTS LISTTTTTTT'

        #print dep_varname

        # logit specification object
        specification = Specification(choice, coeff_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)
    
        model = LogitChoiceModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, values=values, seed=seed, 
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)#Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_linear_object_for_locations(self, model_element, spatialConst_list):
        """
        creates linear combination objects for locations and travel times
        """

        seed = self.process_seed(model_element)
        altSetElement = model_element.find('AlternativeSet')        
        if altSetElement is None or spatialConst_list is None: 
            return 

        for const in spatialConst_list:
            if const.countChoices is not None:
                depvariable_element = model_element.find('DependentVariable')
                dep_varname = depvariable_element.get('var')
                
                countChoices = const.countChoices
                destinationField = const.destinationField

                #Filter set
                filter_set_element = model_element.find('FilterSet')
                if filter_set_element is not None:
                    filter_type = filter_set_element.get('type')
                else:
                    filter_type = None

                #Filter set
                run_filter_set_element = model_element.find('RunUntilConditionSet')
                if run_filter_set_element is not None:
                    run_filter_type = run_filter_set_element.get('type')
                else:
                    run_filter_type = None

                dataFilter = self.return_filter_condition_list(model_element)
                runUntilFilter = self.return_run_until_condition(model_element)

                choice = [dep_varname]
                variance = array([[0.0]])
                errorSpec = LinearRegErrorSpecification(variance)         
                model_type = 'regression'

                variableIterator = model_element.getiterator('Variable')
                rep_var_list = []
                for variable_element in variableIterator:
                    rep_var = variable_element.get('repeat')

                    if rep_var is not None:
                        rep_var_list += re.split('[,]', rep_var)

                

                for i in range(countChoices):
                   
                    # additional data filter
                    dataFilterLoc = DataFilter(dep_varname, 'equals', i+1)

                    #Models to populate the travel time to destination variable
                    var = const.asField
                    coefficients = [{'%s%s'%(var, i+1):1}]
                    specification = Specification([var], coefficients)
                    model = LinearRegressionModel(specification, errorSpec)
                    model_type = 'regression'
                    model_object = SubModel(model, model_type, var, dataFilter + [dataFilterLoc], 
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)

                    #Models to populate the travel time from destination variable
                    var = 'tt_from' 
                    coefficients = [{'%s%s'%(var, i+1):1}]
                    specification = Specification([var], coefficients)
                    model = LinearRegressionModel(specification, errorSpec)
                    model_type = 'regression'
                    model_object = SubModel(model, model_type, var, dataFilter + [dataFilterLoc], 
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)

                    #Models to populate the location id variable
                    coefficients = [{'%s%s'%(destinationField, i+1):1}]
                    specification = Specification(choice, coefficients)                
                    model = LinearRegressionModel(specification, errorSpec)
                    model_object = SubModel(model, model_type, dep_varname, dataFilter + [dataFilterLoc], 
                                            runUntilFilter, seed=seed, filter_type=filter_type,
                                            run_filter_type=run_filter_type)
                    self.model_list.append(model_object)


    def create_nested_logit_object(self, model_element):
        #variable list required for running the model
        variable_list = []
        seed = self.process_seed(model_element)
        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')        
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        #Specification dict
        spec_build_ind = {}


        #building the nest structure
        nest_struct = {}
        spec_dict = {}
        alts = []
        values = []
        alternativeIterator = model_element.getiterator('Alternative')
        for i in alternativeIterator:
            name = i.get('id')
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            coeff_dict, vars_list = self.return_coeff_vars(i)
            variable_list = variable_list + vars_list
            spec = NestedChoiceSpecification([name], coeff_dict)
            spec_build_ind[name] = spec

            branch = i.get('branch')

            parents = branch.strip().split('/')
            
            if parents == ['root']:
                try:
                    val = nest_struct['root']
                    val.append(name)
                    nest_struct['root'] = val
                except:
                    nest_struct['root'] = [name]


            for j in range(len(parents)-1):
                nest = parents[j]
                # Updating parent entries
                try:
                    val = nest_struct[nest]
                    if parents[j+1] not in val:
                        val.append(parents[j+1])
                        nest_struct[nest] = val
                except:
                    nest_struct[nest] = [parents[j+1]]


                # Updating alternative entries
                try:
                    val = nest_struct[parents[-1]]
                    val.append(name)
                    nest_struct[parents[-1]] = val
                except:
                    nest_struct[parents[-1]] = [name]
                
        if len(values) == 0:
            values = None

        for i in nest_struct:
            if i not in alts:
                alts.append(i)
            for j in nest_struct[i]:
                if j not in alts:
                    alts.append(j)

        for i in alts:
            if i not in spec_build_ind.keys() and i <> 'root':
                spec = self.create_spec(i)
                spec_build_ind[i] = spec

        spec_dict = copy.deepcopy(nest_struct)

        for i in nest_struct:
            vals = spec_dict.pop(i)
            vals_spec = []
            for j in vals:
                vals_spec.append(spec_build_ind[j])
            if i <> 'root':
                i = spec_build_ind[i]
            spec_dict[i] = vals_spec
                


        branchIterator = model_element.getiterator('Branch')
        for i in branchIterator:
            name = i.get('name')
            logsum = float(i.get('coeff'))

            for j in spec_dict.keys():
                if j <> 'root':
                    if j.choices == [name.lower()]:
                        j.logsumparameter = logsum



        for i in spec_dict:
            if i <> 'root':
                #print i.choices
                #print i.logsumparameter
                pass
            else:
                #print i
                pass
            for j in spec_dict[i]:
                #print j.choices
                pass
                
                    
        #print nest_struct
        #print alts
        #print spec_build_ind
        
        #print '-----', spec_dict
        
        specification = NestedSpecification(spec_dict)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = NestedLogitChoiceModel(specification)
        model_type = 'choice'
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type)


        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list

        
    def create_spec(self, name):
        choices = name
        coefficients = {'ONE':0}
        
        spec = NestedChoiceSpecification([choices], [coefficients])
        return spec

        
    
    def create_ordered_choice_object(self, model_element):
        #model type
        model_type = model_element.get('type')
        seed = self.process_seed(model_element)        
        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        coefficients_list = []
        threshold_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            threshold = i.get('threshold')
            if threshold is not None:
                threshold_list.append(float(threshold))
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients_list = coefficients_list + coeff_dict
        variable_list = vars_list
        
        if len(values) == 0:
            values = None

        #print dep_varname, model_type
                    
        # logit specification object
        if model_type == 'Logit':
            #print coefficients_list
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())
        else:
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)            

        model = OrderedModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type) #Model Object
    
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list
        #print self.component_variable_list
        #print 'HERE IS OREDERED LOGIT'
        #raw_input()

    
    def create_probability_object(self, model_element):
        #variable_list_required for running the model
        variable_list = []
        seed = self.process_seed(model_element)
        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname = depvariable_element.get('var')
        #dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Filter set
        filter_set_element = model_element.find('FilterSet')
        if filter_set_element is not None:
            filter_type = filter_set_element.get('type')
        else:
            filter_type = None

        #Filter set
        run_filter_set_element = model_element.find('RunUntilConditionSet')
        if run_filter_set_element is not None:
            run_filter_type = run_filter_set_element.get('type')
        else:
            run_filter_type = None

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        values = []
        coefficients_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            value = i.get('value')
            if value is not None:
                values.append(float(value))
            coeff_dict, vars_list = self.return_coeff_vars(i)
            coefficients_list = coefficients_list + coeff_dict
            variable_list = variable_list + vars_list
        if len(values) == 0:
            values = None
        #print coefficients_list
        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition_list(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = ProbabilityModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, 
                                runUntilFilter, values=values, seed=seed,
                                filter_type=filter_type,
                                run_filter_type=run_filter_type) #Model Object
    
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list

    
    def return_table_var(self, var_element):
        return var_element.get('table'), var_element.get('var')
        
    def return_coeff_vars(self, element, alternativeSet=None):
        variableIterator = element.getiterator('Variable')
        vars_list = []
        coeff_ret = []

        for i in variableIterator:
            dep_var = self.check_for_interaction_terms(i, alternativeSet)
            if dep_var is not None:
                #print '\t\tINTERACTION TERM', dep_var
                for j in dep_var:
                    coeff_dict = {}
                    coeff = i.get('coeff')
                    #print coeff
                    #coeff_dict[j] = float(coeff)
                    if len(coeff_ret) < len(dep_var):
                        coeff_dict[j] = float(coeff)
                        coeff_ret.append(coeff_dict)
                    else:
                        coeff_ret[dep_var.index(j)][j] = float(coeff)
                #print coeff_ret, 'new repeated INTERACTION TERMSSSSSSSSSSSSSSSSSSSSSSSSS'
            else:
                #print 'NOT AN INTERACTION TERM'
                coeff_dict = {}
                vars_list.append(self.return_table_var(i))
                varname = i.get('var')
                coeff = i.get('coeff')
                if len(coeff_ret) < 1:
                    coeff_dict[varname] = float(coeff)
                    coeff_ret.append(coeff_dict)
                else:
                    coeff_ret[0][varname] = float(coeff)
                #print coeff_ret
        #print vars_list, 'sent back', coeff_ret
        return coeff_ret, vars_list

    def check_for_interaction_terms(self, var_element, alternativeSet):
        variable_list = []
        coeff_dict = {}
        dep_varname = ''

        #print 'alternativeSet', alternativeSet

        if var_element.get('interaction') is not None:
            rep_var = var_element.get('repeat')
            if rep_var is not None:
                rep_var_list = re.split('[,]', rep_var)
            else:
                rep_var_list = []
        
            #print 'REPEAT VARIABLE LIST -->', rep_var_list
                
            #var_element.get('interaction')
            varnames = re.split('[,]', var_element.get('var'))
            #print 'varnames', varnames
            tablenames = re.split('[,]', var_element.get('table'))
            #print 'tablenames', tablenames
            
            rep_var_table_list = []
            for i in rep_var_list:
                #find and remove the repeate variable from varnames
                var_ind = varnames.index(i)
                varnames.pop(var_ind)

                #find the tablenames for the ones that are to be repeated
                rep_var_table_list.append(tablenames.pop(var_ind))
            #print 'REPEAT TABLE LIST', rep_var_table_list

            for i in range(len(varnames)):
                variable_list.append((tablenames[i], varnames[i]))
                dep_varname = dep_varname + varnames[i].title()
                coeff_dict[varnames[i]] = 1
            #print 'VARIABLE LIST', variable_list

            if alternativeSet is None:
                choice = [dep_varname]
                coefficients_list = [coeff_dict]
                # specification object
                specification = Specification(choice, coefficients_list)
                
                model = InteractionModel(specification) 
                model_type = 'regression'                   #Type of Model 
                model_object = SubModel(model, model_type, dep_varname) #Model Object
                dep_var = [dep_varname]
                self.model_list.append(model_object)
                self.component_variable_list = self.component_variable_list + variable_list            
            else:
                dep_var = []
                dep_rep_varname = copy.deepcopy(dep_varname)
                for j in range(alternativeSet):
                    dep_varname = dep_rep_varname
                    
                    coeffs_rep = copy.deepcopy(coeff_dict)

                    for k in range(len(rep_var_list)):
                        #variable_list.append((rep_var_table_list[k], rep_var_list[k]+str(j+1)))
                        variable_list.append(('temp', rep_var_list[k]+str(j+1)))
                        dep_varname = dep_varname + rep_var_list[k]
                        coeffs_rep[rep_var_list[k]+str(j+1)] = 1
                        
                    dep_varname = dep_varname + str(j+1)
                    choice = [dep_varname]
                    coefficients_list = [coeffs_rep]
                    specification = Specification(choice, coefficients_list)
                    
                    model = InteractionModel(specification)
                    model_type = 'regression'
                    model_object = SubModel(model, model_type, dep_varname)
                    
                    dep_var.append(dep_varname)
            #print dep_var
            #return model_object, variable_list
                    #print '\t\t\t\tFOR THE INTERACTION TERM', variable_list

                    self.model_list.append(model_object)
                    self.component_variable_list = self.component_variable_list + variable_list            

            return dep_var

        else:
            return None

    def return_spatial_query(self, spatial_query_element):
        
        # Parsing attributes of the spatial query
        table = spatial_query_element.get('table')
        skimField = spatial_query_element.get('skim_var')
        asField = spatial_query_element.get('as_var')
        originField = spatial_query_element.get('origin_var')
        destinationField = spatial_query_element.get('destination_var')
        sampleField = spatial_query_element.get('sample_var')
        
        countChoices = spatial_query_element.get('count')
        if countChoices is not None:
            countChoices = int(countChoices)
        thresholdTimeConstraint = spatial_query_element.get('threshold')
        seed = spatial_query_element.get('seed')
        if seed is not None:
            seed = int(seed)
        else:
            seed = 1

        if thresholdTimeConstraint is not None:
            thresholdTimeConstraint = int(thresholdTimeConstraint)


        activity_element = spatial_query_element.get('ActivityFilter')
        if activity_element is not None:
            activityTypeFilter = self.return_activity_type_condition(activity_element)
        else:
            activityTypeFilter = None

        startConstraint_element = spatial_query_element.find('Start')
        startConstraint = self.return_spatio_temporal_constraint(startConstraint_element)

        endConstraint_element = spatial_query_element.find('End')
        endConstraint = self.return_spatio_temporal_constraint(endConstraint_element)


        locationVariables = []
        locationInfoTable = None
        locationIdVar = None
        locationInformationElement = spatial_query_element.find('ExtractLocationInformation')
        if locationInformationElement is not None:
            locationInfoTable = locationInformationElement.get('table')
            locationIdVar = locationInformationElement.get('location_var')
            locationVarsIterator = locationInformationElement.getiterator('LocationVariable')
            
            for var in locationVarsIterator:
                varname = var.get('var')
                locationVariables.append(varname)
                

        beforeModel = spatial_query_element.get('before_model')
        afterModel = spatial_query_element.get('after_model')

        prismConstraint = PrismConstraints(table, skimField, 
                                           originField, destinationField, 
                                           startConstraint, endConstraint, 
                                           asField,
                                           sampleField, countChoices, activityTypeFilter, 
                                           thresholdTimeConstraint, seed,
                                           afterModel, beforeModel,
                                           locationInfoTable,
                                           locationIdVar,
                                           locationVariables)
        #print prismConstraint
        return prismConstraint

    def return_spatio_temporal_constraint(self, constraint_element):
        table = constraint_element.get('table')
        location_field = constraint_element.get('location_var')
        time_field = constraint_element.get('time_var')

        constraint = SpatioTemporalConstraint(table, location_field, time_field)
        return constraint
    

    def return_activity_type_condition(self, model_element):
        # Varies from the filter condition in that no variables
        # are added to the variable list for the component

        filter_element = model_element.find('Filter')
        
        if filter_element is None:
            return None

        tablename = filter_element.get('table')
        varname = filter_element.get('var')
        variable_list = [(tablename, varname)]
        
        filterCondition = filter_element.get('condition')
        filterValue = float(filter_element.get('value'))

        dataFilter = DataFilter(varname, filterCondition, filterValue)

        return dataFilter


    

    def return_filter_condition_list(self, model_element):
        filterIterator = model_element.getiterator("Filter")
        filterList = []
        for i in filterIterator:
            filterCondition = self.return_filter_condition(i)
            filterList.append(filterCondition)
        return filterList

    def return_filter_condition(self, filter_element):
        
        if filter_element is None:
            return None

        tablename = filter_element.get('table')
        varname = filter_element.get('var')
        variable_list = [(tablename, varname)]
        
        filterCondition = filter_element.get('condition')
        filterValue = filter_element.get('value')
        if filterValue is not None:
            filterValue = float(filter_element.get('value'))
        else:
            filterTablename = filter_element.get('valuetable')
            filterValue = filter_element.get('valuevar')
            variable_list_val = [(filterTablename, filterValue)]
            self.component_variable_list = (self.component_variable_list + 
                                            variable_list_val)
        dataFilter = DataFilter(varname, filterCondition, filterValue)

        self.component_variable_list = (self.component_variable_list + 
                                        variable_list)
        
        #print 'FILTERCONDITION - ', filterCondition

        return dataFilter

    def return_run_until_condition(self, model_element):
        runIterator = model_element.getiterator('RunUntilCondition')
        runList = []
        
        for i in runIterator:
            runCondition = self.return_filter_condition(i)
            runList.append(runCondition)
        return runList

    def dummy(self):
        
        if run_until_element is None:
            return None
        
        tablename_ind = run_until_element.get('table')
        varname_ind = run_until_element.get('var')
        variable_list_ind = [(tablename_ind, varname_ind)]

        runUntilCondition = run_until_element.get('condition')
        filterValue = run_until_element.get('value')
        if filterValue is not None:
            filterValue = float(run_until_element.get('value'))
        else:
            filterTablename = run_until_element.get('valuetable')
            filterValue = run_until_element.get('valuevar')
            variable_list_val = [(filterTablename, filterValue)]
            self.component_variable_list = (self.component_variable_list + 
                                            variable_list_val)
        runUntilFilter = DataFilter(varname_ind, runUntilCondition, filterValue)


        """


        tablename_val = run_until_element.get('valuetable')
        varname_val = run_until_element.get('valuevar')
        variable_list_val = [(tablename_val, varname_val)]

        self.component_variable_list = self.component_variable_list +\
            variable_list_ind + variable_list_val

        #print 'RUNUNTILCONDITION - ', runUntilCondition

        runUntilFilter = DataFilter(varname_ind, runUntilCondition, varname_val)
        """
        return runUntilFilter

    def return_component_attribs(self, component_element):
        """
        Returns the variable name, table name, keys for the component.
        """
        name = component_element.get('name')
        readFromTable = component_element.get('read_from_table')
        writeToTable = component_element.get('write_to_table')
        if writeToTable is None:
            writeToTable = readFromTable
            

        prim_keys = component_element.get('key')
        if prim_keys is not None:
            prim_keys = re.split('[,]', prim_keys)
        index_keys = component_element.get('count_key')
        if index_keys is not None:
            index_keys = re.split('[,]', index_keys)

        
        #print varname, tablename, [prim_keys, index_keys]
        return name, readFromTable, writeToTable, [prim_keys, index_keys]
        
                            

if __name__ == '__main__':
    import time
    """
    from numpy import zeros, random
    fileloc = '/home/kkonduri/simtravel/test/config.xml' 
    configObject = etree.parse(fileloc)
    conf_parser = ConfigParser(configObject)
    component_list = conf_parser.parse_models()
    
    colnames = ['one', 'age', 'parttime', 'telcomm', 'empserv', 'commtime', 'popres',
                'numchild', 'numdrv', 'respb', 'autoworkmode', 'gender', 'numadlts',
                'numadltsgender', 'schstat',
                'daystart', 'dayend', 'numjobs', 'workstart1', 'workend1', 
                'workstat', 'workloc', 'numadlts', 'timeend', 
                'numvehs', 'schdailystatus', 'actdestination', 'actduration']
    
    cols = len(colnames)
    cols_dep = 15
    
    ti = time.time()
    
    proc_time = []
    for i in range(4):
        rows = 10**(i)
        print 'RUN WITH - %d records' %(rows)

        ti = time.time()
        rand_input = random.random_integers(1, 4, (rows,cols - cols_dep))
    
        data = zeros((rows, cols))

        data[:,:cols-cols_dep] = rand_input
        data = DataArray(data, colnames)
    
        #print data.data[0,:]


        for i in component_list:
            print '\tCOMPONENT NAME - ', i.component_name
            #print '\t\tVARIABLE LIST FOR COMPONENT - ',i.variable_list
            i.run(data)
        #print i.data.data[:10]
        diff = time.time()-ti
        proc_time.append(diff)
        print '\tTIME ELAPSED USING ARRAY FORMAT - %.2f' %(diff)
    

    """

    from openamos.core.database_management.database_configuration import DataBaseConfiguration
    from openamos.core.database_management.database_connection import DataBaseConnection
    from openamos.core.database_management.query_browser import QueryBrowser
    
    ti = time.time()
    # Changes in the configuration file - add protocol, 
    # convert string parameters to lower case when parsing, variable names

    protocol = 'postgres'
    user_name = 'postgres'
    password = '1234'
    host_name = '10.206.111.198'
    database_name = 'postgres'

    dbconfig = DataBaseConfiguration(protocol, user_name, password, 
                                     host_name, database_name)
    newobject = QueryBrowser(dbconfig)

    # setup a connection
    newobject.dbcon_obj.new_connection()

    newobject.create_mapper_for_all_classes()

    #print type(VEHICLE)

    hhld_class_name = 'households'
    pers_class_name = 'persons'

    query_gen, cols = newobject.select_all_from_table(hhld_class_name)
    query_gen, cols = newobject.fetch_selected_rows(pers_class_name, 'employ', '1')
    #temp_dict = {'households':'household_id, adults, homestaz', 'persons':'employ, workstaz'}
    temp_dict = {'households':['household_id', 'adults', 'homestaz'], 
                 'persons':['employ', 'workstaz']}
    
    query_gen, cols = newobject.select_join(temp_dict, 'household_id', pers_class_name, 'employ', '1')
    
    ti = time.time()
    
    print type(query_gen)

    """
    c = 0
    for i in query_gen:
        c = c + 1
        if c> 10:
            break
        print i.household_id
        
    print 'records read', c
    
    
    


    # create a mapper object
    newobject.create_mapper_for_all_classes()

    # to select all rows from table
    class_name = 'School'
    newobject.select_all_from_table(class_name)

    # to select rows based on a filter
    class_name = 'Office'
    column_name = 'role'
    value = 'se'
    newobject.fetch_selected_rows(class_name, column_name, value)

    # join across tables
    key_column_name = 'role_id'
    temp_dict = {'Person':'first_name, last_name', 'Office':'role, years'}
    match_column_name = 'role_id'
    value='1'
    newobject.select_join(temp_dict, column_name, new_col, value)

    # deleting records
    class_name = 'School'
    newobject.delete_all(class_name)

    



    # close a connection
    newobject.dbcon_obj.close_connection()

    """

    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
