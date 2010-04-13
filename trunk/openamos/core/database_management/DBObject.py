import sys
import exceptions


#create a database object
class  DBObject(object):
	#init method take the below as args. initializing the db object
	def __init__(self, hostname="", username="", password=""):
		self.hostname = hostname
		self.username = username
		self.password = password
	
	#method to print the args of the db
	def printargs(self):
		print self.hostname
		print self.username
		print self.password
