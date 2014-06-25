from Tkinter import *
from ttk import *

class ButtonBox(Frame,object):
	def __init__(self,parent,label,initialValue,callBack):
		self.parent=parent
		Frame.__init__(self,parent)

		self.configure(relief="groove",borderwidth="2px")

		labelWidget = Label(self,text=label)
		buttonWidget = Button(self,text=initialValue,command=callBack)

		labelWidget.pack(fill=X,expand=1,side=TOP)
		buttonWidget.pack(fill=X,expand=1,side=TOP)
		