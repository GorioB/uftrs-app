from Tkinter import *
from ttk import *

class TextTable(Frame,object):
	def __init__(self,parent,aligns=None,weights=None,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.aligns = aligns
		if not self.aligns:
			self.aligns = ["left","left","left","left"]
		if not weights:
			weights=[1,1,1,1]
		self.frames=["one","two","three","four"]
		# for i in range(0,len(self.frames)):
		# 	self.frames[i]=Frame(self)
		# 	self.frames[i].grid(side=LEFT,expand=1,fill=BOTH)

		self.textBoxes=[]
		for i in range(0,len(self.frames)):
			self.textBoxes.append(Text(self,bd=0,width=0,state='disabled'))
			self.textBoxes[-1].grid(row=0,column=i,sticky=W+E+N+S)
			self.textBoxes[-1].tag_configure("right",justify="right")
			self.textBoxes[-1].tag_configure("center",justify="center")
			self.textBoxes[-1].tag_configure("left",justify="left")
			self.grid_columnconfigure(i,weight=weights[i])
		self.grid_rowconfigure(0,weight=1)
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
			i['state']='normal'
			i.delete("1.0","end")
			i['state']='disabled'

	def getLine(self,index):
		vals = []
		for i in self.textBoxes:
			vals.append(i.get(str(index)+".0",str(index)+".end"))

		return vals

if __name__=="__main__":
	root = Tk()
	root.geometry("600x500")
	app = TextTable(root,aligns=['left','center','right','right'],weights=[3,1,1,1])
	app.pack(side=LEFT,expand=1,fill=BOTH)
	app.addRow(['Council Mandated Funds','','',''])
	app.addRow(['    Organizational Fees','1','15,000',''])
	app.mainloop()


