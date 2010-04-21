###create class for connecting to the database.
###check for all types of databases - for now postgresql using sqlalchemy

import sys
import exceptions
import sqlalchemy
from sqlalchemy import create_engine


#class to connect to the database
class connectDB:
	def __init__(self, hostname, username, password, dbname, engine, connection):
		#initializing the variables		
		self.hostname = hostname
		self.username = username
		self.password = password
		self.dbname = dbname
		
		#use the engine to connect to the database
		try:
			#engine used to connect to database. 
			#pass all the required data like hostname username password database name			
			self.engine = create_engine('postgres://postgres:1234@localhost:5432/postgres')
			#engine = create_engine('postgres://$self.username:$self.password@$self.hostname:5432/$self.dbname')
			self.connection = self.engine.connect()
			print 'Connection to database successful'

		except Exception, e:
			#exception occured. print the error. exit the program		        
			print "Error: %s" %e
			print "Exiting the program since database connectivity failed"
			sys.exit()


	#method to close the connection to the database
	def conn_close(self,connection):
		try:		
			#close the connection			
			connection.close()
			print "Connection to the database closed"	
		except:
			#exception occured. print the error and exit the program
			print "Error: %s" %e
			print "Exiting the program since disconnecting the database failed"
			sys.exit()



#unit test to test the code
import unittest

#define a class for testing
class TestConnectDB(unittest.TestCase):
	#only initialize objects here
	def setUp(self):
		self.hostname = 'localhost'
		self.username = 'postgres'
		self.password = '1234'
		self.dbname = 'postgres'
		self.engine = 'engine'
		self.connection = 'abc'

	def testDB(self):
		#test to connect to database 
		DBobj = connectDB(self.hostname, self.username, self.password, self.dbname, self.engine, self.connection)
		connection = self.connection		
	
		#test to disconnect from the database
		DBobj.conn_close(DBobj.connection)


if __name__ == '__main__':
    unittest.main()

#creating an instance of the class.
#dbInstance = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'conn')
#passing the variable connection using the same instance
#dbInstance.conn_close(dbInstance.connection)


