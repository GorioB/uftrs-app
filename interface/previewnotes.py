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

		allNotes = self.app.listNotes()
		treeDict={}
		for i in allNotes:
			if i.identifier=="COCPNote":
				event = i.event.content
				flowDirection = i.flowDirection.content
				nature = i.nature.content
				amount = i.amount.content
				nn = i.noteNumber.content

				if event not in treeDict:
					treeDict[event]={}
				if flowDirection not in treeDict:
					treeDict[event][flowDirection]={}
				treeDict[event][flowDirection][nature]=[nn,amount]

			elif i.identifier=="LTINote":
				purpose = i.purpose.content
				nn = i.noteNumber.content

				if "Long Term Investment" not in treeDict:
					treeDict['Long Term Investment']=[]
				treeDict['Long Term Investment'].append([nn,purpose])

			elif i.identifier=="OONote":
				purpose = i.purpose.content
				nn= i.noteNumber.content

				if "Other Outflows" not in treeDict:
					treeDict['Other Outflows']=[]
				treeDict['Other Outflows'].append([nn,purpose])

			else:
				description = i.description.content
				nn= i.noteNumber.content

				if "Other Descriptive Notes" not in treeDict:
					treeDict['Other Descriptive Notes']=[]
				treeDict['Other Descriptive Notes'].append([nn,description])

		for i in treeDict.keys():
			self.tree.insert("","end",i,text='',values=[i,'','','','',''])
			if i not in ("Long Term Investment","Other Outflows","Other Descriptive Notes"):
				for j in treeDict[i].keys():
					self.tree.insert(i,"end",j+i,text="",values=[j,'','','','',''])
					for k in treeDict[i][j].keys():
						self.tree.insert(j+i,"end",text=treeDict[i][j][k][0],values=[k,'',treeDict[i][j][k][1],'','',''])

			else:
				pass
		# for i in self.tree.get_children():
		# 	self.tree.delete(i)
		# nprev = notespreview.gatherNotes(self.app)
		# for i in nprev.keys():
		# 	self.tree.insert("","end",i,text=i,open=True)
		# 	if i not in ("Long Term Investment","Other Descriptive Notes","Other Outflows"):
		# 		netFlows = 0
		# 		if nprev[i]['Inflows'].keys():
		# 			self.tree.insert(i,"end","Inflows"+i,text="Inflows",open=True)
		# 			for j in sorted(nprev[i]['Inflows'].keys(),key=lambda word:word[0]):
		# 				self.tree.insert("Inflows"+i,"end",j+i,text=j,values=['',nprev[i]["Inflows"][j],'','','',''])
		# 				netFlows+=int(nprev[i]['Inflows'][j])
		# 		if nprev[i]['Outflows'].keys():
		# 			self.tree.insert(i,"end","Outflows"+i,text="Outflows",open=True)
		# 			for j in sorted(nprev[i]['Outflows'].keys(),key=lambda word:word[0]):
		# 				self.tree.insert("Outflows"+i,"end",j+i,text=j,values=['',nprev[i]['Outflows'][j],'','','',''])
		# 				netFlows-=int(nprev[i]['Outflows'][j])

		# 		self.tree.insert(i,"end","Net Cash Flow"+i,text="Net Cash Flow",values=['','','',str(netFlows),'',''])