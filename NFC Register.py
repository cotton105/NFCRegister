import os
import MySQLdb as mariadb
from User import User
from Admin import Admin
from Database import Database

global cwd
cwd = os.path.dirname(os.path.realpath(__file__))

def GetUserID():
    UserID = int(input('UserID: '))
    return UserID

def GetNFCRegisterConnection():
    dbConnection = mariadb.connect(host='localhost',
                                   user='dbadmin',
                                   passwd='dbadmin',
                                   port=3306,
                                   db='NFCRegister')
    return dbConnection

#Create the database file if it does not already exist
if not os.path.isdir('/var/lib/mysql/NFCRegister'):
    dbConnection = mariadb.connect(host='localhost',
                                   user='dbadmin',
                                   passwd='dbadmin',
                                   port=3306,
                                   db='mysql')
    db = Database(dbConnection)
    db.CreateNewDatabase()
    db = Database(GetNFCRegisterConnection())
    db.AddToNewDatabase()

db = Database(GetNFCRegisterConnection())

UserID = GetUserID()
while UserID != 0:
    Authorisation = db.GetAuthorisation(UserID)
    if Authorisation == 'STUDENT' or Authorisation == 'TEACHER':
        Person = User(UserID, db)
    elif Authorisation == 'ADMIN':
        Person = Admin(UserID, db)
    Person.Register()
    UserID = GetUserID()

db.dbConnection.close()
