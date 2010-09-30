#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import sqlite3
import psycopg2 as dbapi2
import sqlalchemy
from psycopg2 import extensions
from sqlalchemy.schema import MetaData, Column, Table
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
                database_name = None):


        #create the database object here
        self.protocol = protocol
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    
    #checks if the database engine is installed
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

        database_engine = None
        try:
            import psycopg2
            database_engine = 'postgres'
        except:
            pass

        """
        After storing the installed engies, check if the protocol in
        the database configuration object is present in the array
        """
        db_engine = self.protocol
        if db_engine == database_engine:
            return db_engine
        else:
            raise Exception('Required database is not installed')
            sys.exit()

    
    #checks if the database exists			
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
        Create a connection to the database.
        """
        if self.protocol is 'postgres':
            try:
                #create a connection
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))

                #create a cursor
                self.cursor = self.connection.cursor()
                self.cursor.execute("select datname from pg_database")
                
                dbs = [db[0] for db in self.cursor.fetchall()]
                database_flag = self.database_name.lower() in dbs
		
                #set a flag that indicates the existence of the database.
                if database_flag:
                    print 'Database %s exists'%self.database_name
                    #dispose the engine and close the raw connection
                    self.cursor.close()
                    self.connection.close()
                    return 1
                else:
                    #dispose the engine and close the raw connection			
                    self.cursor.close()
                    self.connection.close()
                    print 'Database does not exist.'
                    return 0
            except Exception, e:
                print e


    #this function creates a new database
    def create_database(self, new_database):
        """
        This method creates a new database by the database name passed 
        in the database configuration object.
    
        Input:
        Database name
        
        Output:
        Database created if it does not exists
        """

        db_flag = self.check_if_database_exists()		
        if not db_flag:
        #since the database does not exist we create a new database.
        #before creating the new database check the protocol.
            try:
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))
                self.cursor = self.connection.cursor()
                self.cursor.execute("create database %s encoding = 'utf8'"%new_database)
                print 'Database %s created'%new_database
            except:
                raise Exception('Error while creating a new database')
        else:
            print 'Database exists. No need to create a new database'


    #drops a database
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
                self.connection = dbapi2.connect("host=%s user=%s password=%s port=5432"%(self.host_name, self.user_name, self.password))
                self.cursor = self.connection.cursor()
                self.cursor.execute("drop database %s"%self.database_name)
                print 'Database dropped'
            except:
                raise Exception('Error while deleting a database')
        else:
            print 'Database does not exists. Cannot drop database.'
    
    
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
        
        #before connecting to the database check if the database exists
        
        #create a connection and try to establish a session with the database
        try:
            self.connection = dbapi2.connect("host=%s dbname=%s user=%s password=%s port=5432"%(self.host_name, self.database_name, self.user_name, self.password))
            self.cursor = self.connection.cursor()
            print 'New connection created.\n'
        except Exception, e:
            print "Exiting the program since database connectivity failed"
            print e

    
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
            print "Closing the database connection."
            self.cursor.close()
            self.connection.close()
            if self.connection.closed:
                print 'Connection to database closed.\n'
            else:
                print 'Connection to database not closed.\n'
        except:
            print "Error while closing the database connection. Exiting the program."
            self.cursor = None
            self.connection = None
            sys.exit()
    

    #define mapping for the columns and datatypes                
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

    #check if table exists 
    def check_if_table_exists(self, table_name):
        """
        This method checks if the table exists in the database.

        Input:
        Table name

        Output:
        Return boolean indicating the table exists or not
        """
        self.table_name = table_name
        try:
            self.cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = 'public'")
            tables = self.cursor.fetchall()
            tbs = [tb[0] for tb in tables]
            table_exists = self.table_name in tbs
            return table_exists
        except:
            print 'Error when checking for existing tables'
            raise Exception


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
            self.cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = 'public'")
            tables = self.cursor.fetchall()
            tbs = [tb[0] for tb in tables]
            return tbs
        except:
            print 'Error while fetching the tables from the database'
            raise Exception


    #get the list of tables from the database
    def get_column_list(self, table_name):
        """
        This method is used to fetch the list of all tables in the database.

        Input:
        Database configuration object

        Output:
        List of the tables in the database.
        """
        self.table_name = table_name
        #before returning the columns check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            try:
                self.cursor.execute("select column_name from information_schema.columns where table_name = %s"%table_name)
                columns = self.cursor.fetchall()
                cols = [cl[0] for cl in columns]
                return cols
            except:
                print 'Error while fetching the columns from the table'
                raise Exception
        else:
            print 'Table %s does not exist. Cannot get the column list'%table_name


    #get the description of the table
    def get_table_desc(self, columns, ctypes, keys):
        """
        This method is used to get the description of the table.
        The method returns the columns with the datatypes and keys if any. It 
        calls the mapping function to obtain the datatypes of the columns.
        
        Input:
        Column names, their datatypes and keys in the form of lists.
        All three lists have one to one mapping
        
        Output:
        Returns the columns of the table in the required format.        
        """
        #store the column names, datatypes and keys in local variables
        col_names = columns
        col_types = ctypes
        key_types = keys
        table_columns = []

        for col, ctype, ktype in zip(col_names, col_types, key_types):
            #ktype identifies if key is a primary or not
            if ktype == "1":
                column = Column(col, self.define_mapping(ctype), primary_key=True)
            else:
                column = Column(col, self.define_mapping(ctype))
            table_columns.append(column)
            
        return table_columns


    #creates a new table
    def create_table(self, table_name, columns):
        """
        This method is used to create new table in the database.

        Input:
        Database configuration object and table name

        Output:
        New table created
        table_name, columns, ctypes, keys
        """
        #before creating a new table check if that table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            print 'Table already exists in the database. No need to create a new table'
        else:
            #create a new table since it does not exist
            print 'Table does not exist. Create a new table'
            try:
                self.cursor.execute("create table %s %s"%(self.table_name, columns))
                self.connection.commit()
                print "Table '%s' created"%self.table_name
            except Exception, e:
                print 'Error while creating the table %s'%self.table_name
                print e


    #drop the table
    def drop_table(self, table_name):
        """
        This method is used to drop the table from the database

        Input:
        Database configuration object and table name

        Output:
        Table is dropped from the database
        """
        
        #before dropping the table check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            #table exists and hence can be dropped
            print 'Table exists in the database.'
            self.cursor.execute("drop table %s"%self.table_name)
            self.connection.commit()
        else:
            print 'Table does not exist in the database. Cannot the drop the table'


    #temp function prints the values of the database configuration object	
    def temp_function(self):
        """
        This is a test function.
        It displays the values of the database configuration object

        Input:
        Database configuration object
		
        Output:
        Display the object details
        """

        print 'protocol is %s'%self.protocol
        print 'host name is %s'%self.host_name
        print 'user name is %s'%self.user_name
        print 'password is %s'%self.password
        print 'database name is %s'%self.database_name
        print 'cursor is %s'%self.cursor
        print 'connection is %s\n'%self.connection



#unit test to test the code
import unittest

#define a class for testing
class TestDataBaseConnection(unittest.TestCase):
	#only initialize objects here
	def setUp(self):
		self.protocol = 'postgres'		
		self.user_name = 'postgres'
		self.password = '1234'
		self.host_name = 'localhost'
		self.database_name = 'postgres'


	def testDB(self):
	    print 'test'
		#test to connect to database 
		#dbobj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
		#print dbobj
		#dbobj.new_connection()
        """
        table_name = 'abc'
        columns = ['aa','bb','cc','dd']
        ctypes = ['integer','integer', 'integer', 'integer']
        keys = ['1','0','0','0']
        column = ' '
        for col, ctype, key in zip(columns, ctypes, keys):
            if key == '1':
                column = column + col + ' ' + ctype + ' primary key,'
            else:
                column = column + col + ' ' + ctype + ','
        column = '('+column[1:-1]+')'
        print 'haha',column,'hehe'
        """
        #dbobj.create_table(table_name, column)
        #dbobj.drop_table(table_name)
        #dbobj.close_connection()


if __name__ == '__main__':
    unittest.main()
	

