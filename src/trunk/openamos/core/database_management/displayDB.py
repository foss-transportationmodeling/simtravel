###create class for displaying the contents of the database.


import sys
import exceptions
import sqlalchemy
#from sqlalchemy import create_engine
from newdb import connectDB


#class to display the content of the database
class displayDB:
	def __init__(self, dbobj, table_name, col_name, value, result):
		#initializing the variables
		self.table_name = table_name
		self.result = result
		self.dbobj = dbobj
		self.col_name = col_name
		self.value = value


		try:	
			#created an instance of the database object to connect to it		
			self.dbobj = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'connection')
			print self.dbobj
			
			#check if the column name is specified
			if not self.col_name:			
				#column name is empty. print the whole table				
				print "Column name is empty"
				#try to execute simple select query
				self.result = self.dbobj.connection.execute("select * from %s" %(self.table_name))
				print self.result.fetchall()
			else: 
				#column name is not empty. print the selected details from the table
				print "Column is not empty. print the selective details from the table"
			
				#try to execute simple select query
				self.result = self.dbobj.connection.execute("select * from %s where %s = %s" %(self.table_name, self.col_name, self.value))
				print self.result.fetchall()
				#self.result = self.db.connection.execute("select table_name from information_schema.tables "\
				#					 "where table_schema = 'public'")
				#print self.result.fetchall()
		
		except Exception, e:
			#Exception occured. print the error
		        print "Error: %s" %e
			print "Error while fetching and displaying data from the database"
		

		#close the database connection
		print "Close the connection"
		self.dbobj.conn_close(self.dbobj.connection)


#unit test to test the code
import unittest

#define a class for testing
class TestDisplayDB(unittest.TestCase):
	#only initialize objects here
	def setUp(self):
		self.dbobj = 'abc'
		self.table_name = 'users'
		self.col_name = 'age'
		self.value = '8'
		self.col_name1 = ''
		self.result = 'xzy'


	def testDB(self):
		#test to display rows when value is given
		DBobj = displayDB(self.dbobj, self.table_name, self.col_name, self.value, self.result)		
	
		#test to display rows when value is not given
		DBobj = displayDB(self.dbobj, self.table_name, self.col_name1, self.value, self.result)
		

if __name__ == '__main__':
    unittest.main()

		
#creating an instance of the class.
#dispInstance = displayDB('namz', 'users', 'age', '8', 'abc')
#dispInstance = displayDB()


