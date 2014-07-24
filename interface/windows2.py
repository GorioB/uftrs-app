from windows import *
from Tkinter import *
from ttk import *
from ScrolledFrame import VerticalScrolledFrame
from interface.textfield import *
from interface.datefield import *
from interface.autocomplete import *
from interface.readingBox import ReadingBox
from lib.timeFuncs import *
import datetime
from lib.models import *
from lib.floattostr import *
from checkbuttonbox import *
from lib.db import *
from interface.previewnotes import *
from lib.floattostr import *
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
class EmptyBox(object):
	def __init__(self):
		self.text="N/A"
def notebookLockTabs(noteBook,tabIndex):
	others = [i for i in noteBook.tabs() if i!=tabIndex]
	for i in others:
		noteBook.tab(i,state="disabled")

def notebookUnlockTabs(noteBook):
	for i in noteBook.tabs():
		noteBook.tab(i,state="normal")

class OALWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList=["Timestamp","Include","Type","Category","Details","Remarks"]
		tree['columns']=colList
		for i in colList:
			tree.heading(i,text=i,command=lambda _i=i:treeview_sort_column(tree,_i,False))
			tree.column(i,anchor=W,width=60)
		tree.column("#0",width=0,anchor=W)
		if "Amount" in colList:
			tree.column("Amount",anchor=E)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y,expand=0)
		xscroll.pack(side=TOP,fill=X,expand=0)
		tree.pack(side=LEFT,fill=BOTH,expand=1)
		tree.tag_configure("deleted",foreground="red")

	def initTotalTag(self):
		pass

	def initFields(self):
		
		self.fieldsNotebook = Notebook(self.fieldsFrame.interior)
		self.accountsOutstandingFrame=Frame(self.fieldsNotebook)
		self.inventoriesAndOtherAssetsFrame = Frame(self.fieldsNotebook)
		self.othersFrame = Frame(self.fieldsNotebook)
		self.fieldsNotebook.add(self.accountsOutstandingFrame,text="Accounts Outstanding")
		self.fieldsNotebook.add(self.inventoriesAndOtherAssetsFrame,text="Inventories and Other Material Assets")
		self.fieldsNotebook.add(self.othersFrame,text="Others")

		self.fieldsNotebook.pack(fill=BOTH,expand=1)
		self.fieldsNotebook.pack_propagate(0)

		self.fields={}
		self.fields['accountsOutstanding']={}
		self.fields['inventoriesAndOtherAssets']={}
		self.fields['others']={}

		#accountsOutstanding

		cn='accountsOutstanding'
		self.fields[cn]['timestamp']=TextFieldBox(self.accountsOutstandingFrame,
			label="Timestamp",readonly=True,height=1)
		self.fields[cn]['include']=CheckButtonBox(self.accountsOutstandingFrame)
		self.fields[cn]['include'].pack(fill=X,expand=1)
		self.fields[cn]['category']=AutocompleteBox(self.accountsOutstandingFrame,
			label="Category")
		options=["Payable","Receivable"] #Don't overwrite
		self.fields[cn]['category'].initDropDown(options)

		self.fields[cn]['details']=TextFieldBox(self.accountsOutstandingFrame,
			label="Description",height=5)

		helpfulMessage = ReadingBox(self.accountsOutstandingFrame,text="[Receivable]: Please indicate the amount, the payor's name, source of the receivable, and other pertinent data.\n\t(e.g. Receivable of P5,000.00 in cash from Company XYZ in accordance with the sponsorship agreement entered into last October 15, 2013. This is expected to increase the cash balance next month.)\n[Payable]: Please indicate the amount, the payee's name, source of the payable, and other pertinent data.\n\t(e.g. Payable of P500.00 in cash to Councilor A as reimbursement for purchase of office supplies. This is expected to decrease the cash balance in the following month.)",
			)

		for i in self.fields[cn]:
			self.fields[cn][i].bind("<Return>",self.save)
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage.pack(fill=BOTH,expand=1)

		#inventoriesAndOtherAssets
		cn='inventoriesAndOtherAssets'

		self.fields[cn]['timestamp'] = TextFieldBox(self.inventoriesAndOtherAssetsFrame,
			label="Timestamp",readonly=True,height=1)
		self.fields[cn]['include'] = CheckButtonBox(self.inventoriesAndOtherAssetsFrame)
		self.fields[cn]['include'].pack(fill=X,expand=1)

		self.fields[cn]['category']=AutocompleteBox(self.inventoriesAndOtherAssetsFrame,
			label="Category")
		self.fields[cn]['category'].initDropDown(['Inventory','Other Material Asset'])
		self.fields[cn]['details']=TextFieldBox(self.inventoriesAndOtherAssetsFrame,
			label="Description",height=5)
		helpfulMessage2 = ReadingBox(self.inventoriesAndOtherAssetsFrame,
			text="Please indicate the item in question, the amount, the source of the item, and other pertinent data.\n\t(e.g. Received X-deals from Company DEF. 200 black ballpens were received in good condition on October 20, 2013. These are expected to be given away as freebies during the general registration next semester.)\n\t(e.g. Received a brand-new projector from Company GHI in accordance with the sponsorship agreement entered into last August 24, 2013. The projector was received in good condition on September 12, 2013.)")

		for i in [i for i in self.fields[cn] if i!="category"]:
			self.fields[cn][i].bind("<Return>",self.save)
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage2.pack(fill=BOTH,expand=1)

		#others
		cn='others'
		self.fields[cn]['timestamp']=TextFieldBox(self.othersFrame,
			label="Timestamp",readonly=True,height=1)
		self.fields[cn]['include']=CheckButtonBox(self.othersFrame)
		self.fields[cn]['include'].pack(fill=X,expand=1)

		self.fields[cn]['category']=AutocompleteBox(self.othersFrame,
			label="Category")
		self.fields[cn]['category'].initComboBox(self.app.listOptions("OAL_Category"))

		self.fields[cn]['details']=TextFieldBox(self.othersFrame,
			label="Description",height=5)
		helpfulMessage3=ReadingBox(self.othersFrame,scrollX=False,
			text="Please indicate the item in question, the amount, the source of the item, and other pertinent data.")

		for i in self.fields[cn]:
			self.fields[cn][i].bind("<Return>",self.save)
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage3.pack(side=TOP,fill=X,expand=1)

		self.fieldsIdent={}
		self.fieldsIdent['accountsOutstanding']=self.fieldsNotebook.tabs()[0]
		self.fieldsIdent['inventoriesAndOtherAssets']=self.fieldsNotebook.tabs()[1]
		self.fieldsIdent['others']=self.fieldsNotebook.tabs()[2]

	def newButtonCallback(self):
		notebookUnlockTabs(self.fieldsNotebook)
		CashDisbursmentsWindow.newButtonCallback(self)

	def getSelection(self,event):
		item=self.tree.selection()[0]
		self.selectedpk=self.tree.item(item,"text")

		values=self.tree.item(item,'values')
		humanToCode={"":"","Accounts Outstanding":"accountsOutstanding","Others":"others","Inventories and Other Assets":"inventoriesAndOtherAssets"}
		cn = humanToCode[values[2]]
		if self.selectedpk=="New":
			for i in self.fields:
				for j in self.fields[i]:
					self.fields[i][j].text =""
			cn='accountsOutstanding'
		notebookUnlockTabs(self.fieldsNotebook)
		self.fieldsNotebook.select(self.fieldsIdent[cn])
		
		fieldIndices={'timestamp':0,'include':1,'OALType':2,'category':3,'details':4,'remarks':5}
		for i in self.fields[cn]:
			self.fields[cn][i].text=values[fieldIndices[i]]

		if self.selectedpk!="New":
			notebookLockTabs(self.fieldsNotebook,self.fieldsIdent[cn])

	def _populateTree(self,entryList):
		pass

	def populateTree(self,*a):
		[self.tree.delete(item) for item in self.tree.get_children()]
		self.fieldList=['timestamp','includeInStatement','OALType','category','details','remarks']
		showDeleted=self.deletedVar.get()
		entryList = self.app.listOALs(showDeleted=showDeleted)
		codeToHuman = {"accountsOutstanding":"Accounts Outstanding","others":"Others","inventoriesAndOtherAssets":"Inventories and Other Assets"}
		for i in entryList:
			dataFields=[]
			pk=i.pk.content
			for j in self.fieldList:
				dataFields.append(vars(i)[j].content)
			dataFields[0]=secsToString(dataFields[0])
			dataFields[2]=codeToHuman[dataFields[2]]

			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))

	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		excelBuilder = ExcelBuilder()
		self.addSheet(excelBuilder)
		excelBuilder.build()

	def addSheet(self, excelBuilder):
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList
		fileName = 'OAL_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setFileName(fileName)
		excelBuilder.setTableColumnWidth(7000)
		excelBuilder.setSheetName("Other Assets and Liabilities")
		excelBuilder.buildSheet()


	def save(self,*a):
		cn=[i for i in self.fieldsIdent if self.fieldsIdent[i]==self.fieldsNotebook.select()][0]
		if checkFields(self.fields[cn]):
			return 1
		if self.selectedpk!="New":
			old = self.app.getOAL(self.selectedpk)
			if old.OALType.content!=cn or old.category.content!=self.fields[cn]['category'].text or old.details.content!=self.fields[cn]['details'].text:
				self.selectedpk=self.app.editOAL(self.selectedpk,
					OALType=cn,
					category=self.fields[cn]['category'].text,
					details=self.fields[cn]['details'].text)
			self.app.toggleOAL(self.selectedpk,self.fields[cn]['include'].text)
		else:
			self.selectedpk=self.app.newOAL(
				OALType=cn,
				category=self.fields[cn]['category'].text,
				details=self.fields[cn]['details'].text,
				includeInStatement=self.fields[cn]['include'].text)
		self.populateTree()

		if cn=="others":
			self.app.addOption("OAL_Category",self.fields[cn]['category'].text)
			self.fields[cn]['category'].comboBox.config(values=self.app.listOptions("OAL_Category"))

		self.newButtonCallback()

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteOAL(self.selectedpk)
		self.populateTree()

class COCPWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList = ["Note #","Timestamp","Date of Transaction","Event/Project","Inflow/Outflow","Purpose","Nature","Amount","Liquidating Person/Payee's Name","Official Receipt #","Notes","Remarks"]
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
		pass

	def initFields(self):
		self.fields={}
		self.fields['noteNumber'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Note #")
		self.fields['noteNumber'].initComboBox(self.app.listOptions("NoteNumber"))

		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)

		self.fields['dateOfTransaction']=CalendarBox(self.fieldsFrame.interior,
			label="Date of Transaction")
		self.fields['dateOfTransaction'].pack(fill=X,expand=1,side=TOP)
		self.fields['event']=AutocompleteBox(self.fieldsFrame.interior,
			label="Event/Project",toolTip="Specify Event")
		self.fields['event'].initComboBox(self.app.listOptions("COCP_Event"))

		self.fields['flowDirection']=AutocompleteBox(self.fieldsFrame.interior,
			label="Inflow/Outflow")
		self.fields['flowDirection'].initDropDown(["Inflow","Outflow"])

		self.fields['purpose']=TextFieldBox(self.fieldsFrame.interior,
			label="Purpose",toolTip="What the cash was used for.")

		self.fields['nature']=AutocompleteBox(self.fieldsFrame.interior,
			label="Nature",toolTip='The "Council Budget" is a budgeting tool for events to determine whether the expenditures are within the budget. They are not actual cash inflows but are categorized as inflows as a tool only.')
		self.natureFromReceipts = self.app.listOptions("Nature")
		self.fields['nature'].initComboBox(["Council Budget"]+self.natureFromReceipts)

		self.fields['amount']=TextFieldBox(self.fieldsFrame.interior,
			label="Amount",toolTip="Amount of actual expenditure",height=1,textType="number")

		self.fields['liquidatingPerson']=AutocompleteBox(self.fieldsFrame.interior,
			label="Liquidating Person/Payee's Name",toolTip="Name of the individual who actually received the cash for the expenditure")
		self.fields['liquidatingPerson'].initComboBox(self.app.listOptions("COCP_Payee"))

		self.fields['docNo']=TextFieldBox(self.fieldsFrame.interior,
			label="Reference Document",toolTip="Put all receipt numbers here")

		self.fields['notes']=TextFieldBox(self.fieldsFrame.interior,
			label="Notes",toolTip="Any added notes about the transaction")

		self.fields['remarks']=TextFieldBox(self.fieldsFrame.interior,
			label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
	def _populateTree(self,entryList):
		pass

	def populateTree(self,*a):
		self.fieldList=['noteNumber','timestamp','dateOfTransaction','event','flowDirection','purpose','nature','amount','liquidatingPerson','docNo','notes','remarks']
		showDeleted=self.deletedVar.get()
		[self.tree.delete(item) for item in self.tree.get_children()]
		entryList = self.app._listGeneral(COCPNote,showDeleted=showDeleted)
		for i in entryList:
			dataFields=[]
			pk = i.pk.content
			for j in self.fieldList:
				dataFields.append(vars(i)[j].content)
			dataFields[1]=secsToString(dataFields[1])
			dataFields[2]=secsToDay(dataFields[2])

			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))
		self.fields['nature'].comboBox.config(values=["Council Budget",]+self.app.listOptions("Nature"))

	def addSheet(self, excelBuilder):
		"""Called by the Notes tab's exportToExcel method"""
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Notes- Council & Other Projects")
		excelBuilder.buildSheet()

	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk = self.app.editNote("COCPNote",self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				event=self.fields['event'].text,
				flowDirection=self.fields['flowDirection'].text,
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text,
				noteNumber=self.fields['noteNumber'].text)
		else:
			self.selectedpk=self.app.newNote("COCPNote",self.fields['noteNumber'].text,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				event=self.fields['event'].text,
				flowDirection=self.fields['flowDirection'].text,
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		self.app.addOption("COCP_Event",self.fields['event'].text)
		self.fields['event'].comboBox.config(values=self.app.listOptions("COCP_Event"))
		self.app.addOption("COCP_Payee",self.fields['liquidatingPerson'].text)
		self.fields['liquidatingPerson'].comboBox.config(values=self.app.listOptions("COCP_Payee"))
		self.app.addOption("NoteNumber",self.fields['noteNumber'].text)
		self.fields['noteNumber'].comboBox.config(values=self.app.listOptions("NoteNumber"))
		self.newButtonCallback()

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteNote("COCPNote",self.selectedpk)
		self.populateTree()

class LTIWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList=["Note #","Timestamp","Date of Transaction","Purpose","Nature","Amount","Liquidating Person/Payee's Name","Official Receipt #","Notes","Remarks"]
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
		self.fields['noteNumber'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Note #")
		self.fields['noteNumber'].initComboBox(self.app.listOptions("NoteNumber"))

		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)

		self.fields['dateOfTransaction']=CalendarBox(self.fieldsFrame.interior,
			label="Date of Transaction")
		self.fields['dateOfTransaction'].pack(fill=X,expand=1,side=TOP)
		self.fields['purpose']=TextFieldBox(self.fieldsFrame.interior,
			label="Purpose",toolTip="What the cash was used for.")

		self.fields['nature']=AutocompleteBox(self.fieldsFrame.interior,
			label="Nature",toolTip='The "Council Budget" is a budgeting tool for events to determine whether the expenditures are within the budget. They are not actual cash inflows but are categorized as inflows as a tool only.')
		self.natureFromReceipts = self.app.listOptions("LTI_Nature")
		self.fields['nature'].initComboBox(["Council Budget"]+self.natureFromReceipts)

		self.fields['amount']=TextFieldBox(self.fieldsFrame.interior,
			label="Amount",toolTip="Amount of actual expenditure",height=1,textType="number")

		self.fields['liquidatingPerson']=AutocompleteBox(self.fieldsFrame.interior,
			label="Liquidating Person/Payee's Name",toolTip="Name of the individual who actually received the cash for the expenditure")
		self.fields['liquidatingPerson'].initComboBox(self.app.listOptions("LTI_Payee"))

		self.fields['docNo']=TextFieldBox(self.fieldsFrame.interior,
			label="Reference Document",toolTip="Put all receipt numbers here")

		self.fields['notes']=TextFieldBox(self.fieldsFrame.interior,
			label="Notes",toolTip="Any added notes about the transaction")
	
		self.fields['remarks']=TextFieldBox(self.fieldsFrame.interior,
			label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
	# def _populateTree(self,entryList):
	# 	pass

	def _populateTree(self,entryList):
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
			dataFields[1]=secsToString(dataFields[1])
			dataFields[2]=secsToDay(dataFields[2])

			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))
		self.totalLabel.config(text="Total Long Term Investments: "+floatToStr(total))
		self.total=total
	def populateTree(self,*a):
		self.fieldList=['noteNumber','timestamp','dateOfTransaction','purpose','nature','amount','liquidatingPerson','docNo','notes','remarks']
		showDeleted=self.deletedVar.get()
		self._populateTree(self.app._listGeneral(LTINote,showDeleted=showDeleted))

	def addSheet(self, excelBuilder):
		"""Called by the Notes tab's exportToExcel method"""
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Notes- Long Term Investments")
		excelBuilder.buildSheet()

	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk=self.app.editNote("LTINote",self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text,
				noteNumber=self.fields['noteNumber'].text)
		else:
			self.selectedpk=self.app.newNote("LTINote",self.fields['noteNumber'].text,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		self.app.addOption("LTI_Nature",self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values=self.app.listOptions("LTI_Nature"))
		self.app.addOption("LTI_Payee",self.fields['liquidatingPerson'].text)
		self.fields['liquidatingPerson'].comboBox.config(values=self.app.listOptions("LTI_Payee"))
		self.app.addOption("NoteNumber",self.fields['noteNumber'].text)
		self.fields['noteNumber'].comboBox.config(values=self.app.listOptions("NoteNumber"))
		self.newButtonCallback()

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteNote("LTINote",self.selectedpk)
		self.populateTree()

class OOWindow(LTIWindow):
	def initFields(self):
		self.fields={}
		self.fields['noteNumber'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Note #")
		self.fields['noteNumber'].initComboBox(self.app.listOptions("NoteNumber"))

		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)

		self.fields['dateOfTransaction']=CalendarBox(self.fieldsFrame.interior,
			label="Date of Transaction")
		self.fields['dateOfTransaction'].pack(fill=X,expand=1,side=TOP)
		self.fields['purpose']=TextFieldBox(self.fieldsFrame.interior,
			label="Purpose",toolTip="What the cash was used for.")

		self.fields['nature']=AutocompleteBox(self.fieldsFrame.interior,
			label="Nature",toolTip='The "Council Budget" is a budgeting tool for events to determine whether the expenditures are within the budget. They are not actual cash inflows but are categorized as inflows as a tool only.')
		self.natureFromReceipts = self.app.listOptions("OO_Nature")
		self.fields['nature'].initComboBox(["Council Budget"]+self.natureFromReceipts)

		self.fields['amount']=TextFieldBox(self.fieldsFrame.interior,
			label="Amount",toolTip="Amount of actual expenditure",height=1,textType="number")

		self.fields['liquidatingPerson']=AutocompleteBox(self.fieldsFrame.interior,
			label="Liquidating Person/Payee's Name",toolTip="Name of the individual who actually received the cash for the expenditure")
		self.fields['liquidatingPerson'].initComboBox(self.app.listOptions("OO_Payee"))

		self.fields['docNo']=TextFieldBox(self.fieldsFrame.interior,
			label="Reference Document",toolTip="Put all receipt numbers here")

		self.fields['notes']=TextFieldBox(self.fieldsFrame.interior,
			label="Notes",toolTip="Any added notes about the transaction")
	
		self.fields['remarks']=TextFieldBox(self.fieldsFrame.interior,
			label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)
	def populateTree(self,*a):
		self.fieldList=['noteNumber','timestamp','dateOfTransaction','purpose','nature','amount','liquidatingPerson','docNo','notes','remarks']
		showDeleted=self.deletedVar.get()
		self._populateTree(self.app._listGeneral(OONote,showDeleted=showDeleted))


	def addSheet(self, excelBuilder):
		"""Called by the Notes tab's exportToExcel method"""
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Notes- Other Outflows")
		excelBuilder.buildSheet()

	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk = self.app.editNote("OONote",self.selectedpk,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text,
				noteNumber=self.fields['noteNumber'].text)
		else:
			self.selectedpk=self.app.newNote("OONote",self.fields['noteNumber'].text,
				dateOfTransaction=stringToSecs(self.fields['dateOfTransaction'].text+":0:0:0"),
				purpose=self.fields['purpose'].text,
				nature=self.fields['nature'].text,
				amount=(self.fields['amount'].text),
				liquidatingPerson=self.fields['liquidatingPerson'].text,
				docNo=self.fields['docNo'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		self.app.addOption("OO_Nature",self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values=self.app.listOption("OO_Nature"))
		self.app.addOption("OO_Payee",self.fields['liquidatingPerson'].text)
		self.fields['liquidatingPerson'].comboBox.config(values=self.app.listOption("OO_Payee"))
		self.app.addOption("NoteNumber",self.fields['noteNumber'].text)
		self.fields['noteNumber'].comboBox.config(values=self.app.listOptions("NoteNumber"))
		self.newButtonCallback()

	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteNote("OONote",self.selectedpk)
		self.populateTree()

class ODNWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList = ["Note #","Timestamp","Description","Remarks"]
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
		pass

	def initFields(self):
		self.fields={}
		self.fields['noteNumber'] = AutocompleteBox(self.fieldsFrame.interior,
			label="Note #")
		self.fields['noteNumber'].initComboBox(self.app.listOptions("NoteNumber"))

		self.fields['timestamp']=TextFieldBox(self.fieldsFrame.interior,
			label="Timestamp",readonly=True,height=1)

		self.fields['description'] = TextFieldBox(self.fieldsFrame.interior,
			label="Description",height=7)

		self.fields['remarks'] = TextFieldBox(self.fieldsFrame.interior,
			label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].bind("<Return>",self.save)

	def getSelection(self,event):
		item = self.tree.selection()[0]
		values = self.tree.item(item,'values')
		for i in range(0,len(self.fieldList)):
			self.fields[self.fieldList[i]].text=values[i]

		self.selectedpk=self.tree.item(item,"text")
		
	def _populateTree(self,entryList):
		pass

	def populateTree(self,*a):
		self.fieldList=['noteNumber','timestamp','description','remarks']
		showDeleted = self.deletedVar.get()
		[self.tree.delete(item) for item in self.tree.get_children()]
		entryList = self.app._listGeneral(ODNote,showDeleted=showDeleted)
		for i in entryList:
			dataFields=[]
			pk=i.pk.content
			for j in self.fieldList:
				dataFields.append(vars(i)[j].content)
			dataFields[1]=secsToString(dataFields[1])

			if 'amount' in self.fieldList:
				dataFields[self.fieldList.index('amount')]=floatToStr(dataFields[self.fieldList.index('amount')])

			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))

	def addSheet(self, excelBuilder):
		"""Called by the Notes tab's exportToExcel method"""
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		columnHeaders = self.colList

		excelBuilder.setRows(rows)
		excelBuilder.setColumnHeaders(columnHeaders)
		excelBuilder.setStartingPoint(2, 0)
		excelBuilder.setTableColumnWidth(5000)
		excelBuilder.setSheetName("Notes- Other Descriptive Notes")
		excelBuilder.buildSheet()

	def save(self,*a):
		if checkFields(self.fields):
			return 1
		if self.selectedpk!="New":
			self.selectedpk=self.app.editNote("ODNote",self.selectedpk,
				description=self.fields['description'].text,
				noteNumber=self.fields['noteNumber'].text)
		else:
			self.selectedpk=self.app.newNote("ODNote",self.fields['noteNumber'].text,
				description=self.fields['description'].text)
		self.app.addOption("NoteNumber",self.fields['noteNumber'].text)
		self.fields['noteNumber'].comboBox.config(values=self.app.listOptions("NoteNumber"))
		self.populateTree()

		self.newButtonCallback()


	def delete(self):
		if self.selectedpk!="New":
			self.app.deleteNote("ODNote",self.selectedpk)
		self.populateTree()

class NotesWindow(Frame,object):
	def __init__(self,parent,app,deletedVar):
		Frame.__init__(self,parent)
		self.parent=parent
		self.nb = Notebook(self.parent)
		self.notes={}
		self.app=app
		self.deletedVar=deletedVar
		for i in ["Council and Other College Projects","Long Term Investments","Other Outflows","Other Descriptive Notes","Preview"]:
			self.notes[i]=Frame(self.nb)
			self.nb.add(self.notes[i],text=i)
		self.nb.pack(fill=BOTH,expand=1)
		self.nb.pack_propagate(0)

		self.notes['Council and Other College Projects']=COCPWindow(self.notes['Council and Other College Projects'],self.app,deletedVar=self.deletedVar)
		self.notes['Council and Other College Projects'].pack()

		self.notes['Long Term Investments']=LTIWindow(self.notes['Long Term Investments'],self.app,deletedVar=self.deletedVar)
		self.notes['Long Term Investments'].pack()

		self.notes['Other Outflows']=OOWindow(self.notes['Other Outflows'],self.app,deletedVar=self.deletedVar)
		self.notes['Other Outflows'].pack()

		self.notes['Other Descriptive Notes'] = ODNWindow(self.notes['Other Descriptive Notes'],self.app,deletedVar=self.deletedVar)
		self.notes['Other Descriptive Notes'].pack()

		self.notes['Preview'] = PreviewPage(self.notes['Preview'],self.app,deletedVar=self.deletedVar)
		self.notes['Preview'].pack(fill=BOTH,expand=1,side=TOP)
		self.nb.bind("<<NotebookTabChanged>>",self.refreshPage)
	def populateTree(self,*a):
		self.refreshPage()

	def refreshPage(self,*a):
		selectedpage = self.nb.select()
		tabName=self.nb.tab(selectedpage,option="text")
		self.notes[tabName].populateTree()

	def exportToExcel(self):
		"""Exports all subtabs as different sheets under one excel file"""
		excelBuilder = ExcelBuilder()
		self.addSheet(excelBuilder)

		fileName = 'Notes_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'
		excelBuilder.setFileName(fileName)

		excelBuilder.build()

	def addSheet(self, excelBuilder):
		for key in ["Council and Other College Projects","Long Term Investments","Other Outflows","Other Descriptive Notes"]:
			subTab = self.notes[key]
			subTab.addSheet(excelBuilder)
