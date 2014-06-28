from Tkinter import *
from ttk import *

class TextTable(Frame,object):
	def __init__(self,parent,aligns=None,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.aligns = aligns
		if not self.aligns:
			self.aligns = ["left","left","left","left"]
		self.frames=["one","two","three","four"]
		for i in range(0,len(self.frames)):
			self.frames[i]=Frame(self)
			self.frames[i].pack(side=LEFT,expand=1,fill=BOTH)

		self.textBoxes=[]
		for i in self.frames:
			self.textBoxes.append(Text(i,bd=0,width=0,state='disabled'))
			self.textBoxes[-1].pack(side=LEFT,expand=1,fill=BOTH)
			self.textBoxes[-1].tag_configure("right",justify="right")
			self.textBoxes[-1].tag_configure("center",justify="center")
			self.textBoxes[-1].tag_configure("left",justify="left")

	def fixAligns(self):
		for i in range(0,len(self.textBoxes)):
			self.textBoxes[i]['state']='normal'
			self.textBoxes[i].tag_add(self.aligns[i],'1.0','end')
			self.textBoxes[i]['state']='disabled'

	def addRow(self,values):
		for i in range(0,len(self.textBoxes)):
			self.textBoxes[i]['state']='normal'
			self.textBoxes[i].insert(self.textBoxes[i].index("end"),values[i]+"\n")
			self.textBoxes[i]['state']='disabled'

		self.fixAligns()

	def clear(self):
		for i in self.textBoxes:
			i.delete("1.0","end")

	def getLine(self,index):
		vals = []
		for i in self.textBoxes:
			vals.append(i.get(str(index)+".0",str(index)+".end"))

		return vals

if __name__=="__main__":
	root = Tk()
	root.geometry("600x500")
	app = TextTable(root,aligns=['left','center','right','right'])
	app.pack(side=LEFT,expand=1,fill=BOTH)
	app.addRow(['Council Mandated Funds','','',''])
	app.addRow(['    Organizational Fees','1','15,000',''])
	app.mainloop()


