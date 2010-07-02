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


class Vehicle(object): pass

class Links(object): pass

class Link_OD(object): pass

class Schedule(object): pass

class TSP(object): pass

class Destination_Opportunities(object): pass

class Household(object): pass

class Person(object): pass

class Person_Schedule(object): pass

class Trip(object): pass

class Person_Trip(object): pass

class Office(object): pass
 
class Temp(object): pass

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
        class_name = 'Vehicle'
        table_name = 'vehicle'
        self.vehicle = self.table_mapper(class_name, table_name)
                
        #for class Links
        class_name = 'Links'
        table_name = 'links'
        self.links = self.table_mapper(class_name, table_name)

        #for class Link_OD
        class_name = 'Link_OD'
        table_name = 'link_od'
        self.link_od = self.table_mapper(class_name, table_name)
        
        #for class Schedule
        class_name = 'Schedule'
        table_name = 'schedule'
        self.schedule = self.table_mapper(class_name, table_name)
        
        #for class TSP
        class_name = 'TSP'
        table_name = 'tsp'
        self.tsp = self.table_mapper(class_name, table_name)
        
        #for class Destination_Opportunities
        class_name = 'Destination_Opportunities'
        table_name = 'destination_opportunities'
        self.destination_opportunities = self.table_mapper(class_name, table_name)
        
        #for class Household
        class_name = 'Household'
        table_name = 'household'
        self.household = self.table_mapper(class_name, table_name)

        #for class Person_Schedule
        class_name = 'Person_Schedule'
        table_name = 'person_schedule'
        self.person_schedule = self.table_mapper(class_name, table_name)

        #for class Trip
        class_name = 'Trip'
        table_name = 'trip'
        self.trip = self.table_mapper(class_name, table_name)
        
        #for class Person_Trip
        class_name = 'Person_Trip'
        table_name = 'person_trip'
        self.person_trip = self.table_mapper(class_name, table_name)
        """
        #for class Office
        class_name = 'Office'
        table_name = 'office'
        self.office = self.table_mapper(class_name, table_name)
            
        #for class Person
        class_name = 'Person'
        table_name = 'person'
        self.person = self.table_mapper(class_name, table_name)

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
        new_class_name = class_name
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
        """
        Fetch all the rows of a table using the select query. This query 
        returns a row proxy for each row in the table.above code returns 
        an instance of the mapper class
        """
        """
        temp_table = Table(self.table_name, self.metadata, autoload=True)
        s = select([temp_table])
        res = self.connection.execute(s)
        print "display all rows"
        for row in res.fetchall():
            print row
            print type(row)
        """            


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
        new_class_name = class_name
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
    def select_join(self, temp_dict, column_name):
        """
        self, table1_list, table2_list, column_name
        This method is used to select the join of tables and display them.
        
        Input:
        Database configuration object, table names, columns and values.
        
        Output:
        Dsiplays the rows based on the join and the selection criterion.
        """
        """
        #for now send no args
        #currently the code works for 2 tables
        col_name = column_name
        list1 = table1_list
        list2 = table2_list

        #initialize the variables
        final_list = []
        table_list = []
        class_list = []
        class1 = None
        class2 = None
        table1 = None
        table2 = None
        ctr = 0
        #separate the column names and table names and append them to lists
        for w in list1:
            if ctr == 0:
                class1 = w
                table1 = w.lower()
                class_list.append(w)
                table_list.append(w.lower())
                ctr = ctr +1
            else:
                final_list.append(w)
        ctr = 0
        for x in list2:
            if ctr == 0:
                class2 = x
                table2 = x.lower()
                class_list.append(x)
                table_list.append(x.lower())
                ctr = ctr +1
            else:        
                final_list.append(x)

        print '\ncolumns are'
        for y in final_list:
            print y
        print '\ntables are'
        for z in table_list:
            print z
        print '\nclasses are'
        for a in class_list:
            print a

        """
        #initialize the variables
        final_list = []
        table_list = []
        class_list = []
        col_name = column_name
        final_list = temp_dict.values()
        table_list = temp_dict.keys()      
        
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

        if len2 == 2:
            condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + table_list[1].lower() + '.' + col_name
        else:
            ctr = 0
            for i in table_list:
                if int(ctr) < (int(len2)-1):
                    condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + str(i.lower()) + '.' + col_name + ' and '
                    ctr = ctr + 1
                else:
                    condition_str = condition_str + table_list[0].lower() + '.' + col_name + ' = ' + str(i.lower()) + '.' + col_name
        
        sql_string = sql_string + condition_str
        print sql_string
        print ' '
        
        #for_key = None
        try:
            """
            temp_table1 = Table(table1, self.metadata, autoload=True)
            temp_table2 = Table(table2, self.metadata, autoload=True)

            keys1 = temp_table1.foreign_keys
            keys2 = temp_table2.foreign_keys
            if keys1 <> None:
                for i in keys1:
                    print 'keys1 %s'%i
            elif keys2 <> None:
                for j in keys2:
                    print 'keys2 %s'%j
            """
            result = self.dbcon_obj.connection.execute(sql_string)
            rows = result.fetchall()
            for each_row in rows:
                print each_row
            print ' '
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'            
                 

    ########## methods for select query end ##########

    ########## methods for delete query ##########
    
    #delete rows based on a deletion criteria
    def delete_selected_rows(self, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """
        print 'testing delete'
        try:
            delete_query = self.session.query(Temp).filter(Temp.last_name==value)
            #based on the count determine if any rows were selected
            if delete_query.count() == 0:
                print 'No rows were fetched. Cannot complete delete operation.'
            else:                
                for each_ins in delete_query:
                    #print 'each is %s'%each_ins
                    self.session.delete(each_ins)
                print 'delete successful'                    
        except:
            print 'Error retrieving the information. Query failed.'
        

    #delete all rows i.e. empty table
    def delete_all(self, table_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """
        #fetch al rows of the table and then delete
        col = []
        temp_table = Table(self.table_name, self.metadata, autoload=True)
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)

        try:
            query = self.session.query(Temp).values(*col)
            #print 'query is %s'%query
        
            for instance in query:
                print instance
                self.session.delete(instance)
        except:
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
        class_name = 'Person'
        #newobject.select_all_fom_table(class_name)

        """ to select few rows """
        class_name = 'Office'
        column_name = 'role'
        value = 'se'
        #newobject.fetch_selected_rows(class_name, column_name, value)

        """ to print the join """
        column_name = 'role_id'
        table1_list = ['Person', 'first_name', 'last_name']
        table2_list = ['Office','role', 'years']
        temp_dict = {'Person':'first_name, last_name', 'Office':'role, years'}
        #temp_dict = {'Person':'first_name, last_name', 'Office':'role, years', 'Name':'firstname, lastname', 'School':'roll_no, teacher'}
        #newobject.select_join(table1_list, table2_list, column_name)
        newobject.select_join(temp_dict, column_name)
        
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
