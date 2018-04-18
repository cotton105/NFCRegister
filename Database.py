import time
import MySQLdb as mariadb
from tkinter import *
class Database:
	def __init__(self, dbConnection):
		self.dbConnection = dbConnection
		self.__cur = self.dbConnection.cursor()

	def CreateNewDatabase(self):
		createDatabase = 'CREATE DATABASE NFCRegister;' #Create the database to hold each entity
		self.__ExecuteSQL(createDatabase)

	def AddToNewDatabase(self): #Procedure to create entities and add one user to the new database
		#Query to create UserDetails entity
		createUserDetailsEntity = 'CREATE TABLE UserDetails(' \
			+ 'UserID SMALLINT(5) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
			+ 'KeyID CHAR(14) NOT NULL, ' \
			+ 'FirstName VARCHAR(50) NOT NULL, ' \
			+ 'Surname VARCHAR(50) DEFAULT NULL, ' \
			+ 'Authorisation VARCHAR(7) NOT NULL , ' \
			+ 'Status VARCHAR(10) NOT NULL DEFAULT "ABSENT");'
		#Query to create Log entity
		createLogEntity = 'CREATE TABLE Log(' \
			+ 'LogID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
			+ 'UserID SMALLINT UNSIGNED NOT NULL, ' \
			+ 'FOREIGN KEY UserID (UserID) REFERENCES UserDetails(UserID), ' \
			+ 'Type VARCHAR(12) NOT NULL, ' \
			+ 'Forced BOOLEAN NOT NULL);'
		#Query to create entity which tracks time of logs
		createEntryTimeEntity = 'CREATE TABLE EntryTime(' \
			+ 'LogID INT UNSIGNED NOT NULL, ' \
			+ 'FOREIGN KEY LogID (LogID) REFERENCES Log(LogID), ' \
			+ 'Date DATE NOT NULL, ' \
			+ 'Time TIME NOT NULL);'
		#Query to ensure at least one admin is registered, so that changes can be made
		createAdmin = 'INSERT INTO UserDetails(' \
			+ 'FirstName, Authorisation) ' \
			+ 'VALUES("Admin", "ADMIN");'
		queries = (createUserDetailsEntity,
				   createLogEntity,
				   createEntryTimeEntity,
				   createAdmin)
		#Execute each query in consecutive order
		for query in range(len(queries)):
			self.__ExecuteSQL(str(queries[query]))

	def GetFirstName(self, UserID):
		query = 'SELECT FirstName FROM UserDetails WHERE UserID = {0};'.format(UserID)
		FirstName = self.__ReturnOneSQL(query)
		return FirstName

	def GetAuthorisation(self, UserID):
		query = 'SELECT Authorisation FROM UserDetails WHERE UserID = {0};'.format(UserID)
		Authorisation = self.__ReturnOneSQL(query)
		return Authorisation

	def GetStatus(self, UserID):
		query = 'SELECT Status FROM UserDetails WHERE UserID = {0};'.format(UserID)
		Status = self.__ReturnOneSQL(query)
		return Status

	def UpdateStatus(self, UserID, Status):
		query = 'UPDATE UserDetails SET Status = "{0}" WHERE UserID = {1};'.format(Status, UserID)
		self.__ExecuteSQL(query)

	def __ExecuteSQL(self, query):
		print('Query: {0}'.format(query))
		try:
			self.__cur.execute(query)
			self.dbConnection.commit()
		except Exception as e:
			print(e)
			self.dbConnection.rollback()

	def __ReturnOneSQL(self, query):
		print('Query: {0}'.format(query))
		self.__cur.execute(query)
		result = (self.__cur.fetchone())[0] #Get the value retrieved by the cusor execution, and convert from tuple to string
		print(result)
		return result

	def __ReturnAllSQL(self, query):
		print('Query: {0}'.format(query))
		self.__cur.execute(query)
		result = self.__cur.fetchall()
		print(result)
		return result

	def AddLog(self, UserID, Type, Forced):
		currentTime = time.strftime('%H:%M:%S')
		currentDate = time.strftime('%Y-%m-%d')
		query = 'INSERT INTO Log(UserID, Type, Forced) VALUES({0}, "{1}", {2});'.format(UserID, Type, Forced)
		self.__ExecuteSQL(query)
		query = 'SELECT LogID, MIN(LogID) AS most_recent_record FROM Log;'
		LogID = self.__ReturnOneSQL(query)
		query = 'INSERT INTO EntryTime(LogID, Date, Time) VALUES(last_insert_id(), "{0}", "{1}");'.format(currentDate, currentTime)
		self.__ExecuteSQL(query)

	def ManualChangeFName(self, TargetUserID, FName): #(Admin) Manually modify a user's FirstName
		self.AddLog(TargetUserID, 'FNAMECHANGE', True)
		query = 'UPDATE UserDetails SET FirstName = "{0}" WHERE UserID = {1};'.format(FName, TargetUserID)
		self.__ExecuteSQL(query)

	def ManualChangeSName(self, TargetUserID, SName): #(Admin) Manually modify a user's Surname
		self.AddLog(TargetUserID, 'SNAMECHANGE', True)
		query = 'UPDATE UserDetails SET Surname = "{0}" WHERE UserID = {1};'.format(SName, TargetUserID)
		self.__ExecuteSQL(query)

	def ManualChangeAuth(self, TargetUserID, Auth): #(Admin) Manually modify a user's Authorisation
		self.AddLog(TargetUserID, 'AUTHCHANGE', True)
		query = 'UPDATE UserDetails SET Authorisation = "{0}" WHERE UserID = {1};'.format(Auth, TargetUserID)
		self.__ExecuteSQL(query)

	def ManualChangeStatus(self, TargetUserID, Status): #(Admin) Manually modify a user's Status
		self.AddLog(TargetUserID, 'STATUSCHANGE', True)
		self.UpdateStatus(TargetUserID, Status)

	def AddNewUser(self, FName, SName, Auth): #(Admin) Add a new user into the UserDetails entity
		query = 'INSERT INTO UserDetails(FirstName, Surname, Authorisation) VALUES("{0}", "{1}", "{2}");'.format(FName, SName, Auth)
		self.__ExecuteSQL(query)
		query = 'SELECT last_insert_id() FROM Log;'
		self.AddLog(self.__ReturnOneSQL(query), 'NEWUSER', True)

	def __ValidAuthorisation(self, Authorisation): #Determine whether the Authorisation string passed is valid
		if Authorisation == 'STUDENT' or Authorisation == 'TEACHER' or Authorisation == 'ADMIN':
			return True
		else:
			return False

	def GetLogs(self): #(Admin) Display all the records in the Log entity
		query = 'SELECT Log.LogID, Log.UserID, Log.Type, Log.Forced, EntryTime.Date, EntryTime.Time ' \
				'FROM Log, EntryTime ' \
				'WHERE Log.LogID = EntryTime.LogID ' \
				'ORDER BY EntryTime.Date, EntryTime.Time ASC;'
		logTable = self.__ReturnAllSQL(query)
		'''
		print('+-------+--------+------------+--------+----------+--------+\n' \
			  '| LogID | UserID |    Type    | Forced |   Date   |  Time  |\n' \
			  '+-------+--------+------------+--------+----------+--------+')
		for row in logTable:
			print('|{0:<7}|{1:<8}|{2:<12}|{3:<8}|{4:<10}|{5:<8}|'.format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])))
		print('+-------+--------+------------+--------+----------+--------+')
		'''
		return logTable

	def GetUsers(self):
		query = 'SELECT * FROM UserDetails;'
		userTable = self.__ReturnAllSQL(query)
		'''
		print('+--------+--------------------+--------------------+---------------+----------+\n' \
			  '| UserID |     FirstName      |      Surname       | Authorisation |  Status  |\n' \
			  '+--------+--------------------+--------------------+---------------+----------+')
		for row in userTable:
			print('|{0:<8}|{1:<20}|{2:<20}|{3:<15}|{4:<10}|'.format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))
		print('+--------+--------------------+--------------------+---------------+----------+')
		'''
		return userTable
