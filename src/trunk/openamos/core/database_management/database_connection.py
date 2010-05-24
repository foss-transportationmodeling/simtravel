#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import sqlalchemy
import psycopg2 as dbapi2
from sqlalchemy import create_engine
from psycopg2 import extensions
from sqlalchemy.sql import select
from database_configuration import DataBaseConfiguration
from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.orm import mapper
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime



#class to define the database connection along with other functions
class DataBaseConnection(object):
    """
    This is the class for database connectivity and functionality.
    The class will also perform various other functions on the database for
    data definition and data manipulation.

    Input: Database configuration object
    """

    def __init__(self, protocol = None, user_name = None,
                password = None, host_name = None, 
                database_name = None, database_config_object = None, 
                engine = None, connection = None, 
                result = None, query = None,
                metadata = None, table_name = None):

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
        test_variable = ''

        #create the database object here
        db_obj = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        database_config_object = db_obj
        self.database_config_object = database_config_object


    #done	
    def temp_function(self):
        """
        This is a test function.
        It displays the values of the database configuration object

        Input:
        Database configuration object
		
        Output:
        Display the object details
        """

        print self.database_config_object.protocol
        print self.database_config_object.host_name
        print self.database_config_object.user_name
        print self.database_config_object.password
        print self.database_config_object.database_name
	
    
    #done
    def check_if_database_engine_exits(self):
        """
        This method checks if the database engine has been installed.
        The types of databases checked are as below. The installed 
        engines are stored in an array.

        Input:
        Protocol/database type of the database configuration object

        Output:
        Return the database engine if it exists else raises exception.
        """

        database_engine = []
        try:
            import MySQLdb
            database_engine.append('mysql')
        except:
            pass
	
        try:
            import pyodbc2
            database_engine.append('mssql')
        except:
            pass

        try:
            import psycopg2
            database_engine.append('postgres')
        except:
            pass

        try:
            import sqlite3
            database_engine.append('sqlite')
        except:
            pass

        """
        After storing the installed engies, check if the protocol in
        the database configuration object is present in the array
        """
        db_engine = self.database_config_object.protocol
        if db_engine in database_engine:
            return db_engine
        else:
            raise Exception('Required database is not installed')
            sys.exit()
	
    
    #done			
    def check_if_database_exists(self):
        """
        This method opens a raw connection to the postgres database 
        and checks if the database name passed by the database 
        configuration object already exists or not. If the database 
        does not exists the database is created by another method.

        Input:
        Database name of the database configuration object.

        Output:
        Returns a boolean value indicating the database exists or not.
        """		
		
        """
        Before checking for database check if the database engine 
        is installed or not. If database is not installed then exit.
        """
        installed_db = self.check_if_database_engine_exits()
        if installed_db:
            print 'Database %s is installed.'%installed_db
        else:
            print 'Database is not installed. Cannot proceed furthur.'
            print 'Exiting the program'
            sys.exit()

        """
        Create a raw connection string for the engine
        This part is only for postgres. for other databases different 
        connection string will be used. for now implementing only for 
        postgresql.
        """
        if self.database_config_object.protocol is 'postgres':
            connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
            self.engine = create_engine(connect_string)
            engine = self.engine
            engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            #Select all the database names and check if database exists
            self.connection = engine.text("select datname from pg_database").execute()
            result = self.connection

            dbs = [db[0] for db in result.fetchall()]
            database_flag = self.database_config_object.database_name.lower() in dbs
		
            #set a flag that indicates the existence of the database.
            if database_flag:
                print 'Database %s exists'%self.database_config_object.database_name
                #dispose the engine and close the raw connection
                engine.dispose()
                self.connection.close()
                return 1
            else:
                #dispose the engine and close the raw connection			
                engine.dispose()
                self.connection.close()
                print 'Database does not exist.'
                return 0
        elif self.database_config_object.protocol is 'mysql':
            print 'Protocol is mysql'
        elif self.database_config_object.protocol is 'mssql':
            print 'Protocol is mssql'
        elif self.database_config_object.protocol is 'sqlite':
            print 'Protocol is sqlite'

            
    #this function creates a new database
    def create_database(self):
        """
        This method creates a new database by the database name passed 
        in the database configuration object.
    
        Input:
        Database name
        
        Output:
        Database created if it does not exists
	    	
        """

        #print 'database name is %s'%self.database_config_object.database_name
        db_flag = self.check_if_database_exists()		
        if not db_flag:
            try:
                connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
                self.engine = create_engine(connect_string)
                engine = self.engine
                engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.connection = engine.text("create database %s encoding = 'utf8'"%self.database_config_object.database_name).execute()
                print 'new database created'
                engine.dispose()
                self.connection.close()
            except:
                raise Exception('Error while creating a new database')
        else:
            print 'no need to create a new database'
	    		
		
    #done
    def drop_database(self):
        """
        This method is used to drop the database.
    
        Input:
        Database name
    
        Output:
        Database dropped and boolean returned
        """
    
        #Before dropping the database check if the database exists or not
        db_flag = self.check_if_database_exists()		
        if db_flag:
            try:
                connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
                self.engine = create_engine(connect_string)
                engine = self.engine
                engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.connection = engine.text("drop database %s"%self.database_config_object.database_name).execute()
                engine.dispose()
                self.connection.close()
                print 'database dropped'
            except:
                raise Exception('Error while deleting a database')
    
            
    #done                
    def define_mapping(self, ctype, map_flag = True):
        """
        This method is used to map the columns in the table. This method implements
        mapping and reverse mapping. This method helps identify the datatype 
        of the column.
     
        Input:
        Column type and map flag which identifies mapping or reverse mapping
    
        Output:
        Return the column datatype
        """
    
        #use the mapping function to check for mapping and reverse mapping
        #Before proceeding with the mapping check if mapping or reverse mapping
        if map_flag:
            #mapping datatyes
            filter_data = { "INTEGER" : Integer,
                            "SHORT" : SmallInteger,
                            "FLOAT" : Float,
                            "DOUBLE" : Numeric,
                            "VARCHAR" : VARCHAR(255),
                            "BOOLEAN" : Boolean,
                            "TINYTEXT" : VARCHAR(255),
                            "TEXT" : Text,
                            "MEDIUMTEXT" : Text,
                            "LONGTEXT": Text,
                            "DATETIME": DateTime}
	  
            return filter_data[ctype]
        else:
            #reverse mapping
            filter_data = {Integer: "INTEGER",
                            SmallInteger: "SHORT",
                            Float: "FLOAT",
                            Numeric: "DOUBLE",
                            VARCHAR: "VARCHAR",
                            Boolean: "BOOLEAN",
                            CLOB: "MEDIUMTEXT",
                            DateTime: "DATETIME",
                            String: "VARCHAR"}
	   
            try:
                c_type = filter_data[ctype.__class__]
            except:
                if isinstance(ctype, VARCHAR):
                    c_type = "VARCHAR"
                elif isinstance(ctype, CLOB):
                    c_type = "MEDIUMTEXT"
                elif isinstance(ctype, Boolean):
                    c_type = "BOOLEAN"
                elif isinstance(ctype, SmallInteger):
                    c_type = "SHORT"
                elif isinstance(ctype, Float):
                    c_type = "DOUBLE"
                elif isinstance(ctype, DateTime):
                    c_type = "DATETIME"
                elif isinstance(ctype, Numeric):
                    c_type = "DOUBLE"
                elif isinstance(ctype, String):
                    c_type = "VARCHAR"
                if isinstance(ctype, Integer):
                    c_type = "INTEGER"
            
            return c_type            


    #create a new connection with the database name
    def new_connection(self):
        """
        This method creates a new connection to the database with the databse name. 
        This method is used to create a new connection that will be furthur used 
        for data manipulation.

        Input:  
        Database configuration object
    
        Output:
        New connection created
        """
        
        #create a connection and try to establish a session with the database
        try:
            connect_string = '%s://%s:%s@%s:5432/%s'%(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
            #engine = create_engine('postgres://$self.username:$self.password@$self.hostname:5432/$self.dbname')
            self.engine = create_engine(connect_string)	
            self.connection = self.engine.connect()
            #self.metadata.bind = self.engine
            #self.metadata(bind = self.engine, schema = self.database_name)		
            print 'New connection created'
            #print 'metadata is %s'%self.metadata
            #bind the metadata to the engine
            #self.connection.close()
        except:
            print "Exiting the program since database connectivity failed"
            raise Exception
            sys.exit()
		

    #check if table exists 
    def check_if_table_exists(self, table_name):
        """
        This method checks if the table exists in the database.

        Input:
        Table name

        Output:
        Return boolean indicating the table exists or not
        """

        self.new_connection(self.database_config_object)
        #self.table_name = 'person2'
        self.table_name = table_name
        print 'table name is %s'%table_name
        #result = self.connection.execute("SELECT * FROM pg_tables where schemaname = 'public'")
        #table_array = result.fetchall() 
        #table_array = [tb[1] for tb in result.fetchall()]
        #print 'table array is %s'%table_array
        #table_flag = table_name.lower() in table_array
        #print 'result is %s'%table_flag
        #print self.metadata.sorted_tables
        #for t in reversed(self.metadata.sorted_tables):
        #	print 'table is %s'%t
        #method to be implemented. for now assume table does not exist
        table_exists = self.engine.has_table(table_name = table_name)
        if table_exists:
            print table_exists
            return 1
        else:
            print table_exists
            return 0


    #get the list of tables from the database
    def get_table_list(self):
        """
        This method is used to fetch the list of all tables in the database.

        Input:
        Database configuration object

        Output:
        List of the tables in the database.
        """

        try:
            result = self.connection.execute("SELECT * FROM pg_tables where schemaname = 'public'")
            table_names = result.fetchall()
            table_array = [tb[1] for tb in table_names]
            #print 'table list is fetched'
            return table_array
        except:
            print 'Error while fetching the tables from the database'
            raise Exception

        
    #get all the columns in a table
    def get_column_list(self, table_name):
        """
        This method is used to fetch the columns in the table
    
        Input:
        Database configuration object and table name

        Output:
        List of columns present in the table
        """

        try:
            #SELECT column_name,data_type,data_length,data_precision,nullable FROM all_tab_cols where table_name ='EMP';
            self.table_name = table_name
            result = self.connection.execute("select column_name,* from information_schema.columns where table_name = '%s'"%self.table_name)
            column_names = result.fetchall() 
            column-array = [col[0] for col in column_names]
            return column_array
        except:
            print 'Error while fetching the columns of the table %s'%self.table_name
            raise Exception


    def get_table_desc(self, table_name, table_desc):
        #store the column names and
        table_name = 'person2'
        col_names = ["fname", "lname"]
        col_types = ["VARCHAR", "VARCHAR"]
        table_columns = []
        print "new table name is %s"%table_name

        for col, ctype in zip(col_names, col_types):		
            #column = 'Column(%s, %s)'%(col,self.define_mapping(ctype))
            column = Column(col, self.define_mapping(ctype))
            table_columns.append(column)
            print "final columns are"
            
        for x in table_columns:
            print "column is %s"%x
            #call create table to create the new table
            #for now create a table here
            self.metadata = MetaData(
                        bind = self.engine
                        )
        
        dbname = 'public'
        #kwargs = {'schema':self.database_name}
		
        new_table = Table(
                    table_name,
                    self.metadata,
                    *table_columns
                    )
        #self.metadata.create_all(engine)
        #table_query = new_table
        #create table works
        new_table.create(checkfirst = True)
        print "new table created"

        #insert table works
        ins = new_table.insert()
        entry1 = ins.values(fname="abc", lname="xyz")
        entry2 = ins.values(fname="lmn", lname="pqr")
        self.connection.execute(entry1)
        self.connection.execute(entry2)
        print "values inserted"
		
        #delete works
        #t = 'namz'
        #dele = new_table.delete(new_table.c.fname==t)
        #self.connection.execute(dele)
        #return new_table

        #drop table works
        #found 2 ways to drop table
        #new_table.drop(bind = self.engine)
        #table_name1 = "table123"
        #tab_schema = "public"
        #tab = self.metadata.tables['%s.%s'%(tab_schema, table_name1)]
        #print "table metadata is %s"%tab
        #tab = self.metadata.tables[table_name1]
        #tab.drop(bind = self.engine)
        #self.metadata.remove(tab)
        print "table dropped"

        #select all rows from the table
        s = select([new_table])
        res = self.connection.execute(s)
        #rows = res.fetchall()
        #print rows
        print "display all rows"
		
        for row in res.fetchall():
            print row

        print row.fname, type(row.lname)

        #select all columns from the table
        for c in new_table.c:
            print "column name is %s"%c

        #delete all rows from the table
        #dele = new_table.delete()
        #self.connection.execute(dele)
				
        #get table schema. inverse mapping
        column_name = []
        column_type = []
        print self.metadata.tables.keys()
        tab = self.metadata.tables[table_name]
        print "tab"
        print tab
        for cols in tab.columns:
            #print "inv col is %s"%cols
            column_name.append(cols.name)
            #column_type.append(self.define_mapping(cols.type, False))
            column_type.append(cols.type)
			
        for cname, c_type in zip(column_name, column_type):
            print "name is %s and type is %s"%(cname, c_type)

 
    def create_table(self, table_name):
        """
        This method is used to create new table in the database.

        Input:
        Database configuration object and table name

        Output:
        New table created
        """


    def insert_into_table(self, table_name, values):
        """
        This method is used to insert new values into the table.

        Input:
        Database configuration object, table name and values

        Output:
        Values inserted in to the table
        """


    def select_all_fom_table(self, table_name):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Database configuration object and table name

        Output:
        Returns all the rows in the table
        """


    def fetch_selected_rows(self, table_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Returns the rows that satisfy the selection criteria
        """


    def delete_selected_rows(self, table_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """


    def delete_all(self, table_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """


    def drop_table(self, table_name):
        """
        This method is used to drop the table from the database

        Input:
        Database configuration object and table name

        Output:
        Table is dropped from the database
        """


    def get_reverse_mapping(self, table_name):
        """
        This method is used to get the reverse mapping of a table.

        Input:
        Database configuration object and table name.

        Output:
        Returns the column names and the datatypes
        """


    #close the connection            
    def close_connection(self):
        """
        This method is used to close the database connection.
    
        Input:
        Database configuration object

        Output:
        Close the connection
        """

        try:
            print "closing the database connection."
            self.connection.close()
            self.engine = None
            self.metadata = None
            if self.connection.closed:
                print 'Connection to database closed'
            else:
                print 'Connection to database not closed'
        except:
            print "Error while closing the database connection. Exiting the program."
            self.engine = None
            self.metadata = None
            sys.exit()
	
		
    #return string
    def __repr__(self):
        """
        This method returns string
        """
        return '%s://%s:%s@%s:5432/%s'%(self.protocol, self.user_name,
                                        self.password, self.host_name,
                                        self.database_name)


#unit test to test the code
import unittest

#define a class for testing
class TestDBConfiguration(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'postgres'
        self.database_config_object = None


    def testDB(self):
        #test to connect to database 
        new_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name, self.database_config_object)
        new_obj.temp_function()
        
        """ to create a database """
        new_obj.create_database()
        
        """ to drop database """
        #new_obj.drop_database()
        
        """ to create new connection """
        new_obj.new_connection()
        
        """ to get list of tables """
        tables = new_obj.get_table_list()
        for i in tables:
            print 'Table is %s'%i
        
        """ to get the columns in a table """
        table_name = 'person2'
        columns = new_obj.get_column_list(table_name)
        for i in columns:
            print 'Column is %s'%i
        
        """ to close the connection """
        new_obj.close_connection()
        
        #new_obj = DataBaseConnection()
        #print 'new object is %s'%new_obj
        #database_config_object = self.database_config_object

        #new_obj.temp_function(new_obj.database_config_object)
        #new_obj.check_if_database_exists(new_obj.database_config_object)
        #new_obj.create_database(new_obj.database_config_object)
        #print 'table is %s'%table_name
        #table_name = 'abc'
        #value = new_obj.check_if_table_exists(table_name, new_obj.database_config_object)
        #new_obj.get_table_desc(table_name, table_name)
        #new_obj.drop_database(new_obj.database_config_object)
        #new_obj.check_if_database_engine_exits(new_obj.database_config_object)

if __name__ == '__main__':
    unittest.main()

#basic functionality working for all
#TODO:
#limit line length to 80 characters
#coding stds
#divide code into modules
            
