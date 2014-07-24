from Tkinter import *
from ttk import *
from tkFont import *
from notePreviewLines import *
from textable import *

class NoteChunk(Frame,object):
	def __init__(self,parent,app):
		Frame.__init__(self,parent)
		self.app = app
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.mainFrame = Frame(self)
		self.mainFrame.pack(fill=BOTH,expand=1,side=TOP)
		self.blocks=[]

	def update(self):
		for i in self.blocks:
			i.pack_forget()
			i.destroy()
		self.blocks=[]
		noteBlocks = getNotePreviewLines(self.app.getStatementNotes())
		if noteBlocks:
			headBlock = Text(self.mainFrame,bd=0,width=0,height=2)
			f = Font(headBlock,headBlock.cget("font"))
			f.configure(weight="bold")
			headBlock.configure(font=f)
			headBlock.insert('1.0',"Notes to Financial Statement\n")
			self.blocks.append(headBlock)
		for i in noteBlocks:
			if i.blockType=="text":
				newBlock = Text(self.mainFrame,bd=0,width=0,height=0)
				f = Font(newBlock,newBlock.cget("font"))
				f.configure(weight='bold')
				newBlock.tag_configure("b",font=f)
				newBlock.insert('1.0',i.payload[0]+'\n')
				newBlock.tag_add("b",'1.0','end -1 line lineend')
				newBlock.insert(newBlock.index("end"),i.payload[1])
				newBlock.configure(height=int(newBlock.index("end-1c").split(".")[0]))
				self.blocks.append(newBlock)
				newBlock.state='disabled'
			else:
				newBlock = TextTable(self.mainFrame,
					frames=["one","two","three","four","five"],
					aligns=['left','center','right','center','right'],
					weights=[10,0,1,0,1])
				self.setUL(i.payload)
				for line in i.payload:
					newBlock.addRow(line[0],uls=line[1],bolds=line[2])
				self.blocks.append(newBlock)

		for i in self.blocks:
			i.pack(fill=BOTH,expand=1,side=TOP)

	def setUL(self,lines):
		hasp=0
		for i in range(0,len(lines)):
			if lines[i][0][0]==tab(2)+"Total Inflows":
				lines[i-1][1]=[0,0,1,0,0]
			elif lines[i][0][0]==tab(2)+"Total Outflows":
				lines[i-1][1]=[0,0,1,0,0]
			elif lines[i][0][0]=="Net Cash Flow":
				lines[i-1][1]=[0,0,0,0,1]
			elif lines[i][0][0]=="Outflows":
				lines[i-1][1]=[0,0,1,0,0]
			if not hasp and lines[i][0][0].startswith(tab(1)) and not lines[i][0][0].startswith(tab(2)):
				hasp=1
				lines[i][0][1]="P"