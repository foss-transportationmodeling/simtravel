#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import sqlalchemy
import sqlite3
import psycopg2 as dbapi2
import sqlalchemy.schema
from database_configuration import DataBaseConfiguration
from database_connection import DataBaseConnection
from sqlalchemy import create_engine
from psycopg2 import extensions
from sqlalchemy.sql import select
from database_configuration import DataBaseConfiguration
from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from sqlalchemy import schema, types
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime


class VECHICLE(object): pass

class LINKS(object): pass

class LINK_OD(object): pass

class SCHEDULE(object): pass

class TSP(object): pass

class DESTINATION_OPPORTUNITIES(object): pass

class HOUSEHOLD(object): pass

class PERSON(object): pass

class PERSON_SCHEDULE(object): pass

class TRIP(object): pass

class PERSON_TRIP(object): pass

class OFFICE(object): pass
 
class TEMP(object): pass

class SCHOOL(object): pass

class MainClass(object):
    
    ########## initialization ##########
    #initialize the class 
    def __init__(self, protocol = None, user_name = None,
                password = None, host_name = None, 
                database_name = None, database_config_object = None, 
                dbcon_obj = None, engine = None, 
                connection = None, result = None, 
                query = None, metadata = None, 
                table_name = None, session = None,
                class_name = None):
       
        self.protocol = protocol
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.database_name = database_name
        self.engine = engine
        self.connection = connection
        self.result = result
        self.query = query
        self.metadata = metadata
        self.table_name = table_name
        self.session = session
        self.class_name = class_name
        self.database_config_object = database_config_object
        dbcon_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name, self.database_config_object)
        self.dbcon_obj = dbcon_obj
        print self.dbcon_obj
    
    ########## initialization ends ##########

    ########## methods for mapping ##########
    
    #separate function for mapper
    def table_mapper(self, class_name, table_name):
        """
        This method is used to create a mapper to the table in the database
        
        Input:
        Class name and Table name
        
        Output:
        Creates a table mapper object
        """
        
        #before creating the mapper check if the table exists
        self.table_name = table_name
        self.class_name = class_name
        table_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if table_flag:
            #table exists
            try:
                #print 'table name is %s and class name is %s'%(table_name, class_name)
                #load the table
                new_table = Table(self.table_name, self.dbcon_obj.metadata, autoload=True)
                
                #create mapper
                class_name = class_name.upper()                
                mapper(eval(class_name), new_table)

                #create an object for the mapper
                self.temp_object = eval(class_name)()
                
                #print the session and mapper object
                #print 'the session object is %s and the mapper object is %s\n'%(self.dbcon_obj.session, self.temp_object)
                return self.temp_object
            except Exception, e:
                print 'Failed to create mapper'
                print e
                #raise Exception                                
        else:
            print 'Table does not exist in the database. Cannot create a mapper'
            return None


    #create mapper for all the classes
    def create_mapper_for_all_classes(self):
        """
        This method is used to create mapper objects for all the classes/tables
        This method calls the table_mapper method to map a table to a class
        
        Input:
        None
        
        Output:
        Mapper objects for all classes        
        """
        
        #print 'map all the classes'
        """
        #for class Vechile
        class_name = 'VECHICLE'
        table_name = 'vehicle'
        self.vehicle = self.table_mapper(class_name, table_name)
                
        #for class Links
        class_name = 'LINKS'
        table_name = 'links'
        self.links = self.table_mapper(class_name, table_name)

        #for class Link_OD
        class_name = 'LINK_OD'
        table_name = 'link_od'
        self.link_od = self.table_mapper(class_name, table_name)
        
        #for class Schedule
        class_name = 'SCHEDULE'
        table_name = 'schedule'
        self.schedule = self.table_mapper(class_name, table_name)
        
        #for class TSP
        class_name = 'TSP'
        table_name = 'tsp'
        self.tsp = self.table_mapper(class_name, table_name)
        
        #for class Destination_Opportunities
        class_name = 'DESTINATION_OPPORTUNITIES'
        table_name = 'destination_opportunities'
        self.destination_opportunities = self.table_mapper(class_name, table_name)
        
        #for class Household
        class_name = 'HOUSEHOLD'
        table_name = 'household'
        self.household = self.table_mapper(class_name, table_name)

        #for class Person_Schedule
        class_name = 'PERSON_SCHEDULE'
        table_name = 'person_schedule'
        self.person_schedule = self.table_mapper(class_name, table_name)

        #for class Trip
        class_name = 'TRIP'
        table_name = 'trip'
        self.trip = self.table_mapper(class_name, table_name)
        
        #for class Person_Trip
        class_name = 'PERSON_TRIP'
        table_name = 'person_trip'
        self.person_trip = self.table_mapper(class_name, table_name)
        
        #for class Office
        class_name = 'OFFICE'
        table_name = 'office'
        self.office = self.table_mapper(class_name, table_name)
            
        #for class Person
        class_name = 'PERSON'
        table_name = 'person'
        self.person = self.table_mapper(class_name, table_name)
        """
        #for class School
        class_name = 'SCHOOL'
        table_name = 'school'
        self.school = self.table_mapper(class_name, table_name)

    ########## methods for mapping end ##########

    ########## methods for select query ##########
    
    #select all rows from the table
    def select_all_fom_table(self, class_name):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Class name corresponding to the table

        Output:
        Returns all the rows in the table
        """
        
        #get the column list for the table
        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)

        #query the table to fetch all the records by passing the columns
        query = self.dbcon_obj.session.query(eval(new_class_name)).values(*col)

        all_rows = []
        for instance in query:
            print instance
            all_rows.append(instance)

        print ' '
        return query, col


    #select rows based on a selection criteria
    def fetch_selected_rows(self, class_name, column_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        
        #get the column list for the table
        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        #print 'table object is %s'%temp_table
        for cl in temp_table.c:
            col.append(cl)

        try:
            query = self.dbcon_obj.session.query(eval(new_class_name)).filter(getattr((eval(new_class_name)), column_name) == value).values(*col)
            row_list = []
            counter = 0
            for each in query:
                counter = counter + 1
                row_list.append(each)

            if counter == 0:
                print 'No rows selected.\n'
            else:
                for each_ins in row_list:
                    print each_ins            
            print 'Select query successful.\n'
        except:
            print 'Error retrieving the information. Query failed.\n'


    #select and print the join
    def select_join(self, temp_dict, column_name, chk_table, chk_col=None, value=None):
        """
        self, table1_list, table2_list, column_name
        This method is used to select the join of tables and display them.
        
        Input:
        Database configuration object, table names, columns and values.
        
        Output:
        Displays the rows based on the join and the selection criterion.
        """

        #initialize the variables
        final_list = []
        table_list = []
        class_list = []
        col_name = column_name
        final_list = temp_dict.values()
        table_list = temp_dict.keys()      
        
        #check first if the select query is for single table or multiple tables
        if len(table_list) > 1:
            print 'multiple tables'
        else:
            print 'single table'

        #use string manipulation to create the select query
        len1 = len(final_list)
        len2 = len(table_list)
        ctr = 0
        sql_string = "select "
        condition_str = 'where '
        for i in final_list:
            if int(ctr) < (int(len1)-1):
                sql_string = sql_string + str(i) + ', '
                ctr = ctr + 1
            else:
                sql_string = sql_string + str(i) + ' '
        sql_string = sql_string + 'from '

        ctr = 0
        for i in table_list:
            if int(ctr) < (int(len2)-1):
                sql_string = sql_string + str(i.lower()) + ', '
                ctr = ctr + 1
            else:
                sql_string = sql_string + str(i.lower()) + ' '
               

        if len2 == 1:
            condition_str = condition_str
        elif len2 == 2:
            condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + table_list[1].lower() + '.' + col_name
        else:
            ctr = 0
            for i in table_list:
                if int(ctr) == 0:
                    #do nothing
                    #condition_str = condition_str
                    ctr = ctr + 1
                elif int(ctr) < (int(len2)-1):
                    condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + str(i.lower()) + '.' + col_name + ' and '
                    ctr = ctr + 1
                else:
                    condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + str(i.lower()) + '.' + col_name
        

        #put a condition to check for value
        if value == None:
            if int(len2) == 1:
                sql_string = sql_string
            else:
                sql_string = sql_string + condition_str
        else:
            sql_string = sql_string + condition_str
            chk_value = ' and '
            if len2 == 1:
                condition_str = chk_table.lower() + '.' + chk_col + ' = ' + value
                sql_string = sql_string + condition_str
            else:
                condition_str = chk_value + chk_table.lower() + '.' + chk_col + ' = ' + value
                sql_string = sql_string + condition_str
        
        print ' '
        cols_list = []
        tabs_list = []

        #convert all the table names to upper case
        for each in table_list:
            tabs_list.append(each.upper())
        
        #separate all the columns from the lists
        for i in final_list:
            temp = str(i)
            parts = temp.split(", ")
            for j in parts:
                cols_list.append(j)
        
        print sql_string
        
        try:
            """
            temp_var1 = None
            temp_var2 = None
            temp_var1 = str(tabs_list[0]) +  '.' + col_name
            temp_var2 = str(tabs_list[1]) +  '.' + col_name
            if value <> None:
                temp_var3 = str(tabs_list[0]) + '.' + chk_col

            #query = self.dbcon_obj.session.query(eval(tabs_list[0]), eval(tabs_list[1])).\
            #filter(eval(temp_var1)==eval(temp_var2)).filter(eval(temp_var3)==eval(value)).values(*cols_list)
            """
            sample_str = ''
            ctr = 0
            for i in tabs_list:
                if ctr==0:
                    sample_str = i
                    ctr = ctr + 1
                else:
                    sample_str = sample_str + ', ' + i
                query = self.dbcon_obj.session.query((sample_str))

            result = query.from_statement(sql_string).values(*cols_list)
            """
            all_rows = []
            for instance in result:
                print instance
                all_rows.append(instance)
            print ' '
            """
            return result, cols_list
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'            
                 

    ########## methods for select query end ##########

    ########## methods for delete query ##########
    
    #delete rows based on a deletion criteria
    def delete_selected_rows(self, class_name, col_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """
        print 'testing delete'
        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        #print 'table object is %s'%temp_table
        for cl in temp_table.c:
            col.append(cl)

        try:
            delete_query = self.dbcon_obj.session.query(eval(new_class_name)).filter(getattr((eval(new_class_name)), col_name) == value)
            #based on the count determine if any rows were selected
            if delete_query.count() == 0:
                print 'No rows were fetched. Cannot complete delete operation.'
            else:                
                for each_ins in delete_query:
                    #print 'each is %s'%each_ins
                    self.dbcon_obj.session.delete(each_ins)
                print 'delete successful'                    
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'
        

    #delete all rows i.e. empty table
    def delete_all(self, class_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """

        new_class_name = class_name.upper()
        new_table_name = new_class_name.lower()
        #print 'table name is %s and class name is %s'%(new_class_name, new_table_name)
        
        #fetch al rows of the table and then delete
        col = []
        temp_table = Table(new_table_name, self.dbcon_obj.metadata, autoload=True)
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)

        try:
            query = self.dbcon_obj.session.query(eval(new_class_name))
            print 'query is %s'%query
            if query.count() == 0:
                print 'No rows fectched. Cannot complete delete operation'
            else:
                for instance in query:
                    #print instance
                    self.dbcon_obj.session.delete(instance)
                print 'Delete all records successful.'
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'

    ########## methods for delete query end ##########


    ########## methods for insert query ##########
    
    #insert values in the table
    def insert_into_table(self):
        """
        This method is used to insert new values into the table.

        Input:
        Database configuration object, table name and values

        Output:
        Values inserted in to the table
        """

        #testing
        print 'testing'
        jack = Temp()
        jack.first_name = 'jack'
        jack.last_name = 'bauer'
        jack.age = '45'
        self.session.add(jack)
        
        jack = Temp()
        jack.first_name = 'tony'
        jack.last_name = 'bauer'
        jack.age = '51'
        self.session.add(jack)
        self.session.flush()
        self.session.commit()
        print 'jack and tony added'
        #TODO: change the column names to dynamic, currently static
        #can create various objects at once and use 'add_all' to add all objects

    ########## methods for insert query end ##########


#unit test to test the code
import unittest

#define a class for testing
class TestMainClass(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'postgres'
        self.database_config_object = None
        self.dbcon_obj = None
    
    def testMainClass(self):
        newobject = MainClass(self.protocol, self.user_name, self.password, self.host_name, self.database_name, self.database_config_object, self.dbcon_obj)

        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        
        """ create mapper objects for all classes """
        newobject.create_mapper_for_all_classes()
        
        """ to select all rows from the table """
        class_name = 'School'
        #newobject.select_all_fom_table(class_name)

        """ to select few rows """
        class_name = 'Office'
        column_name = 'role'
        value = 'se'
        #newobject.fetch_selected_rows(class_name, column_name, value)

        """ to print the join """
        column_name = 'role_id'
        table1_list = ['person', 'first_name', 'last_name']
        table2_list = ['office','role', 'years']
        temp_dict = {'Person':'first_name, last_name', 'Office':'role, years', 'Asu':'grad, undergrad'}
        #temp_dict = {'Person':'first_name, last_name', 'Office':'role, years'}
        #temp_dict = {'Person':'first_name, last_name'}
        new_col = 'role_id'
        value = '1'
        chk_table = 'person'
        newobject.select_join(temp_dict, column_name, chk_table, new_col, value)
        #newobject.select_join(temp_dict, column_name, chk_table)
        
        """ delete all records """
        class_name = 'School'
        #newobject.delete_all(class_name)

        """ delete selected rows """
        class_name = 'School'
        col_name = 'teacher'
        value = 'ab'
        #newobject.delete_selected_rows(class_name, col_name, value)
        
        """ to select all rows from the table """
        class_name = 'School'
        #newobject.select_all_fom_table(class_name)
        
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
