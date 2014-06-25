from lib.app import App
from lib.db2 import User
from interface import textfield
from Tkinter import *
from ttk import *

class LogIn(Frame,object):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.app = App()
		self.pack()
		self.initUI()

	def initUI(self):
		# Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("360x400")
		#self.parent.state("zoomed")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

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

	# Callbacks
	def submitLogIn(self):
		user = User(self.logIn_username.get(), self.logIn_password.get())
		if user.auth():
			self.logIn_notifier.config(text='Log in successful!', foreground='darkgreen')
			# TODO: move on to main program
		else:
			self.logIn_notifier.config(text='Wrong credentials. Try again.', foreground='red')
			# TODO: notify user in gui that credentials are wrong


	def submitCreateUser(self):
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

	def submitChangePass(self):
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
	app.mainloop()