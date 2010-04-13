###create class for inserting values into the database.
###check for all types of databases

import sys
import exceptions
import sqlalchemy
from sqlalchemy import create_engine
from newdb import connectDB

#class to insert data into the database
class insertDB:
	def __init__(self, dbobj, table_name, result, value):
		#initializing the variables
		self.table_name = table_name
		self.value = value
		self.dbobj = dbobj
		self.result = result

		#print the data
		print self.table_name
		print self.value
		print self.dbobj
		print self.result

		try:	
			#created an instance of the database object to connect to it		
			self.dbobj = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'connection')
			print self.dbobj
			#try to execute simple insert query
			self.result = self.dbobj.connection.execute("insert into %s values ('%s')" % (self.table_name, self.value))
			
			#after inserting the data, print it
			self.result = self.dbobj.connection.execute("select * from %s" %(self.table_name))
			print self.result.fetchall()
			#self.result = self.db.connection.execute("select table_name from information_schema.tables "\
			#					 "where table_schema = 'public'")
			#print self.result.fetchall()
		
		except Exception, e:
		        #Exception occured. print the error
		        print "Error: %s" %e
			print "Error while inserting and displaying data from the database"

		

#creating an instance of the class.
dispInstance = insertDB('dbobj', 'users', 'result', '8')
#dispInstance = displayDB()

		

