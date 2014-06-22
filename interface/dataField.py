from Tkinter import *
from ttk import *

class DataFieldBox(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.config(borderwidth=2)
		self.initUI()

	def initUI(self):
		#frames
		fHigher = Frame(self.parent)
		fLower = Frame(self.parent)
		fHigher.pack(fill=X,expand=0,side=TOP)
		fLower.pack(fill=BOTH,expand=1,side=TOP)
		fLeft = Frame(fHigher)
		fRight = Frame(fHigher)
		fRight.pack(fill=NONE,side=RIGHT,expand=0)
		fLeft.pack(side=LEFT,fill=X,expand=1)

		#elements
		label = Label(fLeft,text="Label:")
		label.pack(side=LEFT,fill=BOTH,expand=1)

		button = Button(fRight,text="?",width=2)
		button.pack(fill=NONE,expand=0)

		textField = Entry(fLower)
		textField.pack(fill=BOTH,expand=1)

if __name__=="__main__":
	root = Tk()
	app = DataFieldBox(root)
	app.mainloop()