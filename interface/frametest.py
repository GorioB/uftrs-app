#TKINTER UI TESTS
from Tkinter import *
from ttk import *
class Application(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.pack()
		self.initUI()

	def initUI(self):
		self.parent.title("Test UI")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)
		self.parent.geometry("700x500")

		#menu
		usersMenu=Menu(menubar)
		usersMenu.add_command(label="Create User")
		preferencesMenu = Menu(menubar)
		preferencesMenu.add_command(label="Settings",command=self.hideList)
		menubar.add_cascade(label="User",menu=usersMenu)
		menubar.add_cascade(label="Preferences",menu=preferencesMenu)
		menubar.add_command(label="About")

		#panedwindow
		p = Panedwindow(self.parent,orient=HORIZONTAL)
		lf1 = Labelframe(p,text="Pane1")
		lf2 = Labelframe(p,text="Pane2")
		p.add(lf1,weight=60)
		p.add(lf2,weight=40)
		p.pack(fill=BOTH,expand=1)
		p.pack_propagate(0)
		lf1.pack_propagate(0)
		lf2.pack_propagate(0)

		#notebook
		n = Notebook(lf1)
		f1 = Frame(n)
		f2 = Frame(n)
		n.add(f1,text='One')
		n.add(f2,text='Two')
		n.pack(fill=BOTH,expand=1)
		n.pack_propagate(0)

		#listbox
		self.listFrame = Frame(f1)
		self.listFrameHidden=False
		scrollBar = Scrollbar(self.listFrame,orient=VERTICAL)
		listBox = Listbox(self.listFrame,yscrollcommand=scrollBar.set)
		scrollBar.config(command=listBox.yview)
		scrollBar.pack(side=RIGHT,fill=Y)
		listBox.pack(side=LEFT,fill=BOTH,expand=1)
		self.listFrame.pack(fill=BOTH,expand=1)
		for i in range(0,500):
			listBox.insert(END,i)


	def hideList(self):
		if self.listFrameHidden:
			self.listFrame.pack(fill=BOTH,expand=1)
			self.listFrameHidden=False
		else:
			self.listFrame.pack_forget()
			self.listFrameHidden=True



if __name__=="__main__":
	root = Tk()
	app = Application(parent=root)
	app.mainloop()
