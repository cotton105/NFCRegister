from Database import Database
from tkinter import *
from tkinter.font import Font
import time
import os
class User:
	#Set all relevant attributes to User object
	def __init__(self, KeyID, db):
		self.db = db
		self.KeyID = KeyID
		self.UserID = db.GetUserID(KeyID)
		self.FirstName = self.db.GetFirstName(self.UserID) #Attribute for user FirstName
		self.Authorisation = self.db.GetAuthorisation(self.UserID) #Attribute for user Auth
		self.Status = self.db.GetStatus(self.UserID) #Attribute for user Status
		self.cwd = os.path.dirname(os.path.realpath(__file__))
		self.normalWindowX = 500 #Consistent window width to use for most windows
		self.normalWelcomeFrameHeight = 100 #Consistent welcome frame height for most windows

	#Determine whether user is signing in or out, and display the appropriate screen
	def Register(self):
		db = self.db
		SignInOrOut = self.__GetLogType() #Determine whether user is signing in or out
		actionPerformed = False
		while not actionPerformed: #Always loop back to this screen unless user selects a registration option or cancels
			if SignInOrOut == 'SIGNIN': #When user is currently Absent
				self.__signInOption = ''
				self.__GetSignInOption() #Change signInOption attribute to the option that the user chooses
				if self.__signInOption == 'SIGNIN':
					db.AddLog(self.UserID, 'SIGNIN', False) #Add appropriate log to database
					db.UpdateStatus(self.UserID, 'PRESENT') #Change the user's status accordingly
					self.__RegisteredScreen() #Inform the user that their request and been acknowledged
					actionPerformed = True
				elif self.__signInOption == 'CANCEL':
					print('Action cancelled.')
					actionPerformed = True
			elif SignInOrOut == 'SIGNOUT': #When user is currently Present
				self.__signOutOption = ''
				self.__GetSignOutOption()
				if self.__signOutOption == 'SIGNOUT':
					db.AddLog(self.UserID, 'SIGNOUT', False)
					db.UpdateStatus(self.UserID, 'ABSENT')
					self.__RegisteredScreen()
					actionPerformed = True
				elif self.__signOutOption == 'LUNCHBREAK':
					db.AddLog(self.UserID, 'LUNCHBREAK', False)
					db.UpdateStatus(self.UserID, 'LUNCHBREAK')
					self.__RegisteredScreen()
					actionPerformed = True
				elif self.__signOutOption == 'TOOLS' and self.Authorisation == 'ADMIN':
					self._AdminTools()
				elif self.__signOutOption == 'TOOLS' and self.Authorisation != 'ADMIN':
					print('Invalid option.')
				elif self.__signOutOption == 'CANCEL':
					print('Action cancelled.')
					actionPerformed = True

	#Use current Status to determine whether user signs in or out
	def __GetLogType(self):
		if self.Status == 'PRESENT':
			return 'SIGNOUT'
		elif self.Status == 'ABSENT' or self.Status == 'LUNCHBREAK':
			return 'SIGNIN'

	#Run when user signs in
	def __GetSignInOption(self):
		self.signInOption = ''
		self._InitNewScreen('Register', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = 'Welcome, {0}.'.format(self.FirstName)
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=100, width=self.normalWindowX)
		optionsFrame.pack(side=LEFT)

		signInButton = Button(optionsFrame, text='Sign in', font=self.buttonFont, bg='green', command=lambda: self.__SetSignInOption('SIGNIN'))
		signInButton.place(relx=.5, rely=.333, anchor='center')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetSignInOption('CANCEL'))
		cancelButton.place(relx=.5, rely=.666, anchor='center')

		#Remind the user of their current status
		statusText = 'Your status is: {0}'.format(self.Status)
		statusLabel = Label(self.mainWindow, text=statusText, font=self.statusFont, fg='grey')
		statusLabel.place(relx=.5, rely=.8, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetSignInOption(self, option):
		self.__signInOption = option
		self.mainWindow.destroy()

	#Run when user signs out
	def __GetSignOutOption(self):
		self.signOutOption = ''
		self._InitNewScreen('Register', self.normalWindowX)

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.2, anchor='n')

		welcomeText = '{0}, select your reason for signing out.'.format(self.FirstName)
		welcomeLabel = Label(self.welcomeFrame, text=welcomeText, font=self.greetingFont)
		welcomeLabel.place(relx=.5, rely=.1, anchor='n')

		optionsFrame = Frame(self.mainWindow, height=150, width=self.normalWindowX)
		optionsFrame.place(relx=.5, rely=.33, anchor='n')

		signOutButton = Button(optionsFrame, text='Sign out', font=self.buttonFont, bg='yellow', command=lambda: self.__SetSignOutOption('SIGNOUT'))
		signOutButton.place(relx=.38, rely=.2, anchor='n')

		lunchbreakButton = Button(optionsFrame, text='Lunchbreak', font=self.buttonFont, bg='yellow', command=lambda: self.__SetSignOutOption('LUNCHBREAK'))
		lunchbreakButton.place(relx=.62, rely=.2, anchor='n')

		if self.Authorisation == 'ADMIN': #Only display this button if the user is an admin
			toolsButton = Button(optionsFrame, text='Admin tools', font=self.buttonFont, bg='blue', command=lambda: self.__SetSignOutOption('TOOLS'))
			toolsButton.place(relx=.5, rely=.425, anchor='n')

		cancelButton = Button(optionsFrame, text='Cancel', font=self.buttonFont, bg='red', command=lambda: self.__SetSignOutOption('CANCEL'))
		cancelButton.place(relx=.5, rely=.65, anchor='n')

		statusText = 'Your status is: {0}'.format(self.Status)
		statusLabel = Label(self.mainWindow, text=statusText, font=self.statusFont, fg='grey')
		statusLabel.place(relx=.5, rely=.8, anchor='n')

		self._DateAndTime()
		self.mainWindow.mainloop()

	def __SetSignOutOption(self, option):
		self.__signOutOption = option
		self.mainWindow.destroy()

	#Notification to inform the user that the program has adhered to their sign in/out option
	def __RegisteredScreen(self):
		self.Status = self.db.GetStatus(self.UserID) #Update user's Status attribute
		self._InitNewScreen('Registered', self.normalWindowX)

		self.dateLabel = Label(self.mainWindow, text=time.strftime('%-d %b %Y'), font=self.datetimeDisplayFont)
		self.dateLabel.place(anchor='nw')

		self.welcomeFrame = Frame(self.mainWindow, height=self.normalWelcomeFrameHeight, width=self.normalWindowX)
		self.welcomeFrame.place(relx=.5, rely=.35, anchor='n')

		#Update string to display, based on user's updated status
		if self.Status == 'PRESENT':
			registerType = 'in'
		elif self.Status == 'ABSENT' or self.Status == 'LUNCHBREAK':
			registerType = 'out'
		registeredText = '{0}, you are now signed {1}.'.format(self.FirstName, registerType)
		registeredLabel = Label(self.welcomeFrame, text=registeredText, font=self.greetingFont)
		registeredLabel.place(relx=.5, rely=.33, anchor='n')

		windowCloseText = 'This window will close in three seconds.'
		windowCloseLabel = Label(self.welcomeFrame, text=windowCloseText, font=self.datetimeDisplayFont)
		windowCloseLabel.place(relx=.5, rely=.66, anchor='n')

		statusText = 'Your status is: {0}'.format(self.Status)
		statusLabel = Label(self.mainWindow, text=statusText, font=self.statusFont, fg='grey')
		statusLabel.place(relx=.5, rely=.8, anchor='n')

		self.mainWindow.after(3000, self.mainWindow.destroy)
		self.mainWindow.mainloop()

	#The basic format of every window to be used throughout the program
	def _InitNewScreen(self, title, windowX):
		self.mainWindow = Tk()
		windowY = 500
		#screenX = self.mainWindow.winfo_screenwidth()
		#screenY = self.mainWindow.winfo_screenheight()
		#x = (screenX/2) - (windowX/2)
		#y = (screenY/2) - (windowY/2)
		self.mainWindow.geometry('{0}x{1}+{2}+{3}'.format(windowX, windowY, 200, 200))
		self.mainWindow.title(title)
		self.mainWindow.resizable(width=False, height=False)
		#self.mainWindow.update_idletasks()
		#self.mainWindow.overrideredirect(True) #Remove border around window which includes min, max and X buttons

		#All fonts available to display in the program
		self.greetingFont = Font(family='Helvetica', size=18)
		self.buttonFont = Font(family='Helvetica', size=14)
		self.smallButtonFont = Font(family='Helvetica', size=8)
		self.entryLabelFont = Font(family='Helvetica', size=10)
		self.datetimeDisplayFont = Font(family='Helvetica', size=12)
		self.statusFont = Font(family='Helvetica', size=12)
		self.tableFont = Font(family='Calibri', size=12)

	#Display date and time in appropriate postitions on the window
	def _DateAndTime(self):
		self.dateLabel = Label(self.mainWindow, font=self.datetimeDisplayFont)
		self.dateLabel.place(anchor='nw')

		self.clock = Label(self.welcomeFrame, font=self.datetimeDisplayFont)
		self.clock.place(relx=.5, rely=.4, anchor='n')

		self.falsetime = ''
		self._UpdateDateAndTime()

	#Dynamically update the date and time display on the window using recursion
	def _UpdateDateAndTime(self):
		self.currentTime = time.strftime('%H:%M:%S') #Format string of the current time in 24hr format
		self.currentDate = time.strftime('%-d %b %Y') #Format date in d/m/y format
		#Update if the time is different from last check
		if self.currentTime != self.falsetime:
			self.falsetime = self.currentTime
			self.clock.config(text=self.currentTime)
			self.dateLabel.config(text=self.currentDate)
		self.mainWindow.after(200, self._UpdateDateAndTime) #Repeat every 1/5th of a second to emulate a dynamic clock
