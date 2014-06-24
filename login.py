from lib.app import App
from lib.db2 import User
from interface import windows, textfield
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
		#Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("800x500")
		self.parent.state("zoomed")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		#notebook
		self.notebook = Notebook(self.parent)
		self.notes={}
		for i in ["Log In","Reset Password","Create Account"]:
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
		self.logIn_password = Entry(logInFrame)
		self.logIn_password.pack()
		self.logIn_submit = Button(logInFrame, text="Submit", command=self.submitLogIn)
		self.logIn_submit.pack()

	#callbacks
	def submitLogIn(self):
		print self.logIn_username.get()
		print self.logIn_password.get()
		user = User(self.logIn_username.get(), self.logIn_password.get())
		if user.auth():
			print "Log in successful!"
			# TODO: move on to main program
		else:
			print "Log in failed."
			pass
			# TODO: notify user in gui that credentials are wrong

if __name__=="__main__":
	root = Tk()
	app = LogIn(root)
	app.mainloop()