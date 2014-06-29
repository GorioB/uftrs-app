from Tkinter import *
from ttk import *
from tkFont import Font
from textable import TextTable
from lib.floattostr import *
from ScrolledFrame import VerticalScrolledFrame

def tab(n=1):
	return "    "*n
class StatementWindow(Frame,object):
	def __init__(self,parent,app,deletedVar,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.app = app
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.mainFrame = VerticalScrolledFrame(self)
		self.mainFrame.pack(fill=BOTH,expand=1,side=TOP)
		self.mainFrame = self.mainFrame.interior
		self.headerField = Text(self.mainFrame,bd=0,width=0,state='disabled',height=3)
		self.headerField.tag_configure("center",justify="center")
		f = Font(self.headerField,self.headerField.cget('font'))
		f.configure(weight='bold')
		self.headerField.configure(font=f)
		self.headerField.pack(fill=X,expand=1,side=TOP)

		self.cashFlowsText = TextTable(self.mainFrame,
			aligns=['left','left','right','right','right','right'],
			weights=[4,4,1,1,1,1],
			width=500)
		self.cashFlowsText.pack(expand=1,fill=BOTH,side=TOP)

	def populateTree(self):
		self.lines=[]
		self.headerField['state']='normal'
		self.headerField.delete('1.0','end')
		self.headerField.insert('1.0',"UP School of Dinosaurs Student Council\nStatement of Cash Flows\nFor the Semester Ended Octber 31,2013")
		self.headerField.tag_add('center','1.0','end')
		self.headerField['state']='disabled'

		self.lines.append([['CASH INFLOWS','Note','','','',''],[],[1,0,0,0,0,0]])
		cashFlowList = self.app.listCashflows(showDeleted=False)
		inflowList = [i for i in cashFlowList if i.source.content.split(":")[0]=="CashReceipt"]
		totalInflows=0
		self.firstInflow=0
		self.firstInflowTotal=0
		#replace with db stuff
		inflowTypeList = ['Council Mandated Funds','General Sponsorship Inflows','Income Generating Projects','Other Inflows']
		for inflowType in inflowTypeList:
			self.lines.append([[inflowType,'','','','',''],[],[]])
			partialList = [i for i in inflowList if i.getContents().category.content==inflowType]
			lines,partialTotal = self.getInflows(partialList)
			self.lines=self.lines+lines
			totalInflows+=partialTotal

		self.lines.append([[tab(3)+"Total Inflows",'','','','P',floatToStr(totalInflows)],[0,0,0,0,0,1],[]])
		self.commitLines(self.lines)
	def getInflows(self,flowList):
		partialTotals={}
		totalInflows=0
		for i in flowList:
			name = i.getContents().nature.content
			amount = i.getContents().amount.content
			notes = i.note.content
			try:
				amount = float(amount)
			except:
				amount=0
			totalInflows+=amount
			if name in partialTotals:
				partialTotals[name][0]+=amount
			else:
				partialTotals[name]=[amount]
				partialTotals[name].append(notes)
		newLines = self.writeLinesPartial(partialTotals)
		return newLines,totalInflows

	def writeLinesPartial(self,partialTotalsList):
		total=0
		partialTotalsKeys = partialTotalsList.keys()
		partialTotalsKeys.sort()
		tempLines=[]
		for i in partialTotalsKeys:
			name = i
			amount = partialTotalsList[i][0]
			notes = partialTotalsList[i][1]
			total+=amount
			tempLines.append([[tab()+name,notes,'',floatToStr(amount),'',''],[],[]])

		if tempLines:
			if not self.firstInflow:
				tempLines[0][0][2]="P"
				self.firstInflow=1
			tempLines[-1][1]=[0,0,0,1,0,0]
		# tempLines[0][0][2]="P"+tempLines[0][0][2]
		# tempLines[-1][1]=[0,0,1,0]
		tempLines.append([[tab(2)+"Total",'','','','',floatToStr(total)],[0,0,0,0,0,1],[]])
		if not self.firstInflowTotal:
			self.firstInflowTotal=1
			tempLines[-1][0][4]="P"
		return tempLines

	def commitLines(self,lines):
		self.cashFlowsText.clear()
		for i in lines:
			print i
			self.cashFlowsText.addRow(i[0],uls=i[1],bolds=i[2])


if __name__=="__main__":
	root = Tk()
	app = StatementWindow(root,None,None)
	app.pack(fill=BOTH,expand=1)
	app.populateTree()
	app.mainloop()