from Tkinter import *
from ttk import *
from windows import CashDisbursmentsWindow
from lib import notespreview

class PreviewPage(CashDisbursmentsWindow):
	def generateNewButton(self):
		pass

	def initTree(self):
		self.nprev = notespreview.gatherNotes(self.app)
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		yscroll = Scrollbar(self.treeFrame,orient="vertical",
			command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient='horizontal',
			command=tree.xview)
		self.colList = colList = ["one","two","three","four","five","six"]
		tree['columns']=colList
		for i in colList:
			tree.column(i,anchor=E,width=100,minwidth=100)

		tree.column("#0",anchor=W,width=150,minwidth=100)
		yscroll.pack(side=RIGHT,fill=Y,expand=0)
		xscroll.pack(fill=X,expand=0,side=TOP)
		self.tree.pack(side=LEFT,fill=BOTH,expand=1)


		

	def _populateTree(self):
		pass
	def initTotalTag(self):
		pass
	def initSaveDelete(self):
		pass
	def initFields(self):
		pass
	def newButtonCallback(self):
		pass
	def getSelection(self,event):
		pass
	def exportToExcel(self):
		pass
	def addSheet(self,excelBuilder):
		pass
	def save(self,*a):
		pass
	def delete(self,*a):
		pass
	def populateTree(self):
		for i in self.tree.get_children():
			self.tree.delete(i)
		nprev = notespreview.gatherNotes(self.app)
		for i in nprev.keys():

			self.tree.insert("","end",i,text=i,open=True)
			if i not in ("Long Term Investment","Other Descriptive Notes","Other Outflows"):
				self.tree.insert(i,"end","Inflows"+i,text="Inflows",open=True)
				self.tree.insert(i,"end","Outflows"+i,text="Outflows",open=True)
				self.tree.insert(i,"end","Net Cash Flow"+i,text="Net Cash Flow",open=True)
				for j in nprev[i]['Inflows']:
					self.tree.insert("Inflows"+i,"end",j+i,text=j,values=['',nprev[i]["Inflows"][j],'','','',''])
				for j in nprev[i]['Outflows']:
					self.tree.insert("Outflows"+i,"end",j+i,text=j,values=['',nprev[i]['Outflows'][j],'','','',''])

