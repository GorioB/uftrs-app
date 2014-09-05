from Tkinter import *
from ttk import *	


def createNotification(title, text):
	notification = Toplevel()
	notification.title(title)

	Label(notification, text=text, wraplength=400, justify=CENTER).pack()


	button = Button(notification, text="OK", command=notification.destroy)
	button.pack()
	button.bind("<Return>",lambda *e:notification.destroy())

	button.focus_set()