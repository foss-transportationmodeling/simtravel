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

		#print the data
		print self.table_name
		print self.result
		print self.dbobj
		print self.col_name
		print self.value


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


		
#creating an instance of the class.
dispInstance = displayDB('namz', 'users', 'age', '8', 'abc')
#dispInstance = displayDB()


