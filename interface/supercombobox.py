from Tkinter import *
from ttk import *
def startsWithNotEmpty(s,q):
	if q=='':
		return False
	else:
		return s.startswith(q)

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
		print event.char
		closestMatch = [i for i in self['values']+("",) if startsWithNotEmpty(i.lower(),self._buffer.lower())]
		if closestMatch:
			closestMatch.sort()
			print closestMatch
			self._string.set(closestMatch[0])
		else:
			self._buffer=""


	def backspace(self,event):
		self._buffer = self._buffer[:-1]

	def clear(self,event):
		self._buffer=""
		self._string.set("")

	def leaveFocus(self,event):
		self._buffer=""

if __name__=="__main__":
	root = Tk()
	app = SuperComboBox(root,values=['Zinedine','Zidane','Superstar'],state='readonly')
	app.pack()
	button = Button(text="Button")
	button.pack()
	app.focus()
	app.mainloop()