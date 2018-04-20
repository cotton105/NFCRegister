import os
import MySQLdb as mariadb
from User import User
from Admin import Admin
from Database import Database

global cwd
cwd = os.path.dirname(os.path.realpath(__file__)) #Set the directory to use to be the current working directory

def GetUserID():
    UserID = int(input('UserID: ')) #User enters a UserID manually (to be changed)
    return UserID

def GetNFCRegisterConnection():
    #Establish arguments to use for the connection to the database
    dbConnection = mariadb.connect(host='localhost',
                                   user='dbadmin',
                                   passwd='dbadmin',
                                   port=3306,
                                   db='NFCRegister')
    return dbConnection

#Create the database file if it does not already exist
if not os.path.isdir('/var/lib/mysql/NFCRegister'): #Check if the specified directory exists at this location
    dbConnection = mariadb.connect(host='localhost',
                                   user='dbadmin',
                                   passwd='dbadmin',
                                   port=3306,
                                   db='mysql')
    db = Database(dbConnection) #Create new database object instance
    db.CreateNewDatabase() #Create the database
    db = Database(GetNFCRegisterConnection()) #Connect to the newly created database
    db.AddToNewDatabase() #Add the necessary entities to the database

db = Database(GetNFCRegisterConnection())

UserID = GetUserID()
while UserID != 0: #Stop program when 0 is entered as a UserID
    Authorisation = db.GetAuthorisation(UserID) #Check the UserID's matching Auth
    if Authorisation == 'STUDENT' or Authorisation == 'TEACHER':
        Person = User(UserID, db)
    elif Authorisation == 'ADMIN':
        Person = Admin(UserID, db)
    Person.Register() #Go through all the logic neccessary to register user with the database
    UserID = GetUserID()

db.dbConnection.close() #Finally close the connection to the database so no corruption occurs
