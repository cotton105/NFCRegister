from User import User
from tkinter import *
from tkinter.font import Font
import os
class Admin(User): #Inherits the User class
	def _AdminTools(self):
		db = self.db
		self.__actionPerformed = False
		#This loop allows the program to return to an appropriate screen
		#depending on the options the user chooses
		while not self.__actionPerformed:
			self.__adminAction = ''
			self.__GetAdminAction() #Get admin's choice for admin action and update 'adminAction' class attribute
			if self.__adminAction == 'CHANGEATTRIBUTE':
				self.__GetTargetUserID() #Have the admin manually enter the UserID of the user to modify
				if self.__adminAction == 'CHANGEFNAME':
					self.__ChangeFName(self.TargetUserID)
				elif self.__adminAction == 'CHANGESNAME':
					self.__ChangeSName(self.TargetUserID)
				elif self.__adminAction == 'CHANGEAUTH':
					self.__ChangeAuthorisation(self.TargetUserID)
				elif self.__adminAction == 'CHANGESTATUS':
					self.__ChangeStatus(self.TargetUserID)
			elif self.__adminAction == 'SEARCHUSER':
				self.__abortSearch = False
				self.__GetSearchUserName()
				if not self.__abortSearch:
					matchingUsers = self.db.SearchUsers(self.targetFName, self.targetSName)
					try:
						self.__DisplayMatchingUsers(matchingUsers)
					except Exception as e:
						print(e)
						self.mainWindow.destroy()
						self.__NoMatchingUsers()
			elif self.__adminAction == 'VIEWLOGS':
				#Get the whole Log entity from database then display to user
				self.__ViewLogs(db.GetLogs())
			elif self.__adminAction == 'VIEWUSERS':
				#Get the whole UserDetails entity then display
				self.__ViewUsers(db.GetUsers())
			elif self.__adminAction == 'ADDUSER':
				self.__abortNewUser = False
				self.__ScanNewUserCardScreen()
				if not self.__abortNewUser:
					self.__AddNewUser()
			elif self.__adminAction == 'CANCEL':
				print('Action cancelled.')
				self.__actionPerformed = True #Break out of loop to return to register screen

	def __GetAdminAction(self): #Display the screen which allows the user to select an admin option
		self._InitNewScreen('Admin tools', self.normalWindowX)

		#Frame to hold main message and the current time
		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select an admin action to perform.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		#Frame which holds buttons for user to press
		optionsFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		optionsFrame.place(relx=.5, rely=.35, anchor='n')

		changeAttributeButton = Button(optionsFrame, text='Change user attribute', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGEATTRIBUTE'))
		changeAttributeButton.place(relx=.5, rely=0, anchor='n')

		searchUserButton = Button(optionsFrame, text='Search for user', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('SEARCHUSER'))
		searchUserButton.place(relx=.5, rely=.17, anchor='n')

		viewLogsButton = Button(optionsFrame, text='View logs', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('VIEWLOGS'))
		viewLogsButton.place(relx=.5, rely=.34, anchor='n')

		viewUsersButton = Button(optionsFrame, text='View users', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('VIEWUSERS'))
		viewUsersButton.place(relx=.5, rely=.51, anchor='n')

		addUserButton = Button(optionsFrame, text='Add new user', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('ADDUSER'))
		addUserButton.place(relx=.5, rely=.68, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.85, anchor='n')

		self._DateAndTime() #Display date and time in appropriate positions on the main window
		self.mainWindow.mainloop()

	def __SetAdminAction(self, action): #Command when any button is pressed in AdminTools screen
		self.__adminAction = action
		self.mainWindow.destroy()

	def __GetTargetUserID(self): #Retrieve the UserID of the user to modify
		self.__validUserID = False
		while not self.__validUserID:
			self._InitNewScreen('Get UserID', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.25, anchor='n')

			welcomeText = 'Enter the UserID of the user to modify.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			UserIDFrame = Frame(self.mainWindow, height=100, width=350)
			UserIDFrame.place(relx=.43, rely=.4, anchor='n')

			UserIDText = Label(UserIDFrame, text='UserID:', font=self.datetimeDisplayFont)
			UserIDText.place(relx=.28, rely=.33, anchor='n')
			UserIDEntry = Entry(UserIDFrame)
			UserIDEntry.place(relx=.6, rely=.33, anchor='n')
			submitButton = Button(UserIDFrame, text='Submit', font=self.smallButtonFont, bg='green', command=lambda: self.__SetTargetUserID(UserIDEntry.get(), False))
			submitButton.place(relx=.9, rely=.3, anchor='n')

			cancelButton = Button(self.mainWindow, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetTargetUserID(UserIDEntry.get(), True))
			cancelButton.place(relx=.5, rely=.7, anchor='n')

			self._DateAndTime()
			self.mainWindow.mainloop()

	def __SetTargetUserID(self, UserID, setToCancel): #Set the TargetUserID of the user to modify, specified by the admin
		if setToCancel:
			self.__validUserID = True
			self.mainWindow.destroy()
		elif self.__ValidUserID(UserID):
			#Prevent the user modifying themself
			#This can cause issues if they try to change their own status to 'ABSENT'
			if str(UserID) == str(self.UserID):
				self.mainWindow.destroy()
				self._InitNewScreen('Invalid UserID', self.normalWindowX)

				self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
				self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

				welcomeText = 'You cannot modify yourself.'
				welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
				welcomeLabel.place(relx=.5, rely=.1, anchor='n')

				self._DateAndTime()
				self.mainWindow.after(3000, self.mainWindow.destroy) #Close window after about 3 secs
				self.mainWindow.mainloop()
			else:
				self.__validUserID = True
				self.TargetUserID = UserID
				self.mainWindow.destroy()
				self.__GetAttributeToChange()
		else:
			self.mainWindow.destroy()
			self._InitNewScreen('Invalid UserID', self.normalWindowX)

			self.greetingFont = Font(family='Helvetica', size=18)
			self.buttonFont = Font(family='Helvetica', size=14)
			self.datetimeDisplayFont = Font(family='Helvetica', size=12)
			self.smallButtonFont = Font(family='Helvetica', size=8)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

			welcomeText = 'The UserID you entered is invalid.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()

	def __GetAttributeToChange(self): #Display the attributes that the admin can change
		self._InitNewScreen('Get attribute to change', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the attribute to change of {0}.'.format(self.db.GetFirstName(self.TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		optionsFrame.place(relx=.5, rely=.4, anchor='n')

		changeFNameButton = Button(optionsFrame, text='Change First Name', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGEFNAME'))
		changeFNameButton.place(relx=.5, rely=0, anchor='n')

		changeSNameButton = Button(optionsFrame, text='Change Surname', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGESNAME'))
		changeSNameButton.place(relx=.5, rely=.17, anchor='n')

		changeAuthButton = Button(optionsFrame, text='Change Authorisation', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGEAUTH'))
		changeAuthButton.place(relx=.5, rely=.34, anchor='n')

		changeStatusButton = Button(optionsFrame, text='Change Status', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGESTATUS'))
		changeStatusButton.place(relx=.5, rely=.51, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.68, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __ChangeFName(self, TargetUserID): #Manually modify a user's FirstName
		self._InitNewScreen('Change first name', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Enter the new first name for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		entryFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		entryFrame.place(relx=.5, rely=.4, anchor='n')

		#This block creates the whole entry box instance, inc. text and the box itself
		FNameHeight = .1
		FNameText = Label(entryFrame, text='First name:', font=self.datetimeDisplayFont)
		FNameText.place(relx=.33, rely=FNameHeight, anchor='n')
		self.FNameEntry = Entry(entryFrame)
		self.FNameEntry.place(relx=.58, rely=FNameHeight, anchor='n')

		submitButton = Button(entryFrame, text='Submit', font=self.buttonFont, bg='green', command=lambda: self.__SetNewFName(TargetUserID)) #Send all the information to be updated in the database
		submitButton.place(relx=.5, rely=.4, anchor='n')

		cancelButton = Button(entryFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.56, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetNewFName(self, TargetUserID):
		FName = self.FNameEntry.get() #Retrieve the value entered in the entry box previously
		self.mainWindow.destroy()
		if len(FName) == 0: #If entry box is blank
			self._InitNewScreen('Invalid FirstName', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

			welcomeText = 'Value for FirstName cannot be null.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()
		else:
			self.db.ManualChangeFName(TargetUserID, FName) #Make the changes to the database

	def __ChangeSName(self, TargetUserID): #Manually modify a user's Surname
		self._InitNewScreen('Change surname', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Enter the new surname for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		entryFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		entryFrame.place(relx=.5, rely=.4, anchor='n')

		#Text and entry box for new Surname entry
		SNameHeight = .1
		SNameText = Label(entryFrame, text='  Surname:', font=self.datetimeDisplayFont)
		SNameText.place(relx=.33, rely=SNameHeight, anchor='n')
		self.SNameEntry = Entry(entryFrame)
		self.SNameEntry.place(relx=.58, rely=SNameHeight, anchor='n')

		submitButton = Button(entryFrame, text='Submit', font=self.buttonFont, bg='green', command=lambda: self.__SetNewSName(TargetUserID)) #Send all the information to be updated in the database
		submitButton.place(relx=.5, rely=.4, anchor='n')

		cancelButton = Button(entryFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.56, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetNewSName(self, TargetUserID):
		#Unlike FirstName, Surname is allowed to be null
		SName = self.SNameEntry.get()
		self.mainWindow.destroy()
		self.db.ManualChangeSName(TargetUserID, SName) #Make the changes to the database

	def __ChangeAuthorisation(self, TargetUserID): #Manually modify a user's Authorisation
		self._InitNewScreen('Change authorisation', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the new authorisation for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		optionsFrame.place(relx=.5, rely=.4, anchor='n')

		#Radio buttons for new Auth
		#Auth can only be one of these three options
		self.newAuth = StringVar()
		AuthRadioText = Label(optionsFrame, text='Authorisation:', font=self.datetimeDisplayFont)
		AuthRadioText.place(relx=.33, rely=.0, anchor='n')
		AuthRadioStudent = Radiobutton(optionsFrame, text='Student', font=self.entryLabelFont, variable=self.newAuth, value='STUDENT')
		AuthRadioStudent.place(relx=.5, rely=.0, anchor='n')
		AuthRadioTeacher = Radiobutton(optionsFrame, text='Teacher', font=self.entryLabelFont, variable=self.newAuth, value='TEACHER')
		AuthRadioTeacher.place(relx=.5, rely=.10, anchor='n')
		AuthRadioAdmin = Radiobutton(optionsFrame, text='Admin  ', font=self.entryLabelFont, variable=self.newAuth, value='ADMIN')
		AuthRadioAdmin.place(relx=.5, rely=.20, anchor='n')

		submitButton = Button(optionsFrame, text='Submit', font=self.buttonFont, bg='green', command=lambda: self.__SetNewAuth(TargetUserID)) #Send all the information to be updated in the database
		submitButton.place(relx=.5, rely=.40, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.55, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetNewAuth(self, TargetUserID):
		Auth = self.newAuth.get()
		self.mainWindow.destroy()
		if Auth != 'STUDENT' and Auth !='TEACHER' and Auth != 'ADMIN':
			self.__NoOptionSelected()
		else:
			self.db.ManualChangeAuth(TargetUserID, Auth) #Make the changes to the database

	def __ChangeStatus(self, TargetUserID): #Manually modify a user's Status
		self._InitNewScreen('Change status', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the new status for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		optionsFrame.place(relx=.5, rely=.4, anchor='n')

		#Radio buttons for new Status
		#Status can only be one of these three options
		self.newStatus = StringVar()
		StatusRadioText = Label(optionsFrame, text='Status:', font=self.datetimeDisplayFont)
		StatusRadioText.place(relx=.36, rely=.0, anchor='n')
		StatusRadioPresent = Radiobutton(optionsFrame, text='Present     ', font=self.entryLabelFont, variable=self.newStatus, value='PRESENT')
		StatusRadioPresent.place(relx=.5, rely=.0, anchor='n')
		StatusRadioAbsent = Radiobutton(optionsFrame, text='Absent      ', font=self.entryLabelFont, variable=self.newStatus, value='ABSENT')
		StatusRadioAbsent.place(relx=.5, rely=.10, anchor='n')
		StatusRadioLunchbreak = Radiobutton(optionsFrame, text='Lunchbreak', font=self.entryLabelFont, variable=self.newStatus, value='LUNCHBREAK')
		StatusRadioLunchbreak.place(relx=.5, rely=.20, anchor='n')

		submitButton = Button(optionsFrame, text='Submit', font=self.buttonFont, bg='green', command=lambda: self.__SetNewStatus(TargetUserID)) #Send all the information to be updated in the database
		submitButton.place(relx=.5, rely=.40, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.55, anchor='n')

		#Inform the admin what the user's current status is
		UserStatusText = Label(self.mainWindow, text="{0}'s status: {1}".format(self.db.GetFirstName(TargetUserID), self.db.GetStatus(TargetUserID)), font=self.statusFont, fg='grey')
		UserStatusText.place(relx=.5, rely=.8, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetNewStatus(self, TargetUserID):
		Status = self.newStatus.get()
		self.mainWindow.destroy()
		if Status != 'PRESENT' and Status != 'ABSENT' and Status != 'LUNCHBREAK':
			self.__NoOptionSelected()
		else:
			self.db.ManualChangeStatus(TargetUserID, Status) #Make the changes to the database

	def __NoOptionSelected(self):
		self._InitNewScreen('No option selected', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

		welcomeText = 'No option selected.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=0, anchor='n')

		self._DateAndTime()
		self.mainWindow.after(3000, self.mainWindow.destroy)
		self.mainWindow.mainloop()

	def __GetSearchUserName(self): #Prompt user for the name to search for in UserDetails entity
		self._InitNewScreen('Enter user name', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Enter a FirstName, Surname or both.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		entryFrame = Frame(self.mainWindow, height=200, width=self.normalWindowX)
		entryFrame.place(relx=.5, rely=.4, anchor='n')

		EntryBoxX = 300

		#FirstName entry
		FNameEntryY = 0
		FNameEntryText = Label(entryFrame, text='FirstName:', font=self.datetimeDisplayFont)
		FNameEntryText.place(x=(EntryBoxX-125), rely=FNameEntryY, anchor='n')
		self.FNameEntry = Entry(entryFrame)
		self.FNameEntry.place(x=EntryBoxX, rely=FNameEntryY, anchor='n')

		#Surname entry
		SNameEntryY = 0.12
		SNameEntryText = Label(entryFrame, text='  Surname:', font=self.datetimeDisplayFont)
		SNameEntryText.place(x=(EntryBoxX-125), rely=SNameEntryY, anchor='n')
		self.SNameEntry = Entry(entryFrame)
		self.SNameEntry.place(x=EntryBoxX, rely=SNameEntryY, anchor='n')

		searchButton = Button(entryFrame, text='Search', font=self.buttonFont, bg='green', command=self.__SetUserSearch) #Send all the information to be added to the database
		searchButton.place(relx=.5, rely=.3, anchor='n')

		cancelButton = Button(self.mainWindow, text='Cancel', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.5, rely=.85, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetUserSearch(self):
		self.targetFName = self.FNameEntry.get()
		self.targetSName = self.SNameEntry.get()
		self.mainWindow.destroy()
		if len(self.targetFName) == 0 and len(self.targetSName) == 0:
			self.__abortSearch = True
			self._InitNewScreen('No search terms entered', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

			welcomeText = 'You did not provide an FName or SName.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()

	def __DisplayMatchingUsers(self, userRecords): #Show a table of users matching the admin's search terms
		self._InitNewScreen('Display matching users', 700) #Bigger X because table can get bigger

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=700)
		self.welcomeFrame.pack(side=TOP)

		mainTableFrame = Frame(self.mainWindow, height=400, width=684) #Main frame to hold canvas
		self.tableCanvas = Canvas(mainTableFrame) #Canvas to be scrolled and hold table frame
		self.tableFrame = Frame(self.tableCanvas) #Frame to hold the table to be displayed
		self.tableScrollbar = Scrollbar(mainTableFrame, orient='vertical', command=self.tableCanvas.yview) #Scrollbar as table can be long
		self.tableCanvas.config(yscrollcommand=self.tableScrollbar.set) #Set scrollbar to scroll the canvas

		#Organisation of element positions
		mainTableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableScrollbar.pack(side=RIGHT, fill='y', expand=False)
		self.tableCanvas.pack(side=LEFT, fill='both', expand=True)
		self.tableCanvas.create_window((0,0), window=self.tableFrame, anchor='nw')

		self.tableFrame.bind('<Configure>', self.__onFrameConfigure)

		headers = ('UserID', 'KeyID', 'FirstName', 'Surname', 'Authorisation', 'Status') #Define headers of table
		self.__FillTable(userRecords, headers) #Populate table with relevant values

		cancelButton = Button(self.welcomeFrame, text='Return', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.85, rely=.5, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __NoMatchingUsers(self): #Window to display if no users matched the search terms
		self._InitNewScreen('No matching users', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

		welcomeText = 'No matching users.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		self._DateAndTime()
		self.mainWindow.after(3000, self.mainWindow.destroy)
		self.mainWindow.mainloop()

	def __ViewLogs(self, table): #Show table of Log entity in database
		self._InitNewScreen('View logs', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.pack(side=TOP)

		mainTableFrame = Frame(self.mainWindow, height=400, width=484)
		self.tableCanvas = Canvas(mainTableFrame)
		self.tableFrame = Frame(self.tableCanvas)
		self.tableScrollbar = Scrollbar(mainTableFrame, orient='vertical', command=self.tableCanvas.yview)
		self.tableCanvas.config(yscrollcommand=self.tableScrollbar.set)

		mainTableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableScrollbar.pack(side=RIGHT, fill='y', expand=False)
		self.tableCanvas.pack(side=LEFT, fill='both', expand=True)
		self.tableCanvas.create_window((0,0), window=self.tableFrame, anchor='nw')

		self.tableFrame.bind('<Configure>', self.__onFrameConfigure)

		headers = ('LogID', 'UserID', 'Type', 'Forced', 'Date', 'Time')
		self.__FillTable(table, headers)

		cancelButton = Button(self.welcomeFrame, text='Return', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.85, rely=.5, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __ViewUsers(self, table):
		usersWindowWidth = 700 #Window is wider because of wider table
		self._InitNewScreen('View users', usersWindowWidth)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=usersWindowWidth)
		self.welcomeFrame.pack(side=TOP)

		mainTableFrame = Frame(self.mainWindow, height=400, width=684)
		self.tableCanvas = Canvas(mainTableFrame)
		self.tableFrame = Frame(self.tableCanvas)
		self.tableScrollbar = Scrollbar(mainTableFrame, orient='vertical', command=self.tableCanvas.yview)
		self.tableCanvas.config(yscrollcommand=self.tableScrollbar.set)

		mainTableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableFrame.pack(side=LEFT, fill='both', expand=True)
		self.tableScrollbar.pack(side=RIGHT, fill='y', expand=False)
		self.tableCanvas.pack(side=LEFT, fill='both', expand=True)
		self.tableCanvas.create_window((0,0), window=self.tableFrame, anchor='nw')

		self.tableFrame.bind('<Configure>', self.__onFrameConfigure)

		headers = ('UserID', 'KeyID', 'FirstName', 'Surname', 'Authorisation', 'Status')
		self.__FillTable(table, headers)

		cancelButton = Button(self.welcomeFrame, text='Return', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.85, rely=.5, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __onFrameConfigure(self, event):
		self.tableCanvas.config(scrollregion=self.tableCanvas.bbox('all'))

	def __FillTable(self, table, headers): #Logic to insert values into appropriate positions in a table
		#Initially create the headers of the table
		for column in range(len(table[0])):
			headerText = headers[column] #Incrementally go through tuple to insert the correct header
			header = Label(self.tableFrame, text='', font=self.tableFont)
			header.grid(row=0, column=column, sticky='we') #Place the header label in the correct grid pos
			header.config(text=headerText, highlightthickness=1, highlightbackground='grey') #Add correct text and a border to the label
		#Populate the table with values from the database
		for row in range(len(table)): #Number of rows (records) in entity
			for column in range(len(table[0])): #Number of columns in entity
				value = Label(self.tableFrame, text=str(table[row][column]), font=self.tableFont)
				value.grid(row=row + 1, column=column, sticky='we') #Position value (row+1 to compensate for headers row)
				value.config(highlightthickness=1, highlightbackground='grey') #Add border to label

	def __ScanNewUserCardScreen(self):
		self._InitNewScreen('Scan a new card to be used', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

		welcomeText = "Check the console for further instructions."
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=0, anchor='n')

		self._DateAndTime()
		self.mainWindow.after(1000, self.__SetUserTag)
		self.mainWindow.mainloop()

	def __SetUserTag(self):
		print('** SCAN THE CARD TO BE REGISTERED TO THE USER **')
		os.chdir(self.cwd+'/nfcpy/examples')
		os.system('python2 tagtool.py --device tty:AMA0:pn532 show')
		with open('LastTagRead.txt','r') as tagfile:
			UserTag = tagfile.read()
		os.chdir(self.cwd)
		self.newKeyID = UserTag
		self.mainWindow.destroy()
		self.__SetNewUserCard()

	def __SetNewUserCard(self):
		keyExists = self.db.KeyIDExists(self.newKeyID)
		if keyExists:
			self.__abortNewUser = True
			self._InitNewScreen('Card already registered', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

			welcomeText = 'Card already registered to database.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()

	def __AddNewUser(self): #Enter the information for a new user to be added to the database
		self._InitNewScreen('Add a new user', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=150, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.1, anchor='n')

		welcomeText = 'Enter the information for the new user.\nKeyID is: {0}'.format(self.newKeyID)
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=0, anchor='n')

		#Frame for entry boxes to be placed
		entryFrame = Frame(self.mainWindow, height=250, width=self.normalWindowX)
		entryFrame.place(relx=.5, rely=.3, anchor='n')

		EntryX = .6 #Consistent relx value to use for the entry boxes, to keep them aligned

		#FirstName entry
		FNameHeight = .1
		FNameText = Label(entryFrame, text='   First name:', font=self.datetimeDisplayFont)
		FNameText.place(relx=.33, rely=FNameHeight, anchor='n')
		self.FNameEntry = Entry(entryFrame)
		self.FNameEntry.place(relx=EntryX, rely=FNameHeight, anchor='n')

		#Surname entry
		SNameHeight = .2
		SNameText = Label(entryFrame, text='      Surname:', font=self.datetimeDisplayFont)
		SNameText.place(relx=.33, rely=SNameHeight, anchor='n')
		self.SNameEntry = Entry(entryFrame)
		self.SNameEntry.place(relx=EntryX, rely=SNameHeight, anchor='n')

		#Auth radio buttons
		self.newAuth = StringVar()
		AuthRadioText = Label(entryFrame, text='Authorisation:', font=self.datetimeDisplayFont)
		AuthRadioText.place(relx=.33, rely=.35, anchor='n')
		AuthRadioStudent = Radiobutton(entryFrame, text='Student', font=self.entryLabelFont, variable=self.newAuth, value='STUDENT')
		AuthRadioStudent.place(relx=.5, rely=.35, anchor='n')
		AuthRadioTeacher = Radiobutton(entryFrame, text='Teacher', font=self.entryLabelFont, variable=self.newAuth, value='TEACHER')
		AuthRadioTeacher.place(relx=.5, rely=.45, anchor='n')
		AuthRadioAdmin = Radiobutton(entryFrame, text='Admin  ', font=self.entryLabelFont, variable=self.newAuth, value='ADMIN')
		AuthRadioAdmin.place(relx=.5, rely=.55, anchor='n')

		submitButton = Button(entryFrame, text='Submit', font=self.buttonFont, bg='green', command=self.__SetNewUser) #Send all the information to be added to the database
		submitButton.place(relx=.5, rely=.7, anchor='n')

		cancelButton = Button(entryFrame, text='Cancel', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.5, rely=.85, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetNewUser(self): #Set the user information to be added to the database
		valid = True
		validFName = True
		validAuth = True
		KeyID = self.newKeyID
		FName = self.FNameEntry.get()
		SName = self.SNameEntry.get()
		Auth = self.newAuth.get()
		self.mainWindow.destroy()
		if len(FName) == 0: validFName = False #Nothing entered for FName
		if len(Auth) == 0: validAuth = False #Nothing entered for Auth
		if not validFName or not validAuth: #The provided FName and Auth cannot be null (SName can)
			valid = False
		if not valid:
			self._InitNewScreen('Bad user credentials', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
			self.welcomeFrame.place(relx=.5, rely=.4, anchor='n')

			welcomeText = 'No value for "First name" or "Authorisation".'
			self.welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			self.welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()
		else:
			self.db.AddNewUser(KeyID, FName, SName, Auth) #Make the changes to the database

	def __ValidUserID(self, UserID): #Determine whether the UserID provided is above zero and thus is valid
		try:
			if int(UserID) > 0:
				return True
			else:
				return False
		except: #Conversion error from string to int
			return False
