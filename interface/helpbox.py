from Tkinter import *
from ttk import *

def createHelpBox(toolTip):
	helpbox = Toplevel()
	helpbox.title("Help")
	msg = Message(helpbox,text=toolTip)

	msg.pack(expand=1,fill=BOTH)

	button = Button(helpbox,text="OK",command=helpbox.destroy)
	button.pack()



if __name__=="__main__":
	print "test"
	createHelpBox("hi")