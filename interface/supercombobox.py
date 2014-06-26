from Tkinter import *
from ttk import *

class SuperComboBox(Combobox,object):
	def __init__(self,parent,*args,**kwargs):
		self._string = StringVar()
		Combobox.__init__(self,parent,textvariable=self._string,*args,**kwargs)

		self._buffer =""
		self.bind("<Key>",self.key)
		self.bind("<BackSpace>",self.backspace)
		self.bind("<FocusOut>",self.leaveFocus)
		self.bind("<Escape>",self.clear)

	def key(self,event):
		self._buffer=self._buffer+event.char
		closestMatch = [i for i in self['values'] if i.lower().startswith(self._buffer.lower())]
		if closestMatch:
			self._string.set(closestMatch[0])

	def backspace(self,event):
		self._buffer = self._buffer[:-1]

	def clear(self,event):
		self._buffer=""
		self._string.set("")

	def leaveFocus(self,event):
		self.clear(None)

if __name__=="__main__":
	root = Tk()
	app = SuperComboBox(root,values=['Zinedine','Zidane','Superstar'],state="readonly")
	app.pack()
	app.focus()
	app.mainloop()