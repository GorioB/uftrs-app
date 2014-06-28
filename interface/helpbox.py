from Tkinter import *
from ttk import *
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def createHelpBox(toolTip):
	helpbox = Toplevel()
	helpbox.title("Help")
	msg = Message(helpbox,text=toolTip,aspect=200)

	msg.pack(expand=1,fill=BOTH)

	button = Button(helpbox,text="OK",command=helpbox.destroy)
	button.pack()
	button.bind("<Return>",lambda *e:helpbox.destroy())

	button.focus_set()
	center(helpbox)

if __name__=="__main__":
	print "test"
	createHelpBox("hi")