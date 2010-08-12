'''
# OpenAMOS - Open Source Activity Mobility Simulator
# Copyright (c) 2010 Arizona State University
# See openamos/LICENSE

'''

import copy
import re
from lxml import etree
from numpy import array
from openamos.core.component.abstract_controller import BasicController

from openamos.core.models.linear_regression_model import LinearRegressionModel
from openamos.core.models.stochastic_frontier_regression_model import StocFronRegressionModel
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

from openamos.core.database_management.database_configuration import DataBaseConfiguration

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

    def parse_models(self):
        self.iterator = self.configObject.getiterator("Component")
        componentList = []
        
        for i in self.iterator:
            component = self.create_component(i)
            componentList.append(component)
            if i.attrib['name'] == self.componentName:
                return componentList

        return componentList

    def parse_databaseAttributes(self):
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
        
    
                
    def create_component(self, component_element):
        comp_name = component_element.get('name')
        modelsIterator = component_element.getiterator("Model")
        self.model_list = []
        self.component_variable_list = []
        for i in modelsIterator:
            self.create_model_object(i)
            #component_variable_list = (component_variable_list 
            #                           + variable_list)
            #model_list.append(model)
        #print self.component_variable_list
        self.component_variable_list = list(set(self.component_variable_list))
        #print self.component_variable_list
        component = AbstractComponent(comp_name, self.model_list, self.component_variable_list)
        return component
        
    def create_model_object(self, model_element):
        model_formulation = model_element.attrib['formulation']
        
        #print model_formulation
        
        if model_formulation == 'Regression':
            self.create_regression_object(model_element)
            
        if model_formulation == 'Count':
            self.create_count_object(model_element)
        
        if model_formulation == 'Multinomial Logit':
            self.create_multinomial_logit_object(model_element)
    
        if model_formulation == 'Nested Logit':
            self.create_nested_logit_object(model_element)

        if model_formulation == 'Ordered':
            self.create_ordered_choice_object(model_element)

        if model_formulation == 'Probability Distribution':
            self.create_probability_object(model_element)


    def create_regression_object(self, model_element):
        #model type
        model_type = model_element.get('type')

        #variable list required for running the model
        variable_list = []

        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        choice = [dep_varname]

        # Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = [coeff_dict] 

        variable_list = variable_list + vars_list

        # specification object
        specification = Specification(choice, coefficients)

        # Reading the vertex
        vertex = model_element.get('vertex')

        # Creating the variance matrix
        model_type = model_element.get('type')
        
        varianceIterator = model_element.getiterator('Variance')
        
        if model_type == 'Linear':
            for i in varianceIterator:
                variance = array([[float(i.get('value'))]])
            errorSpec = LinearRegErrorSpecification(variance)         
            model = LinearRegressionModel(specification, errorSpec)
            
        
        if model_type == 'Stochastic Frontier':
            for i in varianceIterator:
                variance_type = i.get('type', default=None)
                if variance_type == None:
                    norm_variance = float(i.get('value'))
                elif variance_type == 'Half Normal':
                    half_norm_variance = float(i.get('value'))
                    
            variance = array([[norm_variance, 0],[0, half_norm_variance]])
            errorSpec = StochasticRegErrorSpecification(variance, vertex)
            model = StocFronRegressionModel(specification, errorSpec)                 

        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model_type = 'regression'
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter, 
                                dep_table, dep_keys)
        
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_count_object(self, model_element):
        #model type
        model_type = model_element.get('type')

        #variable list required for running the model
        variable_list = []
        
        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)


        #Creating the coefficients input for the regression model
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients = [coeff_dict]

        variable_list = variable_list + vars_list

        # dependent variable
        variable = model_element.get('name')
        
        # alternatives        
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)

        # specification object
        specification = CountSpecification(choice, coefficients)
        
        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model_type = 'choice'
        model = CountRegressionModel(specification)
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                dep_table, dep_keys)
        
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list
        

    def create_multinomial_logit_object(self, model_element):
        #model type
        model_type = model_element.get('type')

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        coefficients_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            if model_type == 'Alternative Specific':
                coeff_dict, vars_list = self.return_coeff_vars(i)
                coefficients_list.append(coeff_dict)
                variable_list = variable_list + vars_list
        if model_type <> 'Alternative Specific':
            coeff_dict, vars_list = self.return_coeff_vars(model_element)
            coefficients_list.append(coeff_dict)
            coefficients_list = coefficients_list*len(choice)
            variable_list = variable_list + vars_list

        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)
    
        model = LogitChoiceModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                dep_table, dep_keys)#Model Object

        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list


    def create_nested_logit_object(self, model_element):
        #variable list required for running the model
        variable_list = []

        #dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        #Specification dict
        spec_build_ind = {}


        #building the nest structure
        nest_struct = {}
        spec_dict = {}
        alts = []
        alternativeIterator = model_element.getiterator('Alternative')
        for i in alternativeIterator:
            name = i.get('id')
            coeff_dict, vars_list = self.return_coeff_vars(i)
            variable_list = variable_list + vars_list
            spec = NestedChoiceSpecification([name], [coeff_dict])
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

        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = NestedLogitChoiceModel(specification)
        model_type = 'choice'
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                dep_table, dep_keys)


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

        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        coefficients_list = []
        threshold_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            threshold = i.get('threshold')
            if threshold is not None:
                threshold_list.append(float(threshold))
        coeff_dict, vars_list = self.return_coeff_vars(model_element)
        coefficients_list.append(coeff_dict)
        variable_list = vars_list
            

        #print dep_varname, model_type
                    
        # logit specification object
        if model_type == 'Logit':
            #print coefficients_list
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())
        else:
            specification = OLSpecification(choice, coefficients_list, threshold_list,
                                            distribution=model_type.lower())

        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)            

        model = OrderedModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                dep_table, dep_keys) #Model Object
    
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list

    
    def create_probability_object(self, model_element):
        #variable_list_required for running the model
        variable_list = []

        # dependent variable
        depvariable_element = model_element.find('DependentVariable')
        dep_varname, dep_table, dep_keys = self.return_dep_var_attribs(depvariable_element)

        # alternatives
        alternativeIterator = model_element.getiterator('Alternative')
        choice = []
        coefficients_list = []
        for i in alternativeIterator:
            alternative = i.get('id')
            choice.append(alternative)
            coeff_dict, vars_list = self.return_coeff_vars(i)
            coefficients_list.append(coeff_dict)
            variable_list = variable_list + vars_list

        #print coefficients_list
        #print dep_varname

        # logit specification object
        specification = Specification(choice, coefficients_list)

        dataFilter = self.return_filter_condition(model_element)
        runUntilFilter = self.return_run_until_condition(model_element)

        model = ProbabilityModel(specification) 
        model_type = 'choice'                   #Type of Model 
        model_object = SubModel(model, model_type, dep_varname, dataFilter, runUntilFilter,
                                dep_table, dep_keys) #Model Object
    
        #return model_object, variable_list
        self.model_list.append(model_object)
        self.component_variable_list = self.component_variable_list + variable_list

    def check_for_interaction_terms(self, var_element):
        variable_list = []
        coeff_dict = {}
        dep_varname = ''

        if var_element.get('interaction') is not None:
            var_element.get('interaction')
            varnames = re.split('[,]', var_element.get('var'))
            #print varnames
            tablenames = re.split('[,]', var_element.get('table'))
            #print tablenames
            for i in range(len(varnames)):
                variable_list.append((tablenames[i], varnames[i]))
                dep_varname = dep_varname + varnames[i].title()
                coeff_dict[varnames[i]] = 1
            choice = [dep_varname]
            coefficients_list = [coeff_dict]
            # specification object
            #print coefficients_list
            specification = Specification(choice, coefficients_list)

            model = InteractionModel(specification) 
            model_type = 'regression'                   #Type of Model 
            model_object = SubModel(model, model_type, dep_varname) #Model Object
            
            #return model_object, variable_list
            #print '\t\t\t\tFOR THE INTERACTION TERM', variable_list

            self.model_list.append(model_object)
            self.component_variable_list = self.component_variable_list + variable_list            
            return dep_varname

        else:
            return None

    
    def return_table_var(self, var_element):
        return var_element.get('table'), var_element.get('var')
        
    def return_coeff_vars(self, element):
        variableIterator = element.getiterator('Variable')
        vars_list = []
        coeff_dict = {}

        for i in variableIterator:
            dep_varname = self.check_for_interaction_terms(i)
            if dep_varname is not None:
                #print '\t\tINTERACTION TERM'
                coeff = i.get('coeff')
                #print coeff
                coeff_dict[dep_varname] = float(coeff)
            else:
                vars_list.append(self.return_table_var(i))
                varname = i.get('var')
                coeff = i.get('coeff')
                coeff_dict[varname] = float(coeff)
        return coeff_dict, vars_list


    def return_filter_condition(self, model_element):
        filter_element = model_element.find('Filter')
        
        if filter_element is None:
            return None

        tablename = filter_element.get('table')
        varname = filter_element.get('var')
        variable_list = [(tablename, varname)]
        
        filterCondition = filter_element.get('condition')
        filterValue = float(filter_element.get('value'))

        dataFilter = DataFilter(varname, filterCondition, filterValue)

        self.component_variable_list = self.component_variable_list + variable_list
        
        #print 'FILTERCONDITION - ', filterCondition

        return dataFilter

    def return_run_until_condition(self, model_element):
        run_until_element = model_element.find('RunUntilCondition')
        
        if run_until_element is None:
            return None
        
        tablename_ind = run_until_element.get('table')
        varname_ind = run_until_element.get('var')
        variable_list_ind = [(tablename_ind, varname_ind)]

        runUntilCondition = run_until_element.get('condition')

        tablename_val = run_until_element.get('table')
        varname_val = run_until_element.get('var')
        variable_list_val = [(tablename_val, varname_val)]

        self.component_variable_list = self.component_variable_list +\
            variable_list_ind + variable_list_val

        #print 'RUNUNTILCONDITION - ', runUntilCondition

        runUntilFilter = DataFilter(varname_ind, runUntilCondition, varname_val)
        return runUntilFilter

    def return_dep_var_attribs(self, depvariable_element):
        """
        Returns the variable name, table name, keys.
        """
        varname = depvariable_element.get('var')
        tablename = depvariable_element.get('table')
        keys = depvariable_element.get('key')
        if keys is not None:
            keys = re.split('[,]', depvariable_element.get('key'))
        print varname, tablename, keys
        return varname, tablename, keys
        
                            

if __name__ == '__main__':
    import time
    
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

    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
