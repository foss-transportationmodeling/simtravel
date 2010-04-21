###create class for inserting values into the database.
###check for all types of databases

import sys
import exceptions
import sqlalchemy
from sqlalchemy import create_engine
from newdb import connectDB
from dispdb import displayDB

#class to insert data into the database
class insertDB:
	def __init__(self, dbobj, table_name, result, value):
		#initializing the variables
		self.table_name = table_name
		self.value = value
		self.dbobj = dbobj
		self.result = result

		try:	
			#created an instance of the database object to connect to it		
			self.dbobj = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'connection')
			print self.dbobj
			#try to execute simple insert query
			self.result = self.dbobj.connection.execute("insert into %s values ('%s')" % (self.table_name, self.value))
			
			#after inserting the data, print it
			disp_obj = displayDB(self.dbobj, self.table_name, '', '', self.result)

		
		except Exception, e:
		        #Exception occured. print the error
		        print "Error: %s" %e
			print "Error while inserting and displaying data from the database"


		#close the database connection
		print "Close the connection"
		self.dbobj.conn_close(self.dbobj.connection)

		
#unit test to test the code
import unittest

#define a class for testing
class TestInsertDB(unittest.TestCase):
	#only initialize objects here
	def setUp(self):
		self.dbobj = 'abc'
		self.table_name = 'users'
		self.result = 'xzy'
		self.value = '10'


	def testDB(self):
		#test to insert and then display rows
		DBobj = insertDB(self.dbobj, self.table_name, self.result, self.value)

		
if __name__ == '__main__':
    unittest.main()


#creating an instance of the class.
#dispInstance = insertDB('dbobj', 'users', 'result', '9')
#dispInstance = displayDB()

		

