from Tkinter import *
from ttk import *
from tkFont import Font

class StatementWindow(Frame,object):
	def __init__(self,parent,app,deletedVar,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.initUI()

	def initUI(self):
		self.headerField = Text(self,bd=0,width=0,state='disabled',height=3)
		self.headerField.tag_configure("center",justify="center")
		f = Font(self.headerField,self.headerField.cget('font'))
		f.configure(weight='bold')
		self.headerField.configure(font=f)
		self.headerField.pack(fill=X,expand=1)

	def populateTree(self):
		self.headerField['state']='normal'
		self.headerField.insert('1.0',"UP School of Dinosaurs Student Council\nStatement of Cash Flows\nFor the Semester Ended Octber 31,2013")
		self.headerField.tag_add('center','1.0','end')
		self.headerField['state']='disabled'
		pass

if __name__=="__main__":
	root = Tk()
	app = StatementWindow(root,None,None)
	app.pack(fill=BOTH,expand=1)
	app.populateTree()
	app.mainloop()