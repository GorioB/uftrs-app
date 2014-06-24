from Tkinter import *
from ttk import *
from ScrolledFrame import VerticalScrolledFrame
from interface.textfield import *
from interface.datefield import *
from interface.autocomplete import *
from lib.timeFuncs import *
try:
	from xlwt import Workbook, easyxf
except:
	print "Requires xlwt"
	exit(1)
import datetime

class CashReceiptsWindow(Frame,object):
	def __init__(self,parent,app,deletedVar=None):
		Frame.__init__(self,parent)
		self.selectedpk=0
		self.parent=parent
		self.app=app
		if deletedVar:
			self.deletedVar = deletedVar
		else:
			self.deletedVar=BooleanVar()
			self.deletedVar.set(0)

		self.deletedVar.trace("w",self.populateTree)
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
		leftFrameUpper = Frame(leftFrame)
		leftFrameLower = Frame(leftFrame)
		leftFrameLower.pack(expand=0,fill=X,side=BOTTOM)
		leftFrameUpper.pack(expand=1,fill=BOTH,side=BOTTOM)

		self.tree = tree = Treeview(leftFrameUpper,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(leftFrameUpper,orient="vertical",command=tree.yview)
		xscroll=Scrollbar(leftFrameLower,orient="horizontal",command=tree.xview)
		colList = ["Timestamp","Date of Transaction","Category","Nature","Amount","Payor's Name","Acknowledgement Receipt #","Notes","Remarks"]
		tree['columns']= colList
		for i in colList:
			tree.heading(i,text=i)
			tree.column(i,anchor=W,width=60)
		tree.column('#0',width=3,anchor=W)
		tree.configure(yscroll=yscroll.set,xscroll=xscroll.set)
		yscroll.pack(side=RIGHT,fill=Y)
		xscroll.pack(side=TOP,fill=X)
		tree.pack(side=LEFT,fill=BOTH,expand=1)
		tree.tag_configure("deleted",foreground="red")

		#bottombar
		leftLowestFrame = Frame(leftFrameLower)
		leftLowestFrame.pack(fill=X,expand=0)
		newButton = Button(leftLowestFrame,text="New",command=self.newEntry)
		newButton.pack(fill=None,expand=0,side=LEFT)
		self.totalLabel=totalLabel=Label(leftLowestFrame,text="Total: ",relief=SUNKEN,width=20)
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

		saveButton = Button(lowerRight,text="Save",command=self.save)
		saveButton.pack(side=LEFT,fill=X,expand=1)
		deleteButton = Button(lowerRight,text="Delete",command=self.delete)
		deleteButton.pack(side=LEFT,fill=X,expand=1)

		#fields
		self.fields={}
		newColList = colList
		self.fields['timestamp'] = timestamp = TextFieldBox(upperRight.interior,label="Timestamp",readonly=True,height=1)

		self.fields['dateOfTransaction']=dot = CalendarBox(upperRight.interior,label="Date of Transaction")

		#options for removal, get from DB
		options = ["Council Mandated Funds","General Sponsorship Inflows","Income Generating Projects","Other Inflows","Excess"]
		self.fields['category'] = category = AutocompleteBox(upperRight.interior,label="Category",toolTip="[Council Mandated Funds]: All fees, commissions and revenues that the council body is authorized to collect among students and all businesses within the college\n[General Sponsorhip Inflows]: Cash inflows acquired gratuitously from business organizations, studentry/alumni body and other entities\n[Income Generating Projects]: Cash inflows from all council events to raise revenues and generate additional funds supplementary to its operations\n[Other Inflows]: Cash inflows other than council mandated funds, general sponsoships and income generating projects")
		category.initDropDown(options)

		self.fields['nature']=nature = AutocompleteBox(upperRight.interior,label="Nature",toolTip=None)
		nature.initComboBox(self.app.listOptions("Nature"))

		self.fields['amount'] = TextFieldBox(upperRight.interior,label="Amount",readonly=False,height=1)

		self.fields['payor'] = TextFieldBox(upperRight.interior,label="Payor's Name",readonly=False,toolTip = "Name of the individual who actually gave the cash.")

		self.fields['receiptNumber'] = TextFieldBox(upperRight.interior,label="Acknowledgement Receipt #",readonly=False)

		self.fields['notes'] = TextFieldBox(upperRight.interior,label="Notes",toolTip = "Any additional notes about the transaction.")

		self.fields['remarks'] = TextFieldBox(upperRight.interior,label="Remarks",readonly=True)

		for i in self.fields:
			self.fields[i].pack(side=TOP,fill=X,expand=1)

	def getSelection(self,event):
		item = self.tree.selection()[0]
		values = self.tree.item(item,"values")

		for i in range(0,len(self.fieldList)):
			self.fields[self.fieldList[i]].text=values[i]

		if self.fields['dateOfTransaction']=="":
			self.fields['dateOfTransaction']="Calendar"
		self.selectedpk=self.tree.item(item,"text")
		print self.selectedpk

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
			if i.status.content=="DELETED":
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("deleted",))
			else:
				self.tree.insert("","end",text=str(pk),values=dataFields,tags=("none",))
		self.totalLabel.config(text="Total: "+str(total))
		self.total = total


	def exportToExcel(self):
		"""Exports the data displayed on the treebox to excel"""
		book = Workbook()
		sheet1 = book.add_sheet('Sheet 1')
		rows = [(self.tree.item(i,"values"), self.tree.item(i, "tags")) for i in self.tree.get_children()]
		headerStyle = easyxf('font: bold 1;')
		deletedStyle = easyxf('font: color red;')
		# starting location of the table
		startingRow = 3
		startingCol = 0
		# adjust column widths
		for i in xrange(9):
			sheet1.col(i).width = 5000

		# Write auto-generated timestamp
		timeNow = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
		sheet1.write(0, 0, "This file was generated on " + timeNow)

		# Write the table column names
		colList = ["Timestamp","Date of Transaction","Category","Nature","Amount","Payor's Name","Acknowledgement Receipt #","Notes","Remarks"]
		colNumber = startingCol
		for columnHeader in colList:
			sheet1.write(startingRow, colNumber, columnHeader, headerStyle)
			colNumber += 1
		colNumber = startingCol
		rowNumber = startingRow + 1

		# Write the table data
		for i in rows:
			for columnValue in i[0]:
				if "none" in i[1]:
					sheet1.write(rowNumber, colNumber, columnValue)
				elif "deleted" in i[1]:
					sheet1.write(rowNumber, colNumber, columnValue, deletedStyle)
				colNumber += 1
			colNumber = startingCol
			rowNumber += 1
		# Write the total
		sheet1.write(rowNumber, colNumber + 3, "TOTAL")
		sheet1.write(rowNumber, colNumber + 4, str(self.total))

		# Save the excel file
		fileName = 'CashReceipt_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'
		book.save(fileName)

	def save(self):
		if self.selectedpk!="New":
			self.selectedpk = self.app.editCashReceipt(self.selectedpk,
				dateOfTransaction=self.fields['dateOfTransaction'].text,
				category = self.fields['category'].text,
				nature = self.fields['nature'].text,
				amount = self.fields['amount'].text,
				payor = self.fields['payor'].text,
				receiptNumber = self.fields['receiptNumber'].text,
				notes = self.fields['notes'].text)
		else:
			self.selectedpk=self.app.newCashReceipt(
				dateOfTransaction=self.fields['dateOfTransaction'].text,
				category=self.fields['category'].text,
				nature=self.fields['nature'].text,
				amount=self.fields['amount'].text,
				payor=self.fields['payor'].text,
				receiptNumber = self.fields['receiptNumber'].text,
				notes=self.fields['notes'].text)
		self.populateTree()

		#combobox stuff
		self.app.addOption("Nature", self.fields['nature'].text)
		self.fields['nature'].comboBox.config(values = self.app.listOptions("Nature"))

	def newEntry(self):
		#create blank entry for demonstration purposes
		dummyEntry = self.tree.insert("","end",text='New',values=('','','','','','','','',''))
		self.tree.selection_set(dummyEntry)
		self.selectedpk="New"
		print self.selectedpk

	def delete(self):
		if self.selectedpk!=0:
			print self.app.deleteCashReceipt(self.selectedpk)
		self.populateTree()
if __name__=="__main__":
	root = Tk()
	program = CashReceiptsWindow(root,None)
	program.mainloop()