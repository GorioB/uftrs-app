from Tkinter import *
from ttk import *
from tkFont import Font

class TextTable(Frame,object):
	def __init__(self,parent,frames=None,aligns=None,weights=None,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.numberOfRows=0
		self.aligns = aligns
		if not self.aligns:
			self.aligns = ["left","left","left","left","left","left"]
		if not weights:
			weights=[1,1,1,1]
		if frames==None:
			self.frames=["one","two","three","four","five","six"]
		else:
			self.frames=frames
		# for i in range(0,len(self.frames)):
		# 	self.frames[i]=Frame(self)
		# 	self.frames[i].grid(side=LEFT,expand=1,fill=BOTH)

		self.textBoxes=[]
		for i in range(0,len(self.frames)):
			self.textBoxes.append(Text(self,bd=0,width=0,state='disabled'))
			self.textBoxes[-1].grid(row=0,column=i,sticky=W+E+N+S)
			self.textBoxes[-1].tag_configure("right",justify="right",wrap=NONE)
			self.textBoxes[-1].tag_configure("center",justify="center",wrap=NONE)
			self.textBoxes[-1].tag_configure("left",justify="left",wrap=NONE)
			self.textBoxes[-1].tag_configure("underline",underline=True)
			self.grid_columnconfigure(i,weight=weights[i])
		self.grid_rowconfigure(0,weight=1)
		self.boldFont = Font(self.textBoxes[0],self.textBoxes[0].cget('font'))
		self.boldFont.configure(weight='bold')
		for i in self.textBoxes:
			i.tag_configure("bold",font=self.boldFont)


	def fixAligns(self):
		for i in range(0,len(self.textBoxes)):
			self.textBoxes[i]['state']='normal'
			self.textBoxes[i].tag_add(self.aligns[i],'1.0','end')
			self.textBoxes[i]['state']='disabled'

	def addRow(self,values,uls=None,bolds=None):
		self.numberOfRows+=1
		for i in range(0,len(self.textBoxes)):
			self.textBoxes[i]['state']='normal'
			if self.numberOfRows==1:
				self.textBoxes[i].insert(self.textBoxes[i].index("end"),values[i])
			else:
				self.textBoxes[i].insert(self.textBoxes[i].index("end"),"\n"+values[i])
			self.textBoxes[i]['state']='disabled'

		if uls:
			for i in range(0,len(uls)):
				if uls[i]:
					self.textBoxes[i]['state']='normal'
					self.textBoxes[i].tag_add("underline",'end - 1 line','end -1 line lineend')
					self.textBoxes[i]['state']='disabled'
		if bolds:
			for i in range(0,len(bolds)):
				if bolds[i]:
					self.textBoxes[i]['state']='normal'
					self.textBoxes[i].tag_add("bold","end -1 line",'end -1 line lineend')
					self.textBoxes[i]['state']='disabled'
		self.fixAligns()
		for i in self.textBoxes:
			i.configure(height=self.numberOfRows)

	def clear(self):
		for i in self.textBoxes:
			i['state']='normal'
			i.delete("1.0","end")
			i['state']='disabled'
		self.numberOfRows=0

	def getLine(self,index):
		vals = []
		for i in self.textBoxes:
			vals.append(i.get(str(index)+".0",str(index)+".end"))

		return vals

if __name__=="__main__":
	root = Tk()
	root.geometry("600x500")
	app = TextTable(root,aligns=['left','center','center','right','center','right'],weights=[3,1,0,1,0,1])
	app.pack(side=LEFT,expand=1,fill=BOTH)
	app.addRow(['Council Mandated Funds','','','','',''],uls=[1,1,1,1,1,1],bolds=[1,0,1,0,1,0])
	app.addRow(['    Organizational Fees','1','P','15,000','',''],uls=[0,1,0,1,1,1])
	app.mainloop()


