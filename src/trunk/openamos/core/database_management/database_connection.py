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


class Temp(object): pass

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
                metadata = None, table_name = None,
                session = None):

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
        test_variable = ''
        self.new_user = None

        #create the database object here
        db_obj = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        database_config_object = db_obj
        self.database_config_object = database_config_object


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

        print 'protocol is %s'%self.database_config_object.protocol
        print 'host name is %s'%self.database_config_object.host_name
        print 'user name is %s'%self.database_config_object.user_name
        print 'password is %s'%self.database_config_object.password
        print 'database name is %s'%self.database_config_object.database_name
	
    
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
            dbname = self.database_config_object.database_name
            #give the entire file path for the database.
            try:
                if os.path.isfile(dbname):
                    print 'Database %s exists'%self.database_config_object.database_name
                    return 1
                else:
                    print 'Database does not exist.'
                    return 0
            except:
                raise Exception('Error while checking for the database')

       
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
        #since the database does not exist we create a new database.
        #before creating the new database check the protocol.
            if self.database_config_object.protocol is 'postgres':
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
            elif self.database_config_object.protocol is 'mysql':
                print 'Protocol is mysql'
            elif self.database_config_object.protocol is 'mssql':
                print 'Protocol is mssql'
            elif self.database_config_object.protocol is 'sqlite':
                print 'Protocol is sqlite'
                try:
                    db_path = self.database_config_object.database_name
                    """
                    self.connection = sqlite3.connect(db_path)
                    db_cursor = self.connection.cursor()
                    db_cursor.execute('CREATE TABLE TEST (a INTEGER);')
                    except sqlite3.OperationalError, msg:
                    print msg
                    """    
                    print 'db_path is %s'%db_path
                    connect_string = '%s:///%s'%s(self.protocol, db_path)
                    print 'connect_string is %s'%connect_string
                    engine = self.engine
                    print 'test2'
                    engine = create_engine(connect_string)
                    print 'test3'
                    self.connection = engine.connect()
                    print 'New database created.'
                    engine.dispose()
                    self.connection.close()
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
                connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
                self.engine = create_engine(connect_string)
                engine = self.engine
                engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.connection = engine.text("drop database %s"%self.database_config_object.database_name).execute()
                engine.dispose()
                self.connection.close()
                print 'Database dropped'
            except:
                raise Exception('Error while deleting a database')
        else:
            print 'Database does not exists. Cannot drop database.'
    
            
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
            print 'New connection created'
            self.metadata = MetaData(
                        bind = self.engine
                        )
            Session = sessionmaker(bind=self.engine, autoflush=True, autocommit=True)
            self.session = Session()                  
        except Exception, e:
            print "Exiting the program since database connectivity failed"
            #raise Exception e
            print e
            #sys.exit()
		

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
            table_exists = self.engine.has_table(table_name = table_name)
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
            result = self.connection.execute("SELECT * FROM pg_tables where schemaname = 'public'")
            table_names = result.fetchall()
            table_array = [tb[1] for tb in table_names]
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

        self.table_name = table_name
        #before returning the columns check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            #table exists
            print 'Table exists in the database.'
            column_list = []
            temp = None
            columns = Table(self.table_name, self.metadata, autoload=True)
            for c in columns.c:
                temp = str(c)
                parts = temp.split(".")
                column_list.append(parts[1])

            return column_list
        else:
            print 'Table does not exists. Cannot return the column list'


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
    def create_table(self, table_name, columns, ctypes, keys):
        """
        This method is used to create new table in the database.

        Input:
        Database configuration object and table name

        Output:
        New table created
        """
        
        #before creating a new table check if that table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            print 'Table already exists in the database. No need to create a new table'
        else:
            #create a new table since it does not exist
            print 'Table does not exist. Create a new table'
            #get the description of the table
            table_columns = self.get_table_desc(columns, ctypes, keys)
            try:
                new_table = Table(
                        self.table_name,
                        self.metadata,
                        *table_columns
                        )
                #create new table                         
                new_table.create(checkfirst = True)
                print "Table '%s' created"%self.table_name
                #create a mapper for the table
                #mapper(Temp, new_table)
                #create an object for the mapper
                #self.new_user = Temp()
                #print self.new_user
            except:
                print 'Error while creating the table %s'%self.table_name
                raise Exception
            
        
    #separate function for mapper
    def table_mapper(self, table_name):
        """
        This method is used to create a mapper to the table in the database
        
        Input:
        Table name
        
        Output:
        Creates a table object
        """
        
        #before creating the mapper check if the table exists
        self.table_name = table_name
        table_flag = self.check_if_table_exists(table_name)
        if table_flag:
            #table exists
            try:
                #load the table
                new_table = Table(self.table_name, self.metadata, autoload=True)
                #get the attributes
                #dir_before = dir(self.new_user)
                #before_len = len(dir_before)
                print 'table name is %s'%self.table_name
                #create mapper
                mapper(Temp, new_table)
                print 'session object is %s'%self.session

                #create an object for the mapper
                self.new_user = Temp()
                print 'mapper object is %s'%self.new_user
                #get attributes after 
                #dir_after = dir(self.new_user)
                #after_len = len(dir_after)
                #length = after_len - before_len - 1
                #temp_len = before_len + length
                #print 'temp len i s%s'%temp_len
                #print 'test'
                #print dir(self.new_user)[temp_len]
                #print 'length is %s'%length

            except:
                #print 'Failed to create mapper'
                raise Exception                                
        else:
            print 'Table does not exist in the database. Cannot create a mapper'
            
    
    #insert values in the table
    def insert_into_table(self):
        """
        This method is used to insert new values into the table.

        Input:
        Database configuration object, table name and values

        Output:
        Values inserted in to the table
        """
        """
        #(self, table_name, values)
        #check for tables that are present in metadata
        #print self.metadata.tables.keys()
        #print self.metadata
        print 'inside insert into method'
        self.new_user.first_name = 'arun'
        self.new_user.last_name = 'bapat'
        print 'first name is %s and last name is %s'%(self.new_user.first_name, self.new_user.last_name)
        print 'try inserting the values in the table'
        self.session.add(self.new_user)
        self.session.flush()
        self.session.commit()
        print 'test'
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


    #select all rows from the table
    def select_all_fom_table(self):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Database configuration object and table name

        Output:
        Returns all the rows in the table
        """
        
        #get the column list for the table
        col = []
        temp_table = Table(self.table_name, self.metadata, autoload=True)
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)

        #query the table to fetch all the records by passing the columns
        query = self.session.query(Temp).values(*col)
        #print 'query is %s'%query
        
        all_rows = []
        for instance in query:
            print instance
            all_rows.append(instance)

        #print 'final list'
        #for x in all_rows:
        #    print x
        #print 'session is %s'%self.session
        #for obj in self.session:
        #    print obj
          
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
    def fetch_selected_rows(self, table_name, column_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Returns the rows that satisfy the selection criteria
        """
        
        #get the column list for the table
        col = []
        temp_table = Table(self.table_name, self.metadata, autoload=True)
        print 'table object is %s'%temp_table.__table__.columns
        for cl in temp_table.c:
            #print 'column is %s'%cl
            col.append(cl)
            
        #print 'column name is %s'%column_name
        #print 'table name is %s'%table_name
        #print 'value is %s\n'%value
        print 'trial'
        list1 = self.new_user.__class__.__dict__.items()
        for i in list1:
            print i
        print ' '
        try:
            query = self.session.query(Temp).filter(getattr(Temp, column_name) == value).values(*col)
            #print query
            row_list = []
            counter = 0
            for each in query:
                counter = counter + 1
                row_list.append(each)
            #print 'counter is %s'%counter            
            #print 'row list is %s'%row_list
            if counter == 0:
                print 'No rows selected.'
            else:
                for each_ins in row_list:
                    print each_ins            
            print '\nSelect query successful'
        except:
            print 'Error retrieving the information. Query failed.'            


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
            table = Table(self.table_name, self.metadata, autoload=True)
            tab = self.metadata.tables[self.table_name]
            print 'tab is %s'%tab
            tab.drop(bind = self.engine)
            print 'table dropped'
            print tab
        else:
            print 'Table does not exist in the database. Cannot the drop the table'
        

    #obtain the reverse mapping of the columns
    def get_reverse_mapping(self, table_name):
        """
        This method is used to get the reverse mapping of a table.

        Input:
        Database configuration object and table name.

        Output:
        Returns the column names and the datatypes
        """

    #select and print the join
    def select_join(self, table1_list, table2_list):
        """
        This method is used to select the join of tables and display them.
        
        Input:
        Database configuration object, table names, columns and values.
        
        Output:
        Dsiplays the rows based on the join and the selection criterion.
        """
        #for now send no args
        #currently the code works for 2 tables
        #list1 = ['person', 'first_name', 'last_name']
        #list2 = ['office','role', 'years']
        list1 = table1_list
        list2 = table2_list
        #initialize the variables
        final_list = []
        table_list = []
        table1 = None
        table2 = None
        ctr = 0
        #separate the column names and table names and append them to lists
        for w in list1:
            if ctr == 0:
                table1 = w
                table_list.append(w)
                ctr = ctr +1
            else:
                final_list.append(w)
        ctr = 0
        for x in list2:
            if ctr == 0:
                table2 = x
                table_list.append(x)
                ctr = ctr +1
            else:        
                final_list.append(x)
        """
        print 'columns are'
        for y in final_list:
            print y
        print 'tables are'
        for z in table_list:
            print z
        """
        #use string manipulation to create the select query
        len1 = len(final_list)
        len2 = len(table_list)
        ctr = 0
        sql_string = "select "
        for i in final_list:
            if int(ctr) < (int(len1)-1):
                sql_string = sql_string + str(i) + ', '
                ctr = ctr + 1
            else:
                sql_string = sql_string + str(i) + ' '
        sql_string = sql_string + 'from '
        #print sql_string
        
        ctr = 0
        for i in table_list:
            if int(ctr) < (int(len2)-1):
                sql_string = sql_string + str(i) + ', '
                ctr = ctr + 1
            else:
                sql_string = sql_string + str(i) + ' '
        sql_string = sql_string + 'where person.role_id = office.role_id'
        print sql_string
        for_key = None
        try:
            temp_table1 = Table(table1, self.metadata, autoload=True)
            temp_table2 = Table(table2, self.metadata, autoload=True)
            """
            keys1 = temp_table1.foreign_keys
            keys2 = temp_table2.foreign_keys
            if keys1 <> None:
                for i in keys1:
                    print 'keys1 %s'%i
            elif keys2 <> None:
                for j in keys2:
                    print 'keys2 %s'%j
            """
            result = self.connection.execute(sql_string)
            rows = result.fetchall()
            for each_row in rows:
                print each_row
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'            
        

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
        #new_obj.temp_function()
        
        """ to create a database """
        #new_obj.create_database()
        
        """ to drop database """
        #new_obj.drop_database()
        
        """ to create new connection """
        new_obj.new_connection()
      
        """ to create a new table """
        table_name = 'asu'
        columns = ["grad", "undergrad"]
        ctypes = ["VARCHAR", "VARCHAR"]
        keys = ["1","0"]

        #new_obj.create_table(table_name, columns, ctypes, keys)

        #print " "
                        
        """ to get list of tables """
        #tables = new_obj.get_table_list()
        #for i in tables:
        #    print 'Table is %s'%i

        #print " "
        
        """ to get the columns in a table """
        #table_name = 'table123'
        #columns = None
        #columns = new_obj.get_column_list(table_name)
        #if columns <> None:
        #    for i in columns:
        #        print 'Column is %s'%i
        #else:
        #    print 'No columns returned'                
        #        
        #print " "
        
        """ to drop the table """
        #table_name = 'table1'
        #new_obj.drop_table(table_name)
        
        #print " "
        
        """ to create a mapper """
        table_name = 'person'
        new_obj.table_mapper(table_name)
        
        print " " 
                        
        """ to insert values into the table """
        #new_obj.insert_into_table()
        
        """ to delete selected rows """
        value = 'bauer'
        #new_obj.delete_selected_rows(value)
        
        """ to select all rows from the table """
        #new_obj.select_all_fom_table()
        
        """ to select few rows """
        table_name = 'person'
        column_name = 'first_name'
        value = 'seema'
        #new_obj.fetch_selected_rows(table_name, column_name, value)
        print ' '
        
        """ to print the join """
        table1_list = ['person', 'first_name', 'last_name']
        table2_list = ['office','role', 'years']
        new_obj.select_join(table1_list, table2_list)
        
        """ to close the connection """
        new_obj.close_connection()



if __name__ == '__main__':
    unittest.main()

#basic functionality working for all
#TODO:
#limit line length to 80 characters
#coding stds
#divide code into modules
            
