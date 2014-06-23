#TKINTER UI TESTS
from Tkinter import *
from ttk import *
from textfield import TextFieldBox
from autocomplete import AutocompleteBox
from ScrolledFrame import VerticalScrolledFrame
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
		preferencesMenu.add_command(label="Settings")
		menubar.add_cascade(label="User",menu=usersMenu)
		menubar.add_cascade(label="Preferences",menu=preferencesMenu)
		menubar.add_command(label="About",command=self.clickAbout)

		#notebook
		n = Notebook(self.parent)
		f1 = Frame(n)
		f2 = Frame(n)
		n.add(f1,text='One')
		n.add(f2,text='Two')
		n.pack(fill=BOTH,expand=1)
		n.pack_propagate(0)

		#panedwindow
		p = Panedwindow(f1,orient=HORIZONTAL)
		lf1=LabelFrame(p,text="Pane1")
		lf2=VerticalScrolledFrame(p)
		p.add(lf1,weight=60)
		p.add(lf2,weight=40)
		p.pack(fill=BOTH,expand=1)
		p.pack_propagate(0)
		lf1.pack_propagate(0)
		lf2.pack_propagate(0)

		#listbox
		listFrame = Frame(lf1)
		scrollBar = Scrollbar(listFrame,orient=VERTICAL)
		listBox = Listbox(listFrame,yscrollcommand=scrollBar.set)
		scrollBar.config(command=listBox.yview)
		scrollBar.pack(side=RIGHT,fill=Y)
		listBox.pack(side=LEFT,fill=BOTH,expand=1)
		listFrame.pack(fill=BOTH,expand=1)
		for i in range(0,500):
			listBox.insert(END,i)

		#add some datafield boxes
		for i in range(0,7):
			dfb = TextFieldBox(lf2.interior,label=str(i),toolTip="Tooltip "+str(i))
			print dfb.text
			dfb.text=str(i)
			dfb.pack(expand=1,fill=X)

		self.autocomplete = AutocompleteBox(lf2.interior, label="autocomplete")
		self.autocomplete.initComboBox("payors")
		self.autocomplete.text = "autocomplete"
		self.autocomplete.pack(expand=1, fill=X)

		button = Button(lf1, text = 'Press', command = self.clickPress)
		button.pack(pady=20, padx = 20)

	def clickPress(self):
		print self.autocomplete.text
		self.autocomplete.text = "pressed button"

	def clickAbout(self):
		toplevel = Toplevel(height=100,width=200)
		toplevel.title("About")
		msg = Label(toplevel,text="This is a popup message.",anchor="center")
		msg.pack(side=TOP,fill=BOTH,expand=1)
		msg.pack_propagate(0)
		button = Button(toplevel,text="OK",command=toplevel.destroy)
		button.pack(side=TOP)
		button.pack_propagate(0)
		toplevel.pack_propagate(0)


if __name__=="__main__":
	root = Tk()
	app = Application(parent=root)
	app.mainloop()
