import time
import os
import MySQLdb as mariadb
from tkinter import *
class Database:
	def __init__(self, dbConnection):
		self.dbConnection = dbConnection
		self.__cur = self.dbConnection.cursor()
		self.cwd = os.path.dirname(os.path.realpath(__file__))

	def CreateNewDatabase(self):
		createDatabase = 'CREATE DATABASE NFCRegister;' #Create the database to hold each entity
		self.__ExecuteSQL(createDatabase)

	def AddToNewDatabase(self): #Procedure to create entities and add one user to the new database
		#Query to create UserDetails entity
		createUserDetailsEntity = 'CREATE TABLE UserDetails(' \
			'UserID SMALLINT(5) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
			'KeyID CHAR(14) NOT NULL, ' \
			'FirstName VARCHAR(50) NOT NULL, ' \
			'Surname VARCHAR(50) DEFAULT NULL, ' \
			'Authorisation VARCHAR(7) NOT NULL , ' \
			'Status VARCHAR(10) NOT NULL DEFAULT "ABSENT");'
		#Query to create Log entity
		createLogEntity = 'CREATE TABLE Log(' \
			'LogID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
			'UserID SMALLINT UNSIGNED NOT NULL, ' \
			'FOREIGN KEY UserID (UserID) REFERENCES UserDetails(UserID), ' \
			'Type VARCHAR(12) NOT NULL, ' \
			'Forced BOOLEAN NOT NULL);'
		#Query to create entity which tracks time of logs
		createEntryTimeEntity = 'CREATE TABLE EntryTime(' \
			'LogID INT UNSIGNED NOT NULL, ' \
			'FOREIGN KEY LogID (LogID) REFERENCES Log(LogID), ' \
			'Date DATE NOT NULL, ' \
			'Time TIME NOT NULL);'
		#Ensure at least one admin is registered, so that changes can be made
		adminTag = self.__GetAdminTag()
		createAdmin = 'INSERT INTO UserDetails(' \
			'KeyID, FirstName, Authorisation) ' \
			'VALUES("{0}", "Master", "ADMIN");'.format(adminTag)
		queries = (createUserDetailsEntity,
				   createLogEntity,
				   createEntryTimeEntity,
				   createAdmin)
		#Execute each query in consecutive order
		for query in range(len(queries)):
			self.__ExecuteSQL(str(queries[query]))

	def __GetAdminTag(self):
		print('** SCAN THE CARD TO BE USED FOR THE ADMIN **')
		os.chdir(self.cwd+'/nfcpy/examples')
		os.system('python2 tagtool.py --device tty:AMA0:pn532 show')
		with open('LastTagRead.txt','r') as tagfile:
			tag = tagfile.read()
		os.chdir(self.cwd)
		return tag

	def GetUserID(self, KeyID):
		query = 'SELECT UserID FROM UserDetails WHERE KeyID = "{0}";'.format(KeyID)
		UserID =  self.__ReturnOneSQL(query)
		return UserID

	#Function to get the FirstName of a user based on the provided UserID
	def GetFirstName(self, UserID):
		query = 'SELECT FirstName FROM UserDetails WHERE UserID = {0};'.format(UserID)
		FirstName = self.__ReturnOneSQL(query)
		return FirstName

	#Function to get the Authorisation of a user
	def GetAuthorisation(self, UserID):
		query = 'SELECT Authorisation FROM UserDetails WHERE UserID = {0};'.format(UserID)
		Authorisation = self.__ReturnOneSQL(query)
		return Authorisation

	#Get the Status of a user
	def GetStatus(self, UserID):
		query = 'SELECT Status FROM UserDetails WHERE UserID = {0};'.format(UserID)
		Status = self.__ReturnOneSQL(query)
		return Status

	#Update the status of a user
	def UpdateStatus(self, UserID, Status):
		query = 'UPDATE UserDetails SET Status = "{0}" WHERE UserID = {1};'.format(Status, UserID)
		self.__ExecuteSQL(query)

	#Execute any query provided through the parameter
	def __ExecuteSQL(self, query):
		print('Query: {0}'.format(query))
		try:
			self.__cur.execute(query)
			self.dbConnection.commit() #Make the changes to the database
		except Exception as e: #Output error and rollback the database
			print(e)
			self.dbConnection.rollback()

	#Execute an SQL query and retrieve a single value from a table in the cursor (SELECT queries)
	def __ReturnOneSQL(self, query):
		print('Query: {0}'.format(query))
		self.__cur.execute(query)
		result = (self.__cur.fetchone())[0] #Get the value retrieved by the cusor execution, and convert from tuple to string
		print(result)
		return result

	#Retrieve many values from a table
	def __ReturnManySQL(self, query):
		print('Query: {0}'.format(query))
		self.__cur.execute(query)
		result = self.__cur.fetchmany()
		print(result)
		return result

	#Retrieve a whole table
	def __ReturnAllSQL(self, query):
		print('Query: {0}'.format(query))
		self.__cur.execute(query)
		result = self.__cur.fetchall()
		print(result)
		return result

	#Create a new entry in Log and EntryTime tables
	def AddLog(self, UserID, Type, Forced):
		currentTime = time.strftime('%H:%M:%S') #Get current time in 24hr form
		currentDate = time.strftime('%Y-%m-%d') #Get current date in ISO 8601 format
		query = 'INSERT INTO Log(UserID, Type, Forced) VALUES({0}, "{1}", {2});'.format(UserID, Type, Forced) #Insert into Log
		self.__ExecuteSQL(query)
		query = 'SELECT LogID, MIN(LogID) AS most_recent_record FROM Log;' #Identify the most recent log in the Log table
		LogID = self.__ReturnOneSQL(query)
		query = 'INSERT INTO EntryTime(LogID, Date, Time) VALUES(last_insert_id(), "{0}", "{1}");'.format(currentDate, currentTime)  #Insert into EntryTime
		self.__ExecuteSQL(query)

	#(Admin) Manually modify a user's FirstName
	def ManualChangeFName(self, TargetUserID, FName):
		self.AddLog(TargetUserID, 'FNAMECHANGE', True)
		query = 'UPDATE UserDetails SET FirstName = "{0}" WHERE UserID = {1};'.format(FName, TargetUserID)
		self.__ExecuteSQL(query)
	#(Admin) Manually modify a user's Surname
	def ManualChangeSName(self, TargetUserID, SName):
		self.AddLog(TargetUserID, 'SNAMECHANGE', True)
		query = 'UPDATE UserDetails SET Surname = "{0}" WHERE UserID = {1};'.format(SName, TargetUserID)
		self.__ExecuteSQL(query)
	#(Admin) Manually modify a user's Authorisation
	def ManualChangeAuth(self, TargetUserID, Auth):
		self.AddLog(TargetUserID, 'AUTHCHANGE', True)
		query = 'UPDATE UserDetails SET Authorisation = "{0}" WHERE UserID = {1};'.format(Auth, TargetUserID)
		self.__ExecuteSQL(query)
	#(Admin) Manually modify a user's Status
	def ManualChangeStatus(self, TargetUserID, Status):
		self.AddLog(TargetUserID, 'STATUSCHANGE', True)
		self.UpdateStatus(TargetUserID, Status)

	#(Admin) Add a new user into the UserDetails entity
	def AddNewUser(self, KeyID, FName, SName, Auth):
		query = 'INSERT INTO UserDetails(KeyID, FirstName, Surname, Authorisation) VALUES("{0}", "{1}", "{2}", "{3}");'.format(KeyID, FName, SName, Auth)
		self.__ExecuteSQL(query)
		query = 'SELECT last_insert_id() FROM Log;'
		self.AddLog(self.__ReturnOneSQL(query), 'NEWUSER', True)

	#Determine whether the Authorisation string passed is valid
	def __ValidAuthorisation(self, Authorisation):
		if Authorisation == 'STUDENT' or Authorisation == 'TEACHER' or Authorisation == 'ADMIN':
			return True
		else:
			return False

	#(Admin) Retrieve all the records in the Log entity
	def GetLogs(self):
		query = 'SELECT Log.LogID, Log.UserID, Log.Type, Log.Forced, EntryTime.Date, EntryTime.Time ' \
			'FROM Log, EntryTime ' \
			'WHERE Log.LogID = EntryTime.LogID ' \
			'ORDER BY EntryTime.Date, EntryTime.Time ASC;'
		logTable = self.__ReturnAllSQL(query)
		return logTable

	#Construct a query to search for someone's record in UserDetails table then execute
	def SearchUsers(self, FName, SName):
		if len(FName) > 0 and len(SName) > 0: #When both FName and SName are specified
			whereClause = 'FirstName = "{0}" AND Surname = "{1}"'.format(FName, SName)
		elif len(FName) > 0 and len(SName) == 0: #Only FName is specified
			whereClause = 'FirstName = "{0}"'.format(FName)
		elif len(SName) > 0 and len(FName) == 0: #Only SName is specified
			whereClause = 'Surname = "{0}"'.format(SName)
		query = 'SELECT * FROM UserDetails WHERE {0};'.format(whereClause)
		matchingUsers = self.__ReturnAllSQL(query)
		return matchingUsers

	#Retrieve entire UserDetails table
	def GetUsers(self):
		query = 'SELECT * FROM UserDetails;'
		userTable = self.__ReturnAllSQL(query)
		return userTable

	def KeyIDExists(self, keyID):
		query = 'SELECT * FROM UserDetails WHERE KeyID = "{0}"'.format(keyID)
		result = self.__ReturnAllSQL(query)
		if len(result) >= 1:
			return True
		else:
			return False
