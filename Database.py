import mysqldb as mariadb
class Database:

    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

    def __CreateNewDatabase(self):
        createDatabase = 'CREATE DATABASE NFCRegister;' #Create the database to hold each entity
        #Query to create UserDetails entity
        createUserDetailsEntity = 'CREATE TABLE UserDetails(' \
            + 'UserID SMALLINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
            + 'FirstName VARCHAR(50) NOT NULL, ' \
            + 'Surname VARCHAR(50), ' \
            + 'Authorisation VARCHAR(7) NOT NULL, ' \
            + 'Status VARCHAR(10) NOT NULL DEFAULT "ABSENT");'
        #Query to create Log entity
        createLogEntity = 'CREATE TABLE Log(' \
            + 'LogID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
            + 'FOREIGN KEY (UserID) REFERENCES UserDetails(UserID), ' \
            + 'Type VARCHAR(12) NOT NULL, ' \
            + 'Forced BOOLEAN NOT NULL);'
        #Query to create entity which tracks time of logs
        createEntryTimeEntity = 'CREATE TABLE EntryTime(' \
            + 'FOREIGN KEY (LogID) REFERENCES Log(LogID), ' \
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
        self.__ExecuteSQL(queries)

    def __ExecuteSQL(self, queries):
        for query in range(len(queries)):
            self.cursor.execute(str(queries[query]))
