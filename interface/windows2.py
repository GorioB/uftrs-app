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

class OALWindow(CashDisbursmentsWindow):
	def initTree(self):
		self.tree = tree = Treeview(self.treeFrame,selectmode="browse")
		tree.bind("<<TreeviewSelect>>",self.getSelection)
		yscroll = Scrollbar(self.treeFrame,orient="vertical",command=tree.yview)
		xscroll = Scrollbar(self.xScrollFrame,orient="horizontal",command=tree.xview)
		self.colList = colList=["Timestamp","Type","Category","Details","Remarks"]
		tree['columns']=colList
		for i in colList:
			tree.heading(i,text=i)
			tree.column(i,anchor=W,width=60)
		tree.column("#0",width=0,anchor=W)
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

		self.fields[cn]['category']=AutocompleteBox(self.accountsOutstandingFrame,
			label="Category")
		options=["Payable","Receivable"] #Don't overwrite
		self.fields[cn]['category'].initDropDown(options)

		self.fields[cn]['details']=TextFieldBox(self.accountsOutstandingFrame,
			label="Description",height=5)

		helpfulMessage = ReadingBox(self.accountsOutstandingFrame,text="[Receivable]: Please indicate the amount, the payor's name, source of the receivable, and other pertinent data.\n\t(e.g. Receivable of P5,000.00 in cash from Company XYZ in accordance with the sponsorship agreement entered into last October 15, 2013. This is expected to increase the cash balance next month.)\n[Payable]: Please indicate the amount, the payee's name, source of the payable, and other pertinent data.\n\t(e.g. Payable of P500.00 in cash to Councilor A as reimbursement for purchase of office supplies. This is expected to decrease the cash balance in the following month.)",
			)

		for i in self.fields[cn]:
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage.pack(fill=BOTH,expand=1)

		#inventoriesAndOtherAssets
		cn='inventoriesAndOtherAssets'

		self.fields[cn]['timestamp'] = TextFieldBox(self.inventoriesAndOtherAssetsFrame,
			label="Timestamp",readonly=True,height=1)

		self.fields[cn]['details']=TextFieldBox(self.inventoriesAndOtherAssetsFrame,
			label="Details",height=5)
		helpfulMessage2 = ReadingBox(self.inventoriesAndOtherAssetsFrame,
			text="Please indicate the item in question, the amount, the source of the item, and other pertinent data.\n\t(e.g. Received X-deals from Company DEF. 200 black ballpens were received in good condition on October 20, 2013. These are expected to be given away as freebies during the general registration next semester.)\n\t(e.g. Received a brand-new projector from Company GHI in accordance with the sponsorship agreement entered into last August 24, 2013. The projector was received in good condition on September 12, 2013.)")

		for i in self.fields[cn]:
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage2.pack(fill=BOTH,expand=1)

		#others
		cn='others'
		self.fields[cn]['timestmap']=TextFieldBox(self.othersFrame,
			label="Timestamp",readonly=True,height=1)

		self.fields[cn]['category']=AutocompleteBox(self.othersFrame,
			label="Category")
		self.fields[cn]['category'].initComboBox(self.app.listOptions("OAL_Category"))

		self.fields[cn]['description']=TextFieldBox(self.othersFrame,
			label="Description",height=5)
		helpfulMessage3=ReadingBox(self.othersFrame,scrollX=False,
			text="Please indicate the item in question, the amount, the source of the item, and other pertinent data.")

		for i in self.fields[cn]:
			self.fields[cn][i].pack(side=TOP,fill=X,expand=1)
		helpfulMessage3.pack(side=TOP,fill=X,expand=1)
	def getSelection(self,event):
		pass

	def _populateTree(self,entryList):
		pass

	def populateTree(self,*a):
		pass

	def exportToExcel(self):
		pass

	def save(self):
		pass

