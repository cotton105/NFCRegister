import os
import MySQLdb as mariadb
from User import User
from Admin import Admin
from Database import Database

global cwd
cwd = os.path.dirname(os.path.realpath(__file__)) #Set the directory to use to be the current working directory

#Run the 'tagtool' which writes the last scanned UID to a file
def GetUserTag():
    os.chdir(cwd+'/nfcpy/examples')
    os.system('python2 tagtool.py --device tty:AMA0:pn532 show')
    #UserID = int(input('UserID: ')) #User enters a UserID manually (to be changed)
    with open('LastTagRead.txt','r') as tagfile:
        UserTag = tagfile.read()
    os.chdir(cwd)
    return UserTag

#Get UserID from matching KeyID from the database
def GetUserID(UserTag):
    UserID = db.GetUserID(UserTag)
    return UserID

def GetNFCRegisterConnection():
    #Establish arguments to use for the connection to the database
    dbConnection = mariadb.connect(host='localhost',
                                   user='dbadmin',
                                   passwd='dbadmin',
                                   port=3306,
                                   db='NFCRegister')
    return dbConnection

#Create the database if it does not already exist
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

#Repeat indefinitely, until KeyboardInterrupt
repeat = True
while repeat:
    tagExists = False
    #Repeat until a card is scanned which is registered to the database
    while not tagExists:
        UserTag = GetUserTag()
        if db.KeyIDExists(UserTag):
            tagExists = True
        else:
            print('The scanned card is not registered to the database.')
    UserID = GetUserID(UserTag)
    Authorisation = db.GetAuthorisation(UserID) #Check the UserID's matching Auth
    if Authorisation == 'STUDENT' or Authorisation == 'TEACHER':
        Person = User(UserTag, db)
    elif Authorisation == 'ADMIN':
        Person = Admin(UserTag, db)
    Person.Register() #Go through all the logic neccessary to register user with the database

db.dbConnection.close() #Finally close the connection to the database so no corruption occurs
