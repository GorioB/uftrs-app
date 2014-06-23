from Tkinter import *
from ttk import *

class AutocompleteBox(Frame,object):
	def __init__(self,parent,label="Label",text="",**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.parent = parent
		self.label=label
		self._text=text
		self.initUI()

	def initUI(self):
		#frames

		fMain = Frame(self.parent,borderwidth="2px",relief="groove")
		fMain.pack()
		fHigher = Frame(fMain)
		self.fLower = Frame(fMain)
		fHigher.pack(fill=X,expand=0,side=TOP)
		self.fLower.pack(fill=BOTH,expand=1,side=TOP)
		fLeft = Frame(fHigher)
		fRight = Frame(fHigher)
		fRight.pack(fill=NONE,side=RIGHT,expand=0)
		fLeft.pack(side=LEFT,fill=X,expand=1)

		#elements
		label = Label(fLeft,text=self.label)
		label.pack(side=LEFT,fill=BOTH,expand=1)

		button = Button(fRight,text="?",width=2)
		button.pack(fill=NONE,expand=0)

		# self.textField = Text(self.fLower,height=-1)
		# self.textField.pack(fill=BOTH,expand=1)

	def initComboBox(self, identifier):
		# TODO: pull values from th db
		valCombo = ['cat', 'dog', 'pig', 'alberto', 'al', 'alberto lasco']
		self.comboBox = Combobox(self.fLower, values=valCombo, height=-1)
		self.comboBox.pack(fill=BOTH, expand=1)

	@property
	def text(self):
	    return self.comboBox.get()

	@text.setter
	def text(self, value):
		self.comboBox.delete(0, END)
		self.comboBox.insert(0, value)
	
if __name__=="__main__":
	root = Tk()
	app = DataFieldBox(root)
	app.mainloop()