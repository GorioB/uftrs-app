from lib.app import App
from lib.db2 import User
from interface import textfield
from Tkinter import *
from ttk import *
from main import *
import os

class LogIn(Frame,object):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.app = App()
		self.pack()

		# Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("360x400")
		#self.parent.state("zoomed")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		if User.listUsers()==[]:
			print "NO USERS YET"
			self.initUI_FirstRun()
		else:
			self.initUI()

	# if no users exist yet
	def initUI_FirstRun(self):
		# Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("360x400")
		#self.parent.state("zoomed")
		self.frame = frame = Frame(self.parent)
		self.frame.pack()

		Label(frame, text="""Hello first time user!\n To begin, register the first account of the system. This account will serve as the administrator account with the highest privileges. i.e. it can edit the budget and register other user accounts.\n"""
			, wraplength=350, justify=CENTER).pack()

		Label(frame, text="Enter username").pack()
		self.first_username = Entry(frame)
		self.first_username.pack()
		Label(frame, text="Enter email address").pack()
		self.first_email = Entry(frame)
		self.first_email.pack()
		Label(frame, text="Enter password").pack()
		self.first_pass = Entry(frame, show="*")
		self.first_pass.pack()
		Label(frame, text="Re-enter password").pack()
		self.first_pass2 = Entry(frame, show="*")
		self.first_pass2.pack()
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


	def submitFirstUser(self,*a):
		user = User(self.first_username.get(), self.first_pass.get())
		reEnteredPass = self.first_pass2.get()
		email = self.first_email.get()

		if user.password!=reEnteredPass:
			self.first_notifier.config(text="Passwords don't match.", foreground='red')
			return
		elif user.username=="" or user.password=="" or reEnteredPass=="" or email=="":
			self.first_notifier.config(text="Please fill up all fields.", foreground='red')
			return

		# Save the user into the database
		user.saveUser(email, 1)

		# Move on to login screen
		self.frame.pack_forget()
		self.frame.destroy()
		self.initUI()

	def initUI(self):
		# Notebook
		self.notebook = Notebook(self.parent)
		self.notes={}
		for i in ["Log In", "Create Account", "Change Password"]:
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
		Label(createFrame, text="Enter new account's email address").pack()
		self.create_newMail = Entry(createFrame)
		self.create_newMail.pack()
		## Submit button and text notifier
		self.create_submit = Button(createFrame, text="Register New User", command=self.submitCreateUser)
		self.create_submit.pack()
		self.create_notifier = Label(createFrame)
		self.create_notifier.pack()

		#bind submitCreateUser to return event on last entry
		self.create_newMail.bind("<Return>",self.submitCreateUser)

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

		#bind submitChangePass to last entry
		self.change_newPass2.bind("<Return>",self.submitChangePass)

	# Callbacks
	def submitLogIn(self,*a):
		user = User(self.logIn_username.get(), self.logIn_password.get())
		if not user.auth():
			self.logIn_notifier.config(text='Wrong credentials. Try again.', foreground='red')
		else:
			# Destroy log in screen
			self.notebook.pack_forget()
			self.notebook.destroy()

			# Move on to main program
			self.parent.geometry("800x500")
			mainProgram = MainProgram(self.parent)
			mainProgram.app._activeUser = user

	def submitCreateUser(self,*a):
		admin = User(self.create_adminUser.get(), self.create_adminPass.get())
		newUser = User(self.create_newUser.get(), self.create_newPass.get())
		newUserMail = self.create_newMail.get()
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
		if newUser.username=="" or newUser.password=="" or newUserMail=="" or reEnteredPass=="":
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

		newUser.saveUser(newUserMail)
		self.create_notifier.config(text="New user created.", foreground='darkgreen')

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
		self.change_notifier.config(text="Password successfuly changed.", foreground='darkgreen')


if __name__=="__main__":
	root = Tk()
	app = LogIn(root)
	if os.path.exists(os.path.join("assets","logo.gif")):
		img=PhotoImage(file=os.path.join("assets","logo.gif"))
		root.tk.call("wm","iconphoto",root._w,img)
	app.mainloop()