###create class for displaying the contents of the database.


import sys
import exceptions
import sqlalchemy
#from sqlalchemy import create_engine
from newdb import connectDB


#class to display the content of the database
class displayDB:
	def __init__(self, dbobj, table_name, result):
		#initializing the variables
		self.table_name = table_name
		self.result = result
		self.dbobj = dbobj

		#print the data
		print self.table_name
		print self.result
		print self.dbobj


		try:	
			#created an instance of the database object to connect to it		
			self.dbobj = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'connection')
			print self.dbobj
			#try to execute simple select query
			self.result = self.dbobj.connection.execute("select * from %s" %(self.table_name))
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
dispInstance = displayDB('namz', 'users', 'abc')
#dispInstance = displayDB()


