from lib.app import App
from interface import *
from Tkinter import *
from ttk import *

class MainProgram(Frame,object):
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
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		#menu
		usersMenu=Menu(menubar)
		usersMenu.add_command(label="Create User")
		preferencesMenu=Menu(menubar)
		preferencesMenu.add_command(label="Settings")
		menubar.add_cascade(label="User",menu=usersMenu)
		menubar.add_cascade(label="Preferences",menu=preferencesMenu)
		menubar.add_command(label="About",command=self.about)

		#notebook
		self.notebook = Notebook(self.parent)
		self.notes={}
		for i in ["Cash Receipts","Cash Disbursments","Cash Flows",
			"Other Assets and Liabilities","Notes",
			"Operation and Maintenance Expense","Statement of Cash Flows"]:
			self.notes[i]=Frame(self.notebook)
			self.notebook.add(self.notes[i],text=i)
		self.notebook.pack(fill=BOTH,expand=1)
		self.notebook.pack_propagate(0)

	#callbacks
	def about(self):
		pass

if __name__=="__main__":
	root = Tk()
	app = MainProgram(root)
	app.mainloop()