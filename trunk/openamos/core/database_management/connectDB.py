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
			#print the data that the instance passes to the class			
			print self.hostname
			print self.username
			print self.password
			print self.dbname
			print self.engine
			print self.connection
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



#creating an instance of the class.
#dbInstance = connectDB('localhost', 'postgres', '1234', 'postgres', 'engine', 'conn')
#passing the variable connection using the same instance
#dbInstance.conn_close(dbInstance.connection)


