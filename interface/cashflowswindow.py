from Tkinter import *
from ttk import *
from windows import *
from windows2 import *
from ScrolledFrame import VerticalScrolledFrame
from textfield import *
from lib.timeFuncs import *
from buttonbox import ButtonBox

class CashFlowsWindow(CashDisbursmentsWindow):
	def generateNewButton(self):
		pass

	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		colList = ['one','two','three','four']
		tree['columns']=colList
		for i in colList:
			tree.column(i,anchor=E,width=100,minwidth=100)

		tree.heading('one',text="Notes")
		tree.heading('two',text="Amount")
		tree.heading('three',text="Total")
		tree.column("#0",anchor=W,width=150,minwidth=100)
		tree.insert("","end","inflows",text="Cash Inflows",open=True)
		tree.insert("","end","outflows",text="Cash Outflows",open=True)
		tree.insert("","end","net",text="Net Cashflow",open=True)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y,expand=0)
		xscroll.pack(side=TOP,fill=X,expand=0)
		tree.pack(side=LEFT,fill=BOTH,expand=1)

		#replace with db entry
		self.inflow_categories=inflow_categories=['Council Mandated Funds','General Sponsorship Inflows','Income Generating Projects','Other Inflows']
		for i in inflow_categories:
			tree.insert("inflows",'end',i.lower().replace(" ",""),text=i,open=True)

		#replace with db entry
		self.outflow_categories=outflow_categories=['Council and Other College Projects','Operation and Maintenance Expenses','Long Term Investments','Other Outflows']
		for i in outflow_categories:
			tree.insert("outflows","end",i.lower().replace(" ",""),text=i,open=True)


	def initTotalTag(self):
		pass

	def initSaveDelete(self):
		pass

	def initFields(self):
		self.magicFields = Frame(self.fieldsFrame.interior)
		self.magicFields.pack(fill=X,expand=1)

		self.mFields={}
		self.calendarFrame = Frame(self.magicFields)
		self.calendarFrame.pack(fill=X,expand=1)
		self.mFields['startDate']=CalendarBox(self.calendarFrame,
			label="Start Date")
		self.mFields['endDate']=CalendarBox(self.calendarFrame,label="End Date")
		self.mFields['startDate'].pack(side=LEFT,fill=X,expand=1)
		self.mFields['endDate'].pack(side=RIGHT,fill=X,expand=1)

		self.balanceFrame = Frame(self.magicFields)
		self.balanceFrame.pack(fill=X,expand=1)
		self.mFields['beginningBalance']=ButtonBox(self.balanceFrame,"Beginning Balance",
			"",None)
		self.mFields['endingBalance']=ButtonBox(self.balanceFrame,"Ending Balance","",None)
		self.mFields['beginningBalance'].pack(side=LEFT,fill=X,expand=1)
		self.mFields['endingBalance'].pack(side=LEFT,fill=X,expand=1)



	def newButtonCallback(self):
		pass

	def getSelection(self,event):
		pass

	def _populateTree(self,entrylist):
		pass

	def populateTree(self,*a):
		#clear trees... FOR NOW
		for i in self.inflow_categories:
			cat = i.lower().replace(" ","")
			for item in self.tree.get_children(cat):
				self.tree.delete(item)
		for i in self.outflow_categories:
			cat = i.lower().replace(" ","")
			for item in self.tree.get_children(cat):
				self.tree.delete(item)

		totalInflows=0
		partialTotals={'councilmandatedfunds':0,'generalsponsorshipinflows':0,'incomegeneratingprojects':0,'otherinflows':0}
		showDeleted = self.deletedVar.get()
		cashFlowList = self.app.listCashflows(showDeleted=False)
		inflowList = [i for i in cashFlowList if i.source.content.split(":")[0]=="CashReceipt"]
		for i in inflowList:
			name = i.getContents().nature.content
			amount = i.getContents().amount.content
			notes = i.note.content
			category = i.getContents().category.content.lower().replace(" ","")
			try:
				amount=float(amount)
				totalInflows+=amount
				partialTotals[category]+=amount
			except:
				pass
			self.tree.insert(category,"end",text=name,values=(notes,amount,))

		self.tree.item('inflows',values=("","",totalInflows,""))
		for i in partialTotals:
			self.tree.item(i,values=("","",partialTotals[i],""))
		outflowList = [i for i in cashFlowList if i.source.content.split(":")[0] in ("OME","COCPNote","LTINote","OONote")]
		totalOutflows=0
		partialOutflows={"otheroutflows":0,"operationandmaintenanceexpenses":0,"councilandothercollegeprojects":0,"longterminvestments":0}
		treeParent = {"OONote":"otheroutflows","OME":"operationandmaintenanceexpenses","COCPNote":"councilandothercollegeprojects","LTINote":"longterminvestments"}
		for i in outflowList:
			name=i.getContents().nature.content
			amount = i.getContents().amount.content
			try:
				amount=float(amount)
				totalOutflows+=amount
				partialOutflows[treeParent[i.source.content.split(":")[0]]]+=amount
			except:
				pass
			notes=i.note.content
			self.tree.insert(treeParent[i.source.content.split(":")[0]],"end",text=name,values=(notes,amount,))

		self.tree.item('outflows',values=("","",totalOutflows,""))
		for i in partialOutflows:
			self.tree.item(i,values=("","",partialOutflows[i],""))

		self.tree.item('net',values=("","",totalInflows-totalOutflows,""))
	def exportToExcel(self):
		pass

	def save(self):
		pass

	def delete(self):
		pass
