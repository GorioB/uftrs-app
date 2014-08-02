from lib.app import App
from lib.db2 import User, DropDownMenu
from interface import textfield
from interface.autocomplete import AutocompleteBox
from Tkinter import *
from ttk import *
from main import *
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LogIn(Frame,object):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.app = App()
		self.pack()

		# Window settings
		self.parent.title("UFTRS Program")
		self.parent.geometry("360x400")
		#self.parent.state("zoomed")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		self.logInEntries = []
		self.createEntries = []
		self.changePasswordEntries = []
		self.resetPasswordEntries = []

		if User.listUsers()==[]:
			print "NO USERS YET"
			self.initUI_FirstRun()
		else:
			self.initUI()

	# if no users exist yet
	def initUI_FirstRun(self):
		# Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("360x500")
		#self.parent.state("zoomed")
		self.frame = frame = Frame(self.parent)
		self.frame.pack()

		Label(frame, text="""Hello first time user!\n To begin, register the first account of the system. This account will serve as the administrator account with the highest privileges. i.e. it can edit the budget and register other user accounts.\n"""
			, wraplength=350, justify=CENTER).pack()

		Label(frame, text="Enter username").pack()
		self.first_username = Entry(frame)
		self.first_username.pack()
		Label(frame, text="Enter password").pack()
		self.first_pass = Entry(frame, show="*")
		self.first_pass.pack()
		Label(frame, text="Re-enter password").pack()
		self.first_pass2 = Entry(frame, show="*")
		self.first_pass2.pack()

		Label(frame, text="""\nEnter a secret question for yourself (e.g. "What is your first pet's name?") and the answer to it. This secret question will be used for resetting your password in case you forget it.\n"""
			, wraplength=350, justify=CENTER).pack()

		Label(frame, text="Enter secret question").pack()
		self.first_question = Entry(frame)
		self.first_question.pack()
		Label(frame, text="Enter secret answer").pack()
		self.first_answer = Entry(frame)
		self.first_answer.pack()

		## Submit button and text notifier
		Label(frame, text="").pack()
		self.first_submit = Button(frame, text="Register Account", command=self.submitFirstUser)
		self.first_submit.pack()
		self.first_notifier = Label(frame)
		self.first_notifier.pack()

		#autofocus on first text entry
		self.first_username.focus()
		#bind submitFirstUser to return even on first_pass2
		self.first_pass2.bind("<Return>",self.submitFirstUser)

		self.initDropDownMenus()

	def initDropDownMenus(self):
		"""Initializes the drop down menus list of options"""
		DropDownMenu("Nature").addOption("N/A")
		# TODO: everything else

	def submitFirstUser(self,*a):
		user = User(self.first_username.get(), self.first_pass.get())
		reEnteredPass = self.first_pass2.get()
		secretQ = self.first_question.get()
		secretA = self.first_answer.get()

		if user.password!=reEnteredPass:
			self.first_notifier.config(text="Passwords don't match.", foreground='red')
			return
		elif user.username=="" or user.password=="" or reEnteredPass=="" or secretQ=="" or secretA=="":
			self.first_notifier.config(text="Please fill up all fields.", foreground='red')
			return

		# Save the user into the database
		user.saveUser(secretQ, secretA, 1)

		# Move on to login screen
		self.frame.pack_forget()
		self.frame.destroy()
		self.initUI()

	def initUI(self):
		self.parent.geometry("560x560")

		# Notebook
		self.notebook = Notebook(self.parent)
		self.notes={}
		for i in ["Log In", "Create Account", "Change Password", "Reset Forgotten Password"]:
			self.notes[i]=Frame(self.notebook)
			self.notebook.add(self.notes[i],text=i)
		self.notebook.pack(fill=BOTH,expand=1)
		self.notebook.pack_propagate(0)

		# Log in widgets
		logInFrame = self.notes["Log In"]
		Label(logInFrame, text="Enter username").pack()
		self.logIn_username = Entry(logInFrame)
		self.logIn_username.pack()
		Label(logInFrame, text="Enter password").pack()
		self.logIn_password = Entry(logInFrame,show="*")
		self.logIn_password.pack()
		## Submit button and text notifier
		Label(logInFrame, text="").pack()
		self.logIn_submit = Button(logInFrame, text="Submit", command=self.submitLogIn)
		self.logIn_submit.pack()
		self.logIn_notifier = Label(logInFrame)
		self.logIn_notifier.pack()

		self.logInEntries.append(self.logIn_username)
		self.logInEntries.append(self.logIn_password)

		#press enter to submit
		self.logIn_username.focus()
		self.logIn_password.bind("<Return>",self.submitLogIn)

		# Create account widgets
		## Admin account widgets
		createFrame = self.notes["Create Account"]
		Label(createFrame, text="Enter administrator username").pack()
		self.create_adminUser = Entry(createFrame)
		self.create_adminUser.pack()
		Label(createFrame, text="Enter administrator password").pack()
		self.create_adminPass = Entry(createFrame, show="*")
		self.create_adminPass.pack()
		## New user account widgets
		Label(createFrame, text="").pack()
		Label(createFrame, text="Enter new account's username").pack()
		self.create_newUser = Entry(createFrame)
		self.create_newUser.pack()
		Label(createFrame, text="Enter new account's password").pack()
		self.create_newPass = Entry(createFrame, show="*")
		self.create_newPass.pack()
		Label(createFrame, text="Re-enter new account's password").pack()
		self.create_newPass2 = Entry(createFrame, show="*")
		self.create_newPass2.pack()

		Label(createFrame, text="""\nEnter a secret question for your new account (e.g. "What is your first pet's name?") and the answer to it. This secret question will be used for resetting your password in case you forget it.\n"""
			, wraplength=350, justify=CENTER).pack()

		Label(createFrame, text="Enter new account's secret question").pack()
		self.create_secretQ = Entry(createFrame)
		self.create_secretQ.pack()
		Label(createFrame, text="Enter new account's secret answer").pack()
		self.create_secretA = Entry(createFrame)
		self.create_secretA.pack()

		self.createEntries.append(self.create_adminUser)
		self.createEntries.append(self.create_adminPass)
		self.createEntries.append(self.create_newUser)
		self.createEntries.append(self.create_newPass)
		self.createEntries.append(self.create_newPass2)
		self.createEntries.append(self.create_secretQ)
		self.createEntries.append(self.create_secretA)

		## Submit button and text notifier
		self.create_submit = Button(createFrame, text="Register New User", command=self.submitCreateUser)
		self.create_submit.pack()
		self.create_notifier = Label(createFrame)
		self.create_notifier.pack()

		## bind submitCreateUser to return event on last entry
		self.create_secretA.bind("<Return>",self.submitCreateUser)

		# Change password widgets
		changeFrame = self.notes["Change Password"]
		Label(changeFrame, text="Enter username").pack()
		self.change_user = Entry(changeFrame)
		self.change_user.pack()
		Label(changeFrame, text="Enter password").pack()
		self.change_oldPass = Entry(changeFrame, show="*")
		self.change_oldPass.pack()
		Label(changeFrame, text="").pack()
		Label(changeFrame, text="Enter new password").pack()
		self.change_newPass = Entry(changeFrame, show="*")
		self.change_newPass.pack()
		Label(changeFrame, text="Re-enter new password").pack()
		self.change_newPass2 = Entry(changeFrame, show="*")
		self.change_newPass2.pack()
		## Submit button and text notifier
		Label(changeFrame, text="").pack()
		self.change_submit = Button(changeFrame, text="Change Password", command=self.submitChangePass)
		self.change_submit.pack()
		self.change_notifier = Label(changeFrame)
		self.change_notifier.pack()
		## bind submitChangePass to last entry
		self.change_newPass2.bind("<Return>",self.submitChangePass)

		self.changePasswordEntries.append(self.change_user)
		self.changePasswordEntries.append(self.change_oldPass)
		self.changePasswordEntries.append(self.change_newPass)
		self.changePasswordEntries.append(self.change_newPass2)


		# Reset password widgets
		resetFrame = self.notes["Reset Forgotten Password"]
		Label(resetFrame, text="\nThis page lets you reset your account's password if you've forgotten it.\n").pack()
		## Username selector
		newFrame = Frame(resetFrame)
		newFrame.pack()
		self.reset_userSelector = AutocompleteBox(newFrame, label="Select your username")
		self.reset_userSelector.initDropDown(User.listUsernames())
		self.reset_userSelector.comboBox.bind('<<ComboboxSelected>>', self.handleResetUserSelect)
		self.reset_userSelector.pack()

		Label(resetFrame, text="\n").pack()
		self.reset_secretQ = Label(resetFrame, wraplength=350, justify=CENTER)
		self.reset_secretQ.pack()


		Label(resetFrame, text="\nEnter answer").pack()
		self.reset_answer = Entry(resetFrame)
		self.reset_answer.pack()

		Label(resetFrame, text="Enter new password").pack()
		self.reset_newPass = Entry(resetFrame, show="*")
		self.reset_newPass.pack()
		Label(resetFrame, text="Re-enter new password").pack()
		self.reset_newPass2 = Entry(resetFrame, show="*")
		self.reset_newPass2.pack()

		self.reset_submit = Button(resetFrame, text="Change password", command=self.submitResetPass)
		self.reset_submit.pack()

		self.reset_notifier = Label(resetFrame)
		self.reset_notifier.pack()

		self.resetPasswordEntries.append(self.reset_answer)
		self.resetPasswordEntries.append(self.reset_newPass)
		self.resetPasswordEntries.append(self.reset_newPass2)

	# Callbacks
	def submitLogIn(self,*a):
		user = User(self.logIn_username.get(), self.logIn_password.get())
		if not user.auth():
			self.logIn_notifier.config(text='Wrong credentials. Try again.', foreground='red')
		else:
			# Destroy log in screen
			self.notebook.pack_forget()

			# Move on to main program
			self.parent.geometry("800x500")
			self.mainProgram = mainProgram = MainProgram(self.parent)
			mainProgram.pack(fill=BOTH,expand=1)
			self.mainProgram.bind("<<Logout>>",self.logoutCB)
			mainProgram.app._activeUser = user
			self.clearAllEntries()

	def logoutCB(self,*e):
		self.mainProgram.destroy()
		self.notebook.pack(fill=BOTH,expand=1)
		self.parent.geometry("360x400")
		self.parent.state("normal")

	def submitCreateUser(self,*a):
		admin = User(self.create_adminUser.get(), self.create_adminPass.get())
		newUser = User(self.create_newUser.get(), self.create_newPass.get())
		newUserSecretQ = self.create_secretQ.get()
		newUserSecretA = self.create_secretA.get()
		reEnteredPass = self.create_newPass2.get()

		# Error checking: wrong admin username-password combo
		if not admin.auth():
			self.create_notifier.config(text='Wrong administrator credentials.', foreground='red')
			return
		# Error checking: entered admin account isn't root
		elif not admin.checkIfRoot():
			message = 'User ' + admin.username + ' is not an administrator.'
			self.create_notifier.config(text=message, foreground='red')
			return
		# Error checking: blank fields in new user input fields
		if newUser.username=="" or newUser.password=="" or newUserSecretA=="" or newUserSecretQ=="" or reEnteredPass=="":
			self.create_notifier.config(text='Please fill up all fields.', foreground='red')
			return
		# Error checking: username already taken
		elif User.userExists(newUser.username):
			message = 'Username ' + newUser.username + ' is already taken.'
			self.create_notifier.config(text=message, foreground='red')
			return
		# Error checking: two password fields don't match
		elif newUser.password!=reEnteredPass:
			self.create_notifier.config(text="Passwords don't match", foreground='red')
			return

		# Create the new user
		newUser.saveUser(newUserSecretQ, newUserSecretA)
		self.create_notifier.config(text="New user created.", foreground='darkgreen')
		self.clearCreateAccountEntries()
		# Refresh the Reset Password tab's user drop down menu choices
		self.reset_userSelector.comboBox.config(values=User.listUsernames())

	def submitChangePass(self,*a):
		user = User(self.change_user.get(), self.change_oldPass.get())
		newPass = self.change_newPass.get()
		newPass2 = self.change_newPass2.get()

		# Error checking: username doesn't exist
		if not user.userExists(user.username):
			self.change_notifier.config(text='Username does not exist.', foreground='red')
			return
		# Error checking: wrong password
		elif not user.auth():
			self.change_notifier.config(text='Wrong password.', foreground='red')
			return
		# Error checking: blank fields
		elif newPass=="" or newPass2=="":
			self.change_notifier.config(text='Please fill up all fields.', foreground='red')
			return
		# Error checking: unmatched new passwords
		elif newPass!=newPass2:
			self.change_notifier.config(text="New passwords don't match.", foreground='red')
			return

		user.changePassword(newPass)
		self.change_notifier.config(text="Password successfully changed.", foreground='darkgreen')
		self.clearChangePasswordEntries()

	def submitResetPass(self, *args):
		username = self.reset_userSelector.text
		answer = self.reset_answer.get()
		newPass = self.reset_newPass.get()
		newPass2 = self.reset_newPass2.get()

		# Error checking: username doesn't exist
		if not User.userExists(username):
			self.reset_notifier.config(text="Username does not exist.", foreground='red')
			return
		# Error checking: wrong answer
		elif not User.verifySecretAnswer(username, answer):
			self.reset_notifier.config(text="Wrong answer.", foreground="red")
			return
		# Error checking: blank fields
		elif username=="" or answer=="" or newPass=="" or newPass2=="":
			self.reset_notifier.config(text="Please fill up all fields.", foreground="red")
			return
		elif newPass!=newPass2:
			self.reset_notifier.config(text="New passwords don't match.", foreground="red")
			return

		user = User(username, "")
		user.changePassword(newPass)
		self.reset_notifier.config(text="Password successfully changed.", foreground='darkgreen')
		self.clearResetPasswordEntries()

	def handleResetUserSelect(self, *args):
		username = self.reset_userSelector.text
		self.reset_secretQ.config(text="Question: " + User.getSecretQuestion(username))
		self.clearResetPasswordEntries()

	def clearLogInEntries(self):
		for entryWidget in self.logInEntries:
			entryWidget.delete(0, END)

	def clearCreateAccountEntries(self):
		for entryWidget in self.createEntries:
			entryWidget.delete(0, END)

	def clearChangePasswordEntries(self):
		for entryWidget in self.changePasswordEntries:
			entryWidget.delete(0, END)

	def clearResetPasswordEntries(self):
		for entryWidget in self.resetPasswordEntries:
			entryWidget.delete(0, END)

	def clearAllEntries(self):
		self.clearLogInEntries()
		self.clearCreateAccountEntries()
		self.clearChangePasswordEntries()
		self.clearResetPasswordEntries()


if __name__=="__main__":
	root = Tk()
	app = LogIn(root)
	if os.path.exists(resource_path(os.path.join("assets","logo.gif"))):
		img=PhotoImage(file=resource_path(os.path.join("assets","logo.gif")))
		root.tk.call("wm","iconphoto",root._w,img)
	app.mainloop()