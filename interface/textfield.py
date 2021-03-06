from Tkinter import *
from ttk import *
from helpbox import createHelpBox
from lib.floattostr import *
class TextFieldBox(Frame,object):
	def __init__(self,parent,label="Label",toolTip=None,readonly=False,text="",height=3,textType="text",**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.parent = parent
		#self.config(borderwidth=2,relief="groove")
		self.label=label
		self._text=text
		self.toolTip=toolTip
		self.readonly=readonly
		self.height=height
		self.textType=textType

		#STYLE
		self.initUI()

	def initUI(self):
		#styles
		s = Style()
		s.configure("ToolTip.TLabel",background="yellow")

		#frames
		fMain = Frame(self.parent,borderwidth="2px",relief="groove")
		fMain.pack(fill=X,expand=1)
		fHigher = Frame(fMain)
		fLower = Frame(fMain)
		fHigher.pack(fill=X,expand=0,side=TOP)
		fLower.pack(fill=BOTH,expand=1,side=TOP)
		fHighHigh = Frame(fHigher)
		self.fHighLow=fHighLow =Frame(fHigher)
		fHighHigh.pack(fill=X,expand=1,side=TOP)
		#fHighLow.pack(fill=BOTH,expand=1,side=TOP)
		fLeft = Frame(fHighHigh)
		fRight = Frame(fHighHigh)
		fRight.pack(fill=NONE,side=RIGHT,expand=0)
		fLeft.pack(side=LEFT,fill=X,expand=1)

		#elements
		label = Label(fLeft,text=self.label)
		label.pack(side=LEFT,fill=BOTH,expand=1)
			

		self.textField = Text(fLower,height=self.height)
		self.textField.pack(fill=BOTH,expand=1)
		self.textField.bind("<Tab>",self.focusNext)
		if self.readonly:
			self.textField.configure(state='disabled')
			self.textField.configure(background='grey')

		#tooltip
		if self.toolTip:
			if len(self.toolTip)<100:
				self.shortToolTip=self.toolTip
				button=Button(fRight,text="?",width=2,takefocus=0)
			else:
				self.shortToolTip="Click ? for help."
				button = Button(fRight,text="?",width=2,command=self.createHelpBox,takefocus=0)
			button.pack(fill=NONE,expand=0)
			button.bind("<Enter>",self.hoverHelp)
			button.bind("<Leave>",self.leaveHelp)
			self.tooltipLabel = Label(fHighLow,text=self.shortToolTip,style="ToolTip.TLabel")
			self.tooltipLabel.pack(fill=X,expand=1)

	def createHelpBox(self):
		createHelpBox(self.toolTip)

	def bind(self,event,callback):
		def cb(*a):
			callback()
			return "break"
		self.textField.bind(event,cb)


	@property
	def text(self):
		value = self.textField.get('1.0','end').strip('\n')

		if self.textType=="number":
			try:
				value=strToFloat(value)
				return strToFloat(self.textField.get('1.0','end').strip("\n"))
			except:
				return 0
		return self.textField.get('1.0','end').strip('\n')

	@text.setter
	def text(self, value):
		self.textField.configure(state='normal')
		self.textField.delete('1.0',END)
		self.textField.insert('1.0',value)
		if self.readonly:
			self.textField.configure(state='disabled')

	def focusNext(self,event):
		event.widget.tk_focusNext().focus()
		return ("break")

	def hoverHelp(self,event):
		self.fHighLow.pack(fill=X,expand=1,side=TOP)
		#self.tooltipLabel.pack(fill=X,expand=1)

	def leaveHelp(self,event):
		self.fHighLow.pack_forget()
		#self.tooltipLabel.pack_forget()

	
if __name__=="__main__":
	root = Tk()
	app = TextFieldBox(root,toolTip="This is a sample tooltip\nTest")
	app.mainloop()