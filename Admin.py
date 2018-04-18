from User import User
from tkinter import *
from tkinter.font import Font
class Admin(User): #Inherits the User class
	def _AdminTools(self):
		db = self.db
		self.__actionPerformed = False
		while not self.__actionPerformed:
			self.__GetAdminAction()
			if self.__adminAction == 'CHANGEATTRIBUTE':
				self.__GetTargetUserID()
				if self.__adminAction == 'CHANGEFNAME':
					self.__ChangeFName(self.TargetUserID)
				elif self.__adminAction == 'CHANGESNAME':
					self.__ChangeSName(self.TargetUserID)
				elif self.__adminAction == 'CHANGEAUTH':
					self.__ChangeAuthorisation(self.TargetUserID)
				elif self.__adminAction == 'CHANGESTATUS':
					self.__ChangeStatus(self.TargetUserID)
			elif self.__adminAction == 'SEARCHUSER':
				self.__EnterUserName()
			elif self.__adminAction == 'VIEWLOGS':
				self.__ViewLogs(db.GetLogs())
			elif self.__adminAction == 'VIEWUSERS':
				self.__ViewUsers(db.GetUsers())
			elif self.__adminAction == 'ADDUSER':
				self.__AddNewUser()
			elif self.__adminAction == 'CANCEL':
				print('Action cancelled.')
				self.__actionPerformed = True

	def __GetAdminAction(self): #Display the screen which allows the user to select an admin option
		self._InitNewScreen('Admin tools', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select an admin action to perform.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=500)
		optionsFrame.place(relx=.5, rely=.35, anchor='n')

		changeAttributeButton = Button(optionsFrame, text='Change user attribute', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('CHANGEATTRIBUTE'))
		changeAttributeButton.place(relx=.5, rely=0, anchor='n')

		viewLogsButton = Button(optionsFrame, text='View logs', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('VIEWLOGS'))
		viewLogsButton.place(relx=.5, rely=.17, anchor='n')

		viewUsersButton = Button(optionsFrame, text='View users', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('VIEWUSERS'))
		viewUsersButton.place(relx=.5, rely=.34, anchor='n')

		addUserButton = Button(optionsFrame, text='Add new user', font=self.buttonFont, bg='dodger blue', command=lambda: self.__SetAdminAction('ADDUSER'))
		addUserButton.place(relx=.5, rely=.51, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetAdminAction('CANCEL'))
		cancelButton.place(relx=.5, rely=.68, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetAdminAction(self, action):
		self.__adminAction = action
		self.mainWindow.destroy()

	def __GetTargetUserID(self): #Retrieve the UserID of the user to modify from the admin
		self.__validUserID = False
		while not self.__validUserID:
			self._InitNewScreen('Get UserID', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
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
			if str(UserID) == str(self.UserID): #Prevent the user modifying themself: this can cause issues if they try to change their own status to 'ABSENT'
				self.mainWindow.destroy()
				self._InitNewScreen('Invalid UserID', self.normalWindowX)

				self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
				self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

				welcomeText = 'You cannot modify yourself.'
				welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
				welcomeLabel.place(relx=.5, rely=.1, anchor='n')

				self._DateAndTime()
				self.mainWindow.after(3000, self.mainWindow.destroy)
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

			self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
			self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

			welcomeText = 'The UserID you entered is invalid.'
			welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			welcomeLabel.place(relx=.5, rely=.1, anchor='n')

			self._DateAndTime()

			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()

	def __GetAttributeToChange(self): #Display the attributes that the admin can change
		self._InitNewScreen('Get attribute to change', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the attribute to change of {0}.'.format(self.db.GetFirstName(self.TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=500)
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

	def __ChangeFName(self, TargetUserID): #(Admin) Manually modify a user's Authorisation
		self._InitNewScreen('Change first name', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Enter the new first name for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		entryFrame = Frame(self.mainWindow, height=200, width=500)
		entryFrame.place(relx=.5, rely=.4, anchor='n')

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
		FName = self.FNameEntry.get()
		self.mainWindow.destroy()
		self.db.ManualChangeFName(TargetUserID, FName) #Make the changes to the database

	def __ChangeSName(self, TargetUserID): #(Admin) Manually modify a user's Authorisation
		self._InitNewScreen('Change surname', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Enter the new surname for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		entryFrame = Frame(self.mainWindow, height=200, width=500)
		entryFrame.place(relx=.5, rely=.4, anchor='n')

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
		SName = self.SNameEntry.get()
		self.mainWindow.destroy()
		self.db.ManualChangeSName(TargetUserID, SName) #Make the changes to the database

	def __ChangeAuthorisation(self, TargetUserID): #(Admin) Manually modify a user's Authorisation
		self._InitNewScreen('Change authorisation', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the new authorisation for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=500)
		optionsFrame.place(relx=.5, rely=.4, anchor='n')

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

	def __ChangeStatus(self, TargetUserID): #Get the status to change to
		self._InitNewScreen('Change status', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Select the new status for {0}.'.format(self.db.GetFirstName(TargetUserID))
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=200, width=500)
		optionsFrame.place(relx=.5, rely=.4, anchor='n')

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

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

		welcomeText = 'No option selected.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=0, anchor='n')

		self._DateAndTime()
		self.mainWindow.after(3000, self.mainWindow.destroy)
		self.mainWindow.mainloop()

	def __EnterUserName(self):
		self._InitNewScreen('Enter user name', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.1)

		welcomeText = 'Enter a FirstName, Surname or both.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=2, anchor='n')



	def __ViewLogs(self, table):
		self._InitNewScreen('View logs', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=self.normalWindowX)
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
		usersWindowWidth = 700
		self._InitNewScreen('View users', usersWindowWidth)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=usersWindowWidth)
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

		headers = ('UserID', 'KeyID', 'FirstName', 'Surname', 'Authorisation', 'Status')
		self.__FillTable(table, headers)

		cancelButton = Button(self.welcomeFrame, text='Return', font=self.buttonFont, bg='red', command=self.mainWindow.destroy)
		cancelButton.place(relx=.85, rely=.5, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __onFrameConfigure(self, event):
		self.tableCanvas.config(scrollregion=self.tableCanvas.bbox('all'))

	def __FillTable(self, table, headers): #Logic to insert values into appropriate positions in a table
		for column in range(len(table[0])):
			headerText = headers[column]
			header = Label(self.tableFrame, text='', font=self.tableFont)
			header.grid(row=0, column=column, sticky='we')
			header.config(text=headerText, highlightthickness=1, highlightbackground='grey')
		for row in range(len(table)):
			for column in range(len(table[0])):
				value = Label(self.tableFrame, text=str(table[row][column]), font=self.tableFont)
				value.grid(row=row + 1, column=column, sticky='we')
				value.config(highlightthickness=1, highlightbackground='grey')

	def __AddNewUser(self): #Enter the information for a new user to be added to the database
		self._InitNewScreen('Add a new user', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
		self.welcomeFrame.place(relx=.5, rely=.1, anchor='n')

		welcomeText = 'Enter the information for the new user.'
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.2, anchor='n')

		entryFrame = Frame(self.mainWindow, height=250, width=500)
		entryFrame.place(relx=.5, rely=.3, anchor='n')

		EntryX = .6 #Consistent relx value to use for the entry boxes, to keep them aligned

		FNameHeight = .1
		FNameText = Label(entryFrame, text='   First name:', font=self.datetimeDisplayFont)
		FNameText.place(relx=.33, rely=FNameHeight, anchor='n')
		self.FNameEntry = Entry(entryFrame)
		self.FNameEntry.place(relx=EntryX, rely=FNameHeight, anchor='n')

		SNameHeight = .2
		SNameText = Label(entryFrame, text='      Surname:', font=self.datetimeDisplayFont)
		SNameText.place(relx=.33, rely=SNameHeight, anchor='n')
		self.SNameEntry = Entry(entryFrame)
		self.SNameEntry.place(relx=EntryX, rely=SNameHeight, anchor='n')

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

	def __SetNewUser(self): #Set the information to be added to the database
		valid = True
		validFName = True
		validAuth = True
		FName = self.FNameEntry.get()
		if len(FName) == 0: validFName = False
		SName = self.SNameEntry.get()
		Auth = self.newAuth.get()
		self.mainWindow.destroy()
		if len(Auth) == 0: validAuth = False
		if not validFName or not validAuth:
			valid = False
		if not valid:
			self._InitNewScreen('Bad user credentials', self.normalWindowX)

			self.welcomeFrame = Frame(self.mainWindow, height=100, width=500)
			self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

			welcomeText = 'No value for "First name" or "Authorisation".'
			self.welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
			self.welcomeLabel.place(relx=.5, rely=0, anchor='n')

			self._DateAndTime()
			self.mainWindow.after(3000, self.mainWindow.destroy)
			self.mainWindow.mainloop()
		else:
			self.db.AddNewUser(FName, SName, Auth) #Make the changes to the database

	def __ValidUserID(self, UserID): #Determine whether the UserID provided is above zero and thus is valid
		try:
			if int(UserID) > 0:
				return True
			else:
				return False
		except:
			return False
