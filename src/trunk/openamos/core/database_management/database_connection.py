#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import sqlalchemy
from sqlalchemy import create_engine
from psycopg2 import extensions
import psycopg2 as dbapi2
from database_configuration import DataBaseConfiguration
from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.orm import mapper
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime


#class to define the database connectio along with other functions
class DataBaseConnection(object):
	"""Database Connection class will connect to the database. It will 
	create a database if none exists. It will also enable creating tables.
	The class will also define methods to drop the database or tables"""

	def __init__(self, protocol = None, user_name = None,
		     password = None, host_name = None, 
		     database_name = None, database_config_object = None, 
		     engine = None, connection = None, 
		     result = None, query = None,
		     metadata = None):

		self.protocol = protocol
		self.user_name = user_name
		self.password = password
		self.host_name = host_name
		self.database_name = database_name
		self.engine = engine
		self.connection = connection
		self.result = result
		self.query = query
		self.metadata = MetaData()

		#create the database object here
		db_obj = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
		database_config_object = db_obj
		self.database_config_object = database_config_object


	#this is a temp function
	#only for testing purpose. it displays the content of the database object
	def temp_function(self, database_config_object):
		print 'function for testing database object'
		#print self.database_config_object.protocol
		#print self.database_config_object.host_name
		#print self.database_config_object.user_name
		#print self.database_config_object.password
		#print self.database_config_object.database_name


	#check if the protocol mentioned in the database object has been installed.
	def check_if_database_engine_exits(self, database_config_object):
		#check the databases installed and save them in an array		
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

		#now check if the protocol in the database configuration object is present in the array
		db_engine = database_config_object.protocol
		if db_engine in database_engine:
			return db_engine
		else:
			raise Exception('Required database is not installed')
	

	#this function checks if there exists any database by the given name.
	#pass the database object as a the parameter
	def check_if_database_exists(self, database_config_object):
		#determine if database exists		
		#returns boolean to the method 
		#before checking database, check if the database is installed
		installed_db = self.check_if_database_engine_exits(database_config_object)
		if installed_db:
			print 'database is installed and it is %s'%installed_db
		else:
			print 'database not installed'

		#create a connect string for the engine
		connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
		self.engine = create_engine(connect_string)
		engine = self.engine
		engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
		self.connection = engine.text("select datname from pg_database").execute()
		result = self.connection
		print 'result is %s'%result
		dbs = [db[0] for db in result.fetchall()]
		database_flag = database_config_object.database_name.lower() in dbs
		if database_flag:
			print 'database exists'
			engine.dispose()
			self.connection.close()
			print 'engine is %s'%engine
			print 'connection is %s'%self.connection
			return 1
		else:
			engine.dispose()
			self.connection.close()
			print 'database does not exist. create a new database'
			return 0


	#this function creates a new database
	def create_database(self, database_config_object):
		print 'database name is %s'%database_config_object.database_name
		db_flag = self.check_if_database_exists(database_config_object)		
		if not db_flag:
			try:
				connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
				self.engine = create_engine(connect_string)
				engine = self.engine
				engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
				self.connection = engine.text("create database %s encoding = 'utf8'"%database_config_object.database_name).execute()
				print 'new database created'
				engine.dispose()
				self.connection.close()
			except:
				raise Exception('Error while creating a new database')
		else:
			print 'no need to create a new database'
			
		
	def drop_database(self, database_config_object):
	#this method wil drop the database
		print 'database name is %s'%database_config_object.database_name
		db_flag = self.check_if_database_exists(database_config_object)		
		if db_flag:
			try:
				connect_string = '%s://%s:%s@%s:5432'%(self.protocol, self.user_name, self.password, self.host_name)
				self.engine = create_engine(connect_string)
				engine = self.engine
				engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
				self.connection = engine.text("drop database %s"%database_config_object.database_name).execute()
				engine.dispose()
				self.connection.close()
				print 'database dropped'
			except:
				raise Exception('Error while deleting a database')


	#create a method for mapper function
	def define_mapping(self, col_types):
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
   
		return filter_data[type_val]
	

	def new_conn(self, database_config_object):
		#create a new connection to the database
		try:
			connect_string = '%s://%s:%s@%s:5432/%s'%(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
			#engine = create_engine('postgres://$self.username:$self.password@$self.hostname:5432/$self.dbname')
			self.engine = create_engine(connect_string)	
			self.connection = self.engine.connect()
			print 'test1'
			self.metadata.bind = self.engine
			#self.metadata(bind = self.engine, schema = self.database_name)		
			print 'new connection'
			print 'metadata is %s'%self.metadata
			#bind the metadata to the engine
			#self.connection.close()
			#if self.connection.closed:
			#	print 'closed'
			#else:
			#	print 'not closed'
		except:
			#print "Error: %s"%e
			raise Exception
		        print "Exiting the program since database connectivity failed"
		        sys.exit()
		

	#check if table exists 
	def check_if_table_exists(self, table_name, database_config_object):
		self.new_conn(database_config_object)
		print self.metadata.sorted_tables
		for t in reversed(self.metadata.sorted_tables):
			print 'table is %s'%t
		#method to be implemented. for now assume table does not exist
		table_exists = 1
		print table_exists
		if table_exists:
			return 1
		else:
			return 0


	#create table. pass the table name and the table description
	#def get_table_desc(self, table_name, table_desc):
		#store the column names and

	def __repr__(self):
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
		self.table_name = 'abc'


	def testDB(self):
		#test to connect to database 
		#new_DBobj = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
		new_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name, self.database_config_object)
		#new_obj = DataBaseConnection()
		print 'new object is %s'%new_obj
		database_config_object = self.database_config_object

		#new_obj.temp_function(new_obj.database_config_object)
		#new_obj.check_if_database_exists(new_obj.database_config_object)
		new_obj.create_database(new_obj.database_config_object)
		new_obj.check_if_table_exists(self.table_name, new_obj.database_config_object)
		#new_obj.drop_database(new_obj.database_config_object)
		#new_obj.check_if_database_engine_exits(new_obj.database_config_object)



if __name__ == '__main__':
    unittest.main()


#TODO:
#limit line length to 80 characters
