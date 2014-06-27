from Tkinter import *
from ttk import *
from windows import *
from windows2 import *
from ScrolledFrame import VerticalScrolledFrame
from textfield import *
from lib.timeFuncs import *
from buttonbox import ButtonBox
from lib.floattostr import *

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
		#change this when db is implemented
		partialTotals={'councilmandatedfunds':{},'generalsponsorshipinflows':{},'incomegeneratingprojects':{},'otherinflows':{}}
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
			except:
				amount=0

			if category in partialTotals:
				totalInflows+=amount
				if name in partialTotals[category]:
					partialTotals[category][name][0]+=amount
				else:
					partialTotals[category][name]=[amount]
					partialTotals[category][name].append(notes)

		for i in partialTotals:
			partialTotalKeys = [key for key in partialTotals[i].keys()]
			partialTotalKeys.sort()
			for j in partialTotalKeys:
				self.tree.insert(i,"end",text=j,values=(partialTotals[i][j][1],floatToStr(partialTotals[i][j][0]),))

		self.tree.item('inflows',values=("","",floatToStr(totalInflows),""))
		for i in partialTotals:
			categoryTotal = reduce(lambda x,y:x+y,[d[0] for d in partialTotals[i].values()]+[0,])
			self.tree.item(i,values=("","",floatToStr(categoryTotal),""))
		outflowList = [i for i in cashFlowList if i.source.content.split(":")[0] in ("OME","COCPNote","LTINote","OONote")]
		totalOutflows=0
		#change for when updated to db-stored variables
		partialOutflows={"otheroutflows":{},"operationandmaintenanceexpenses":{},"councilandothercollegeprojects":{},"longterminvestments":{}}
		treeParent = {"OONote":"otheroutflows","OME":"operationandmaintenanceexpenses","COCPNote":"councilandothercollegeprojects","LTINote":"longterminvestments"}
		for i in outflowList:
			name=i.getContents().nature.content
			amount = i.getContents().amount.content
			notes = i.note.content
			category = i.source.content.split(":")[0]
			print category
			if category=="COCPNote":
				name = i.getContents().event.content
			try:
				amount=float(amount)
			except:
				amount=0

			if category in treeParent:
				category = treeParent[category]
				totalOutflows+=amount
				if name in partialOutflows[category]:
					partialOutflows[category][name][0]+=amount
				else:
					partialOutflows[category][name]=[amount]
					partialOutflows[category][name].append(notes)


		self.tree.item('outflows',values=("","",floatToStr(totalOutflows),""))
		for i in partialOutflows:
			partialOutflowsSorted = [key for key in partialOutflows[i].keys()]
			partialOutflowsSorted.sort()
			for j in partialOutflowsSorted:
				self.tree.insert(i,"end",text=j,values=(partialOutflows[i][j][1],floatToStr(partialOutflows[i][j][0]),))
			categoryTotal = reduce(lambda x,y:x+y,[d[0] for d in partialOutflows[i].values()]+[0,])
			self.tree.item(i,values=("","",floatToStr(categoryTotal),""))
		self.tree.item('net',values=("","",floatToStr(totalInflows-totalOutflows),""))

	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		rowData = []
		for tierAItem in self.tree.get_children():
			# print self.tree.item(tierAItem)
			text = self.tree.item(tierAItem, "text")
			values = self.tree.item(tierAItem, "values")
			newTuple = (text, "", "") + values
			rowData.append(newTuple)
			for tierBItem in self.tree.get_children(tierAItem):
				text = self.tree.item(tierBItem, "text")
				values = self.tree.item(tierBItem, "values")
				newTuple = ("", text, "") + values
				rowData.append(newTuple)
				for tierCItem in self.tree.get_children(tierBItem):
					text = self.tree.item(tierCItem, "text")
					values = self.tree.item(tierCItem, "values")
					newTuple = ("", "", text) + values
					# newTuple = (text,) + values
					rowData.append(newTuple)
		rows = [(i, ("none",)) for i in rowData]

		columnHeaders = ["", "", "", "Notes", "Amount", "Total"]	
		fileName = 'CashFlows_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'

		excelBuilder = ExcelBuilder()
		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setFileName(fileName)
		excelBuilder.setTableColumnWidth(6000)
		excelBuilder.setSheetName("Cash Flows")
		excelBuilder.buildSheet()
		excelBuilder.sheet.col(0).width = 4000
		excelBuilder.sheet.col(1).width = 4000
		excelBuilder.sheet.col(3).width = 2500
		excelBuilder.sheet.col(4).width = 2500
		excelBuilder.sheet.col(5).width = 2500

		excelBuilder.build()

	def save(self):
		pass

	def delete(self):
		pass
