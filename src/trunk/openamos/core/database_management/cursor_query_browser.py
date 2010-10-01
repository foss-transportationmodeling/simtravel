#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
from database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime


class MainClass(object):
    #initialize the class 
    def __init__(self, protocol = None, user_name = None,
                    password = None, host_name = None, 
                    database_name = None, engine = None, 
                    connection = None, result = None):

        self.protocol = protocol
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.database_name = database_name
        self.connection = None
        self.result = None
        self.cursor = None
        dbcon_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        self.dbcon_obj = dbcon_obj
        print self.dbcon_obj
    
    
    ########## methods for select query  ##########
    #select all rows from the table
    def select_all_from_table(self, table_name):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Class name corresponding to the table

        Output:
        Returns all the rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            print 'Table %s exists.'%table_name
            try:    
                self.dbcon_obj.cursor.execute("SELECT * FROM %s"%table_name)
                tables = self.dbcon_obj.cursor.fetchall()
                tbs = [tb for tb in tables]
                return self.dbcon_obj.cursor, tbs
            except Exception, e:
                print 'Error while retreiving the data from the table'
                print e
        else:
            print 'Table %s does not exist.'%table_name
    
  
    #select rows based on a selection criteria
    def fetch_selected_rows(self, table_name, column_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in get_cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.'%table_name
            
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute("SELECT * FROM %s where %s = '%s'"%(table_name, column_name, value))
                data = self.dbcon_obj.cursor.fetchall()
    
                row_list = []
                counter = 0
                for each in data:
                    counter = counter + 1
                    row_list.append(each)

                if counter == 0:
                    print 'No rows selected.\n'           
                print 'Select query successful.\n'
                return self.dbcon_obj.cursor, row_list
            except Exception, e:
                print 'Error retrieving the information. Query failed.\n'
                print e
        else:
            print 'Column %s does not belong to the table %s'%(column_name, table_name)
            return None    
    #select join query pending
    ########## methods for select query end ##########
    
    
    ########## methods for delete query  ##########    
    #delete rows based on a deletion criteria
    def delete_selected_rows(self, table_name, column_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in get_cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.'%table_name
            
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s where %s = '%s'"%(table_name, column_name, value))
                self.dbcon_obj.connection.commit()
                print 'Delete successful'
            except Exception, e:
                print e
                print 'Error deleting the information. Query failed.'
        else:
            print 'Column %s does not belong to the table %s. Could not delete rows.'%(column_name, table_name)


    #delete all rows i.e. empty table
    def delete_all(self, table_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            print 'Table %s exists.'%table_name
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s "%table_name)
                self.dbcon_obj.connection.commit()
                print 'Delete all records successful.'
            except Exception, e:
                print e
                print 'Error retrieving the information. Query failed.'
        else:
            print 'Table %s does not exist.'%table_name
            
    ########## methods for delete query end ##########


    ########## methods for insert query     ##########
    #insert values in the table
    def insert_into_table(self, data_arr, table_name):
        """
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            print 'Table %s exists.'%table_name
            try:
                print 'time before insert query ', time.time()
                arr_str = [tuple(each) for each in data_arr]
                arr_str = str(arr_str)[1:-1]
                insert_stmt = "insert into %s values %s"%(table_name, arr_str)
                #insert_stmt = "copy school from '/home/namrata/Documents/DBclasses/myfile.csv' with delimiter as ',' csv header"
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                print 'time after insert query ', time.time()
            except Exception, e:
                print e
        else:
           print 'Table %s does not exist.'%table_name 
    ########## methods for delete query end ##########


    ########## methods for creating and deleting index##########
    #create an index
    def create_index(self, table_name, col_list):
        index_stmt = ''
        columns = ''
        count = 0
        index_name = table_name + '_index'

        for i in col_list:
            if count < (len(col_list)-1):
                columns = columns + i + ', '
                count = count + 1
            else:
                columns = columns + i
        index_stmt = 'create index %s on %s (%s)'%(index_name, table_name, columns)
        print index_stmt
        try:
            self.dbcon_obj.cursor.execute(index_stmt)
            self.dbcon_obj.connection.commit()
            print 'Index %s created'%index_name
        except Exception, e:
            print 'Error while creating an index'
            print e


    #delete an index
    def delete_index(self, table_name):
        index_name = table_name + '_index'
        try:
            self.dbcon_obj.cursor.execute("drop index %s"%index_name)
            self.dbcon_obj.connection.commit()
            print 'Index %s deleted'%index_name
        except Exception, e:
            print 'Error while creating an index'
            print e
        
    ########## methods for creating and deleting index##########



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

    
    def testMainClass(self):
        newobject = MainClass(self.protocol, self.user_name, self.password, self.host_name, self.database_name)

        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        
        table_name = 'asu'
        column_name = 'rol_id'
        value = '1'
        abc = None
        defg = None
        #abc = newobject.fetch_selected_rows(table_name, column_name, value)
        #print abc
        #newobject.fetch_selected_rows(table_name, column_name, value)
        
        #newobject.delete_selected_rows(table_name, column_name, value)

        #newobject.delete_all(table_name)
        
        col_list = ['grad', 'role_id']
        #newobject.create_index(table_name, col_list)
        
        #newobject.delete_index(table_name)

        #data_arr = [('aa','aa','1'),('bb','bb','1')]
        #newobject.insert_into_table(data_arr, table_name)
        
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
