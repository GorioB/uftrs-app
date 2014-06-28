from Tkinter import *
from ttk import *
from helpbox import createHelpBox
from supercombobox import *

class AutocompleteBox(Frame,object):
	def __init__(self,parent,label="Label",toolTip=None,text="",**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.parent = parent
		self.label=label
		self._text=text
		self.toolTip=toolTip
		self.initUI()

	def initUI(self):
		#styles
		s = Style()
		s.configure("ToolTip.TLabel",background="yellow")

		#frames

		fMain = Frame(self.parent,borderwidth="2px",relief="groove")
		fMain.pack(fill=X,expand=1)
		fHigher = Frame(fMain)
		self.fLower = Frame(fMain)
		fHigher.pack(fill=X,expand=1,side=TOP)
		self.fLower.pack(fill=BOTH,expand=1,side=TOP)
		fHighHigh=Frame(fHigher)
		self.fHighLow=fHighLow=Frame(fHigher)
		fHighHigh.pack(fill=X,expand=1,side=TOP)
		fLeft = Frame(fHighHigh)
		fRight = Frame(fHighHigh)
		fRight.pack(fill=NONE,side=RIGHT,expand=0)
		fLeft.pack(side=LEFT,fill=X,expand=1)

		#elements
		label = Label(fLeft,text=self.label)
		label.pack(side=LEFT,fill=BOTH,expand=1)

		

		#tooltip
		if self.toolTip:
			if len(self.toolTip)<100:
				self.shortToolTip=self.toolTip
			else:
				self.shortToolTip="Click ? for help."
			button = Button(fRight,text="?",width=2,command=self.createHelpBox,takefocus=0)
			button.pack(fill=NONE,expand=0)
			button.bind("<Enter>",self.hoverHelp)
			button.bind("<Leave>",self.leaveHelp)
			self.tooltipLabel = Label(fHighLow,text=self.shortToolTip,style="ToolTip.TLabel")
			self.tooltipLabel.pack(fill=X,expand=1)


		# self.textField = Text(self.fLower,height=-1)
		# self.textField.pack(fill=BOTH,expand=1)
	def createHelpBox(self):
		createHelpBox(self.toolTip)

	def initComboBox(self, options=["cat", "dog", "pig"]):
		self.comboBox = Combobox(self.fLower, values=options, height=-1)
		self.comboBox.pack(fill=BOTH, expand=1)

	def initDropDown(self, options=["cat", "dog", "pig"]):
		self.comboBox = SuperComboBox(self.fLower, values=options, height=-1,state="readonly")
		self.comboBox.pack(fill=BOTH, expand=1)


	@property
	def text(self):
	    return self.comboBox.get()

	@text.setter
	def text(self, value):
		self.comboBox.set(value)

	#MouseOver bindings
	def hoverHelp(self,event):
		self.fHighLow.pack(fill=X,expand=1,side=TOP)

	def leaveHelp(self,event):
		self.fHighLow.pack_forget()

	def bind(self,event,cb):
		self.comboBox.bind(event,cb)
	
if __name__=="__main__":
	root = Tk()
	app = DataFieldBox(root)
	app.mainloop()