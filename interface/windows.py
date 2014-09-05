from Tkinter import *
from ttk import *
from ScrolledFrame import VerticalScrolledFrame
from interface.textfield import *
from interface.datefield import *
from interface.autocomplete import *
from interface.helpbox import *
from lib.timeFuncs import *
import sys
try:
	from xlwt import Workbook, easyxf
except:
	print "Requires xlwt"
	sys.exit(1)
import datetime
import shutil #for moving files
import os
from lib.floattostr import *
def checkFields(fields):
	keys = fields.keys()
	if 'notes' in keys:
		keys.remove("notes")
	if 'remarks' in keys:
		keys.remove('remarks')
	if 'timestamp' in keys:
		keys.remove('timestamp')
	for i in keys:
		if fields[i].text=="":
			createHelpBox("Please fill all fields (Notes and Remarks optional).")
			return 1
def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	if col=="Amount":
		l = sorted(l,reverse=reverse,key=lambda n: \
			strToFloat(n[0]))
	else:
		l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
		treeview_sort_column(tv, col, not reverse))
def newExistsInTree(tree):
	return [i for i in tree.get_children() if tree.item(i,"text")=="New"]

class CashReceiptsWindow(Frame,object):
	def __init__(self,parent,app,deletedVar=None):
		Frame.__init__(self,parent)
		self.selectedpk="New"
		self.parent=parent
		self.app=app
		if deletedVar:
			self.deletedVar = deletedVar
		else:
			self.deletedVar=BooleanVar()
			self.deletedVar.set(0)

		self.deletedVar.trace("w",self.populateTree)

		#STYLE
		s = Style()
		s.configure("NEWButton.TButton",background="green")
		s.configure("SAVEButton.TButton",background="blue")
		self.initUI()

	def initUI(self):
		p = Panedwindow(self.parent,orient=HORIZONTAL)
		leftFrame = LabelFrame(p)
		rightFrame = LabelFrame(p)
		p.add(leftFrame,weight=60)
		p.add(rightFrame,weight=40)
		p.pack(fill=BOTH,expand=1)
		p.pack_propagate(0)
		leftFrame.pack_propagate(0)
		rightFrame.pack_propagate(0)



		#leftFrame elements
		leftFrameUpperest = Frame(leftFrame)
		leftFrameUpper = Frame(leftFrame)
		leftFrameLower = Frame(leftFrame)
		leftFrameLower.pack(expand=0,fill=X,side=BOTTOM)
		leftFrameUpperest.pack(expand=0,fill=X,side=TOP)
		leftFrameUpper.pack(expand=1,fill=BOTH,side=BOTTOM)

		newButton = Button(leftFrameUpperest,text="New",command=self.newEntry,style="NEWButton.TButton")
		newButton.pack(fill=None,expand=0,side=LEFT)
		self.tree = tree = Treeview(leftFrameUpper,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(leftFrameUpper,orient="vertical",command=tree.yview)
		xscroll=Scrollbar(leftFrameLower,orient="horizontal",command=tree.xview)
		colList = ["Timestamp","Date of Transaction","Category","Nature","Amount","Payor's Name","Acknowledgement Receipt #","Notes","Remarks"]
		tree['columns']= colList
		for col in colList:
			tree.heading(col,text=col,command=lambda _col=col: \
				treeview_sort_column(tree,_col,False))
			tree.column(col,anchor=W,width=60)
		tree.column('#0',width=3,anchor=W)
		if "Amount" in colList:
			tree.column("Amount",anchor=E)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y)
		xscroll.pack(side=TOP,fill=X)
		tree.pack(side=LEFT,fill=BOTH,expand=1)
		tree.tag_configure("deleted",foreground="red")

		#bottombar
		leftLowestFrame = Frame(leftFrameLower)
		leftLowestFrame.pack(fill=X,expand=0)

		self.totalLabel=totalLabel=Label(leftLowestFrame,text="Total Cash Receipts: ",relief=SUNKEN,width=50)
		totalLabel.pack(fill=None,expand=0,side=RIGHT)

		#populateTree
		#testing. Remove later for actual data
		self.fieldList = ['timestamp','dateOfTransaction','category','nature','amount','payor','receiptNumber','notes','remarks']
		self.populateTree()

		#rightFrame
		upperRight = VerticalScrolledFrame(rightFrame)
		lowerRight = Frame(rightFrame)
		lowerRight.pack(fill=X,expand=0,side=BOTTOM)
		upperRight.pack(fill=BOTH,expand=1,side=TOP)

		saveButton = Button(lowerRight,text="Save",command=self.save,style="SAVEButton.TButton")
		saveButton.pack(side=LEFT,fill=X,expand=1)
		deleteButton = Button(lowerRight,text="Delete",command=self.delete)
		deleteButton.pack(side=LEFT,fill=X,expand=1)

		#fields
		self.fields={}
		self.fields['timestamp'] = timestamp = TextFieldBox(upperRight.interior,label="Timestamp",readonly=True,height=1)

		self.fields['dateOfTransaction']=dot = CalendarBox(upperRight.interior,label="Date of Transaction")
		dot.pack(side=TOP,fill=X,expand=1)
		#options for removal, get from DB
		options = ["Council Mandated Funds","General Sponsorship Inflows","Income Generating Projects","Other Inflows","Excess"]
		self.fields['category'] = category = AutocompleteBox(upperRight.interior,label="Category",toolTip="[Council Mandated Funds]: All fees, commissions and revenues that the council body is authorized to collect among students and all businesses within the college\n[General Sponsorhip Inflows]: Cash inflows acquired gratuitously from business organizations, studentry/alumni body and other entities\n[Income Generating Projects]: Cash inflows from all council events to raise revenues and generate additional funds supplementary to its operations\n[Other Inflows]: Cash inflows other than council mandated funds, general sponsoships and income generating projects")
		category.initDropDown(options)

		self.fields['nature']=nature = AutocompleteBox(upperRight.interior,label="Nature",toolTip=None)
		nature.initComboBox(self.app.listOptions("Nature"))

		self.fields['amount'] = TextFieldBox(upperRight.interior,label="Amount",readonly=False,height=1,textType="number")

		self.fields['payor'] = AutocompleteBox(upperRight.interior,label="Payor's Name",toolTip = "Name of the individual who actually gave the cash.")
		self.fields['payor'].initComboBox(self.app.listOptions("CR_Payor"))

		self.fields['receiptNumber'] = TextFieldBox(upperRight.interior,label="Acknowledgement Receipt #",readonly=False)

		self.fields['notes'] = TextFieldBox(upperRight.interior,label="Notes",toolTip = "Any additional notes about the transaction.")

		self.fields['remarks'] = TextFieldBox(upperRight.interior,label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
			self.fields[i].pack(side=TOP,fill=X,expand=1)

	def getSelection(self,event):
		item = self.tree.selection()[0]
		values = self.tree.item(item,"values")

		for i in range(0,len(self.fieldList)):
			self.fields[self.fieldList[i]].text=values[i]

		if self.fields['dateOfTransaction'].text=="":
			self.fields['dateOfTransaction'].text=secsToDay(getEpochTime())
		self.selectedpk=self.tree.item(item,"text")

	def populateTree(self,*a):
		showDeleted = self.deletedVar.get()
		entryList = self.app.listCashReceipts(showDeleted=showDeleted)
		total = 0
		[self.tree.delete(item) for item in self.tree.get_children()]
		for i in entryList:
			dataFields=[]
			pk = i.pk.content
			try:
				amt = float(i.amount.content)
			except:
				amt =0
			if i.status.content!="DELETED":
				total+=amt
			for j in self.fieldList:
				dataFields.append(vars(i)[j].content)
			dataFields[0]=secsToString(dataFields[0])
			dataFields[1]=secsToDay(dataFields[1])
			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))
		self.totalLabel.config(text="Total Cash Receipts: "+floatToStr(total))
		self.total = total


	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		excelBuilder = ExcelBuilder()
		self.addSheet(excelBuilder)
		excelBuilder.build()

	def addSheet(self, excelBuilder):
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = ["Timestamp","Date of Transaction","Category","Nature","Amount","Payor's Name","Acknowledgement Receipt #","Notes","Remarks"]
		fileName = 'CashReceipt_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setFileName(fileName)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Cash Receipts")
		excelBuilder.buildSheet()


	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk = self.app.editCashReceipt(self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				category = self.fields['category'].text,
				nature = self.fields['nature'].text,
				amount = (self.fields['amount'].text),
				payor = self.fields['payor'].text,
				receiptNumber = self.fields['receiptNumber'].text,
				notes = self.fields['notes'].text)
		else:
			self.selectedpk=self.app.newCashReceipt(
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				category=self.fields['category'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				payor=self.fields['payor'].text,
				receiptNumber = self.fields['receiptNumber'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		#combobox stuff
		self.app.addOption("Nature", self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values = self.app.listOptions("Nature"))
		self.app.addOption("CR_Payor",self.fields['payor'].text)
		self.fields['payor'].comboBox.config(values=self.app.listOptions("CR_Payor"))
		self.newEntry()

	def newEntry(self):
		#create blank entry for demonstration purposes
		dummyEntry = newExistsInTree(self.tree)
		if not dummyEntry:
			dummyEntry = self.tree.insert("","end",text='New',values=('','','','','','','','',''))
		else:
			dummyEntry = dummyEntry[0]
		self.tree.selection_set(dummyEntry)
		self.selectedpk="New"

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteCashReceipt(self.selectedpk)
		self.populateTree()

#Refer to CashDisbursmentsWinow for creating pages. Override nonportable functions
class CashDisbursmentsWindow(Frame,object):
	def __init__(self,parent,app,deletedVar):
		Frame.__init__(self,parent)
		self.selectedpk="New"
		self.parent=parent
		self.app=app
		self.deletedVar=deletedVar
		self.deletedVar.trace("w",self.populateTree)

		s = Style()
		s.configure("NEWBUTTON.TButton",background="green")
		s.configure("SAVEButton.TButton",background="blue")
		self.initUI()
		self.initTree()
		self.initTotalTag()
		self.initSaveDelete()
		self.initFields()
		self.populateTree()

	def initUI(self):
		#portable
		p = Panedwindow(self.parent,orient=HORIZONTAL)
		leftFrame = LabelFrame(p)
		rightFrame = LabelFrame(p)
		p.add(leftFrame,weight=60)
		p.add(rightFrame,weight=40)
		p.pack(fill=BOTH,expand=1)
		p.pack_propagate(0)
		leftFrame.pack_propagate(0)
		rightFrame.pack_propagate(0)

		self.saveFrame = saveFrame = Frame(leftFrame)
		self.treeFrame = treeFrame = Frame(leftFrame)
		self.xScrollFrame = xScrollFrame = Frame(leftFrame)
		self.totalFrame = totalFrame = Frame(leftFrame)
		saveFrame.pack(expand=0,fill=X,side=TOP)
		totalFrame.pack(expand=0,fill=X,side=BOTTOM)
		xScrollFrame.pack(expand=0,fill=X,side=BOTTOM)
		treeFrame.pack(expand=1,fill=BOTH,side=TOP)

		self.saveDeleteFrame = Frame(rightFrame)
		self.fieldsFrame = VerticalScrolledFrame(rightFrame)
		self.saveDeleteFrame.pack(expand=0,fill=X,side=BOTTOM)
		self.fieldsFrame.pack(expand=1,fill=BOTH,side=TOP)

		self.generateNewButton()

	def generateNewButton(self):
		newButton=Button(self.saveFrame,text="New",style="NEWButton.TButton",command=self.newButtonCallback)
		newButton.pack(expand=0,fill=None,side=LEFT)

	def initTree(self):
		#nonportable
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList = ["Timestamp","Date of Transaction","Category","Event",
			"Purpose","Nature","Amount","Liquidating Person/Payee","Document #","Notes","Remarks"]
		tree['columns']=colList
		for i in colList:
			tree.heading(i,text=i,command=lambda _i=i:treeview_sort_column(tree,_i,False))
			tree.column(i,anchor=W,width=60)
		tree.column("#0",width=3,anchor=W)
		if "Amount" in colList:
			tree.column("Amount",anchor=E)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y,expand=0)
		xscroll.pack(side=TOP,fill=X,expand=0)
		tree.pack(side=LEFT,fill=BOTH,expand=1)
		tree.tag_configure("deleted",foreground="red")

	def initTotalTag(self):
		#portable,optional
		self.totalLabel = totalLabel = Label(self.totalFrame,text="Total Cash Disbursements: ",relief=SUNKEN,width=50)
		totalLabel.pack(fill=None,expand=0,side=RIGHT)

	def initSaveDelete(self):
		#portable
		saveButton=Button(self.saveDeleteFrame,text="Save",command=self.save,
			style="SAVEButton.TButton")
		saveButton.pack(side=LEFT,fill=X,expand=1)
		deleteButton=Button(self.saveDeleteFrame,text="Delete",command=self.delete)
		deleteButton.pack(side=LEFT,fill=X,expand=1)

	def initFields(self):
		#nonportable
		self.fields={}
		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)
		self.fields['dateOfTransaction']=CalendarBox(self.fieldsFrame.interior,
			label="Date of Transaction")
		self.fields['dateOfTransaction'].pack(side=TOP,fill=X,expand=1)
		#patchin get from DB here
		options=['Council and Other Projects','Operation and Maintenance Expenses','Long Term Investments','Other Outflows']

		self.fields['category']=AutocompleteBox(self.fieldsFrame.interior,
			label="Category",toolTip="[Council and Other Projects]: Cash outflows from all projects undertaken by the council.\n[Operation and Maintenance Expenses]: Cash outflows from recurring expenses of operation and upkeep of the council.\n[Long Term Investments]: Cash outflows for assets intended for use and ownership beyond the current academic year.\n[Other Outflows]: Cash outflows other than those incurred for council projects, operations and maintenance and long term investments")
		self.fields['category'].initDropDown(options)

		self.fields['event']=AutocompleteBox(self.fieldsFrame.interior,
			label="Event",toolTip="Specify event if applicable.")
		self.fields['event'].initComboBox(self.app.listOptions("CD_Event"))

		self.fields['purpose']=TextFieldBox(self.fieldsFrame.interior,
			label="Purpose",toolTip="What the cash was used for.")

		self.fields['nature']=AutocompleteBox(self.fieldsFrame.interior,
			label="Nature",toolTip=None)
		self.fields['nature'].initComboBox(self.app.listOptions("CD_Nature"))

		self.fields['amount'] = TextFieldBox(self.fieldsFrame.interior,
			label="Amount",readonly=False,height=1,textType="number",
			toolTip="Actual amount given to liquidating person/payee regardless if actual expenditure differs")

		self.fields['liquidatingPerson'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Liquidating Person/Payee",toolTip="Name of the individual who actually received the cash.")
		self.fields['liquidatingPerson'].initComboBox(self.app.listOptions("CD_Payee"))

		self.fields['docNo'] = TextFieldBox(self.fieldsFrame.interior,
			label="Document Number",toolTip="Put all receipt numbers here, if any. If cash is disbursed before the expenditure, indicate in the notes column that this is so.")

		self.fields['notes'] = TextFieldBox(self.fieldsFrame.interior,
			label="Notes",toolTip="Any additional notes.")

		self.fields['remarks'] = TextFieldBox(self.fieldsFrame.interior,
			label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
			self.fields[i].pack(side=TOP,fill=X,expand=1)


	def newButtonCallback(self):
		#portable
		dummyEntry=newExistsInTree(self.tree)
		if not dummyEntry:
			dummyEntry=self.tree.insert("","end",text="New",values=["" for i in self.colList])
		else:
			dummyEntry=dummyEntry[0]
		self.tree.selection_set(dummyEntry)
		self.selectedpk="New"


	def getSelection(self,event):
		#semiportable -> must have dateOfTransaction
		item=self.tree.selection()[0]
		values=self.tree.item(item,'values')
		for i in range(0,len(self.fieldList)):
			self.fields[self.fieldList[i]].text=values[i]

		if self.fields['dateOfTransaction'].text=="":
			self.fields['dateOfTransaction'].text=secsToDay(getEpochTime())
		self.selectedpk=self.tree.item(item,"text")

	def _populateTree(self,entryList):
		#semiportable -> doesn't work if no total
		total=0
		[self.tree.delete(item) for item in self.tree.get_children()]
		for i in entryList:
			dataFields=[]
			pk=i.pk.content
			try:
				amt=float(i.amount.content)
			except:
				amt=0
			if i.status.content!="DELETED":
				total+=amt
			for j in self.fieldList:
				dataFields.append(vars(i)[j].content)
			dataFields[0]=secsToString(dataFields[0])
			dataFields[1]=secsToDay(dataFields[1])

			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))
		self.totalLabel.config(text="Total Cash Disbursments: "+floatToStr(total))
		self.total=total

	def populateTree(self,*a):
		#nonportable
		self.fieldList=['timestamp','dateOfTransaction','category',
			'event','purpose','nature','amount','liquidatingPerson',
			'docNo','notes','remarks']
		showDeleted = self.deletedVar.get()
		self._populateTree(self.app.listCashDisbursments(showDeleted=showDeleted))

	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		excelBuilder = ExcelBuilder()
		self.addSheet(excelBuilder)
		excelBuilder.build()

	def addSheet(self, excelBuilder):
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList
		fileName = 'CashDisbursements_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setFileName(fileName)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Cash Disbursements")
		excelBuilder.buildSheet()
		


	def save(self,*a):
		#nonportable
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk = self.app.editCashDisbursment(self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				category=self.fields['category'].text,
				event=self.fields['event'].text,
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text)
		else:
			self.selectedpk=self.app.newCashDisbursment(dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				category=self.fields['category'].text,
				event=self.fields['event'].text,
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		self.app.addOption("CD_Nature",self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values=self.app.listOptions("CD_Nature"))
		self.app.addOption("CD_Event",self.fields['event'].text)
		self.app.addOption("CD_Payee",self.fields['liquidatingPerson'].text)
		self.fields['event'].comboBox.config(values=self.app.listOptions("CD_Event"))
		self.fields['liquidatingPerson'].comboBox.config(values=self.app.listOptions("CD_Payee"))

		self.newButtonCallback()

	def delete(self):
		#nonportable
		if self.selectedpk!="New":
			self.app.deleteCashDisbursment(self.selectedpk)
		self.populateTree()

class OperationMaintenanceExpensesWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList = ["Timestamp","Date of Transaction","Purpose","Nature","Amount","Liquidating Person/Payee","Receipt Number","Notes","Remarks"]
		tree['columns']=colList
		for i in colList:
			tree.heading(i,text=i,command=lambda _i=i:treeview_sort_column(tree,_i,False))
			tree.column(i,anchor=W,width=60)
		tree.column("#0",width=3,anchor=W)
		if "Amount" in colList:
			tree.column("Amount",anchor=E)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y,expand=0)
		xscroll.pack(side=TOP,fill=X,expand=0)
		tree.pack(side=LEFT,fill=BOTH,expand=1)
		tree.tag_configure("deleted",foreground="red")

	def initFields(self):
		self.fields={}
		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)
		self.fields['dateOfTransaction']=CalendarBox(self.fieldsFrame.interior,
			label="Date of Transaction")
		self.fields['dateOfTransaction'].pack(side=TOP,expand=1,fill=X)

		self.fields['purpose']=TextFieldBox(self.fieldsFrame.interior,
			label="Purpose",toolTip="What the cash was used for.")

		self.fields['nature']=AutocompleteBox(self.fieldsFrame.interior,
			label="Nature",toolTip=None)
		self.fields['nature'].initComboBox(self.app.listOptions("OME_Nature"))

		self.fields['amount'] = TextFieldBox(self.fieldsFrame.interior,
			label="Amount",readonly=False,height=1,textType="number",
			toolTip="Amount of actual expenditure")

		self.fields['liquidatingPerson'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Liquidating Person/Payee",toolTip="Name of the individual who actually received the cash.")
		self.fields['liquidatingPerson'].initComboBox(self.app.listOptions("OME_Payee"))

		self.fields['receiptNumber'] = TextFieldBox(self.fieldsFrame.interior,
			label="Receipt number",toolTip="Put all receipt numbers here.")

		self.fields['notes'] = TextFieldBox(self.fieldsFrame.interior,
			label="Notes",toolTip="Any added notes about the transaction.")

		self.fields['remarks'] = TextFieldBox(self.fieldsFrame.interior,label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
	def populateTree(self,*a):
		self.fieldList=['timestamp','dateOfTransaction','purpose','nature','amount','liquidatingPerson','receiptNumber','notes','remarks']
		showDeleted=self.deletedVar.get()
		self._populateTree(self.app.listOMEs(showDeleted=showDeleted))

	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		excelBuilder = ExcelBuilder()
		self.addSheet(excelBuilder)
		excelBuilder.build()

	def addSheet(self, excelBuilder):
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList
		fileName = 'OperationMaint_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setFileName(fileName)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Oper. and Maint. Expense")
		excelBuilder.buildSheet()


	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk = self.app.editOME(self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				receiptNumber=self.fields['receiptNumber'].text,
				notes=self.fields['notes'].text)
		else:
			self.selectedpk=self.app.newOME(
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				receiptNumber=self.fields['receiptNumber'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		self.app.addOption("OME_Nature",self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values=self.app.listOptions("OME_Nature"))
		self.app.addOption("OME_Payee",self.fields['liquidatingPerson'].text)
		self.fields['liquidatingPerson'].comboBox.config(values=self.app.listOptions("OME_Payee"))

		self.newButtonCallback()

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteOME(self.selectedpk)
		self.populateTree()

class ExcelBuilder(object):
	"""To use: instantiate, call all setter methods, then call build"""
	def __init__(self):
		self.EXPORT_DIRECTORY = 'ExcelExports'
		self.setTableColumnWidth(5000)
		self.setFileName("export.xls")
		self.setStartingPoint(3, 0)
		self.book = Workbook()

		# Create export directory if it doesn't exist
		if not os.path.exists(self.EXPORT_DIRECTORY):
			os.makedirs(self.EXPORT_DIRECTORY)

	def setRows(self, value):
		"""Expects a list of tuples where tuple[0] is the list of column values in order
		and tuple[1] contains the tags e.g. 'deleted' or 'none'"""
		self.rows = value

	def setStartingPoint(self, row, column):
		"""Sets the starting row and column for the table in the excel file"""
		self.row = row
		self.column = column

	def setColumnHeaders(self, value):
		"""Expects a list of strings"""
		self.colList = value

	def setFileName(self, string):
		"""Sets the file name to be saved"""
		self.fileName = string

	def setTableColumnWidth(self, value):
		self.colWidth = value

	def setSheetName(self, string):
		self.sheetName = string
		
	def build(self):
		"""Builds and saves the excel file"""
		# Save the excel file
		self.book.save(self.fileName)
		shutil.move(self.fileName, self.EXPORT_DIRECTORY+'/'+self.fileName)

	def buildSheet(self):
		"""Adds the sheet to the workbook"""
		self.sheet = sheet = self.book.add_sheet(self.sheetName)
		headerStyle = easyxf('font: bold 1;')
		editedStyle = easyxf('font: color orange;')
		deletedStyle = easyxf('font: color red;')
		# starting location of the table
		startingRow = self.row
		startingCol = self.column
		# adjust column widths
		for i in xrange(self.column, self.column + len(self.colList)):
			sheet.col(i).width = self.colWidth

		# Write auto-generated timestamp
		timeNow = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
		sheet.write(0, 0, "This file was generated on " + timeNow)

		# Write the table column names
		colList = self.colList
		colNumber = startingCol
		for columnHeader in colList:
			sheet.write(startingRow, colNumber, columnHeader, headerStyle)
			colNumber += 1
		colNumber = startingCol
		rowNumber = startingRow + 1

		# Write the table data
		for i in self.rows:
			for columnValue in i[0]:
				if "none" in i[1]:
					sheet.write(rowNumber, colNumber, columnValue)
				elif "deleted" in i[1]:
					sheet.write(rowNumber, colNumber, columnValue, deletedStyle)
				elif "edited" in i[1]:
					sheet.write(rowNumber, colNumber, columnValue, editedStyle)
				colNumber += 1
			colNumber = startingCol
			rowNumber += 1

if __name__=="__main__":
	root = Tk()
	program = CashReceiptsWindow(root,None)
	program.mainloop()