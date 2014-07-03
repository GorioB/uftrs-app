from Tkinter import *
from ttk import *
class CheckButtonBox(Frame,object):
	def __init__(self,parent,*args,**kwargs):
		Frame.__init__(self,parent,*args,**kwargs)
		self._var=StringVar()
		self._var.set("False")
		self.cb = Checkbutton(self,text="Include This Entry in Statement of Cash Flows",variable=self._var,
			offvalue="False",onvalue="True")
		self.cb.pack(fill=X,expand=1)

	@property
	def text(self):
	    return self._var.get()
	@text.setter
	def text(self, value):
		if value=="":
			value="False"
		self._var.set(value)
	
if __name__=="__main__":
	root = Tk()
	app = CheckButtonBox(root)
	app.pack()
	app.text = "True"
	app.mainloop()