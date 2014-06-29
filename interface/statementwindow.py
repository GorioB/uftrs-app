from Tkinter import *
from ttk import *
<<<<<<< Updated upstream
from tkFont import Font

class StatementWindow(Frame,object):
	def __init__(self,parent,app,deletedVar,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.initUI()

	def initUI(self):
		self.headerField = Text(self,bd=0,width=0,state='disabled',height=3)
		self.headerField.tag_configure("center",justify="center")
		f = Font(self.headerField,self.headerField.cget('font'))
		f.configure(weight='bold')
		self.headerField.configure(font=f)
		self.headerField.pack(fill=X,expand=1)

	def populateTree(self):
		self.headerField['state']='normal'
		self.headerField.insert('1.0',"UP School of Dinosaurs Student Council\nStatement of Cash Flows\nFor the Semester Ended Octber 31,2013")
		self.headerField.tag_add('center','1.0','end')
		self.headerField['state']='disabled'
		pass

if __name__=="__main__":
	root = Tk()
	app = StatementWindow(root,None,None)
	app.pack(fill=BOTH,expand=1)
	app.populateTree()
	app.mainloop()
=======
from textable import TextTable
from ScrolledFrame import VerticalScrolledFrame
from lib.floattostr import *

def indent(i=1):
	return "    "*i
class StatementWindow(Frame,object):
	def __init__(self,parent,app,deletedVar,**kwargs):
		Frame.__init__(self,parent)
		self.app = app
		self.deletedVar = deletedVar
		self.pack_propagate(0)
		vsf = VerticalScrolledFrame(self)
		vsf.pack(fill=BOTH,expand=1)
		weights = [2,1,1,1]
		anchors = ['left','center','right','right']
		self.lines=[]
		self.table = TextTable(vsf.interior,aligns=anchors,weights=weights)
		self.header = Text(vsf.interior,width=0,bd=0,height=3)
		self.header.pack(fill=BOTH,expand=1)
		self.header.tag_configure("center",justify="center")
		self.table.pack(fill=BOTH,expand=1)


	def populateTree(self):
		#fill header
		self.header.delete("1.0",'end')
		self.header.insert('1.0',"College of Dinosaurs Student Council\nStatement of Cash Flows\nFor the Semester Ended October 31, 2014")
		self.header.tag_add('center','1.0','end')
		self.header['state']='disabled'

		self.table.clear()
		self.lines=[]
		self.writeInflows()
		self.saveLines()

	def writeInflows(self):
		self.lines.append(['CASH INFLOWS','NOTE','',''])
		self.lines.append(['Council Mandated Funds','','',''])

		totalInflows=0

		cashFlowList = self.app.listCashflows(showDeleted=False)
		inflowList = [i for i in cashFlowList if i.source.content.split(":")[0]=="CashReceipt"]

		CMFList = [i for i in inflowList if i.getContents().category.content=="Council Mandated Funds"]

		natureTotals = self.getFlows(CMFList)
		totalInflows+=self.formatToLines(natureTotals)

		GSIList = [i for i in inflowList if i.getContents().category.content=="General Sponsorship Inflows"]
		
		self.lines.append(['General Sponsorship Inflows','','',''])
		totalInflows+=self.formatToLines(self.getFlows(GSIList))

		self.lines.append([indent(3)+"Total Inflows: ",'','','P'+floatToStr(totalInflows)])


	def formatToLines(self,totals):
		keys= totals.keys()
		keys.sort()
		localtotal=0
		for key in keys:
			self.lines.append([indent(1)+key,str(totals[key][1]),floatToStr(totals[key][0]),''])
			localtotal+=totals[key][0]

		self.lines.append([indent(2)+'Total','','','P'+floatToStr(localtotal)])
		return localtotal

	def saveLines(self):
		self.table.clear()
		for i in self.lines:
			self.table.addRow(i)

	def getFlows(self,catlist):
		natureTotals={}
		for i in catlist:
			name=i.getContents().nature.content
			amount = i.getContents().amount.content
			notes = i.note.content
			try:
				amount = float(amount)
			except:
				amount =0

			if name in natureTotals:
				natureTotals[name][0]+=amount
			else:
				natureTotals[name]=[amount]
				natureTotals[name].append(notes)

		return natureTotals

	def exportToExcel(self):
		pass
>>>>>>> Stashed changes
