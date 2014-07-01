from Tkinter import *
from ttk import *
from supercombobox import SuperComboBox

class NotesEditBox(Frame,object):
	def __init__(self,parent,elements,existing,addCallback,deleteCallback):
		Frame.__init__(self,parent)
		self.existingLabel = Label(self,text=existing,relief='sunken',anchor="center")
		self.existingLabel.pack(fill=X,expand=1,side=TOP)

		lowerFrame = Frame(self)
		lowerFrame.pack(fill=BOTH,expand=1,side=BOTTOM)


		self.dropDown = SuperComboBox(lowerFrame,values=elements,state='readonly')
		self.dropDown.pack(fill=X,expand=1,side=LEFT)

		self.addButton = Button(lowerFrame,text="Add",command=addCallback)
		self.removeButton = Button(lowerFrame,text="Remove",command=deleteCallback)

		self.addButton.pack(fill=X,expand=1,side=LEFT)
		self.removeButton.pack(fill=X,expand=1,side=LEFT)

	@property
	def labels(self):
		return self.existingLabel['text'].split("Notes: ")[1].strip("")
	@labels.setter
	def labels(self, value):
		self.existingLabel['text']="Notes: "+value

	@property
	def elements(self):
	    return self.dropDown['values']
	@elements.setter
	def elements(self, value):
	    self.dropDown['values']=list(set(value))
	
if __name__=="__main__":
	a = Tk()
	app = NotesEditBox(a,['g','o','r','i','o'],"a,s,d",None,None)
	app.elements=['1','2','3']
	app.pack()
	app.mainloop()
	