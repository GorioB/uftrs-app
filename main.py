from lib.app import App
from interface import windows
from Tkinter import *
from ttk import *
from interface import windows2, windows
from interface import cashflowswindow
from interface.statementwindow import StatementWindow
import os
import datetime
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class MainProgram(Frame,object):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.app = App()
		self.pack()
		self.showDeleted=BooleanVar()
		self.showDeleted.set(0)
		self.initUI()

	def initUI(self):
		#Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("800x500")
		self.parent.state("zoomed")
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		#menu
		usersMenu=Menu(menubar)
		usersMenu.add_command(label="Create User")
		preferencesMenu=Menu(menubar)
		preferencesMenu.add_command(label="Export This Page to Excel",command=self.exportSelectedNote)
		preferencesMenu.add_command(label="Export All Pages to Excel", command=self.exportEverything)
		preferencesMenu.add_checkbutton(label="Show History",variable=self.showDeleted,onvalue=1,offvalue=0)
		preferencesMenu.add_command(label="Settings")
		menubar.add_cascade(label="User",menu=usersMenu)
		menubar.add_cascade(label="Options",menu=preferencesMenu)
		menubar.add_command(label="About",command=self.about)

		#notebook
		self.notebook = Notebook(self.parent)
		self.notes={}
		for i in ["Cash Receipts","Cash Disbursments","Cash Flows",
			"Other Assets and Liabilities","Notes",
			"Operation and Maintenance Expense","Statement of Cash Flows"]:
			self.notes[i]=Frame(self.notebook)
			self.notebook.add(self.notes[i],text=i)
		self.notebook.pack(fill=BOTH,expand=1)
		self.notebook.pack_propagate(0)

		#CashReceiptsWindow
		self.notes['Cash Receipts']=windows.CashReceiptsWindow(self.notes['Cash Receipts'],self.app,deletedVar = self.showDeleted)
		self.notes['Cash Receipts'].pack()
		self.notes['Cash Disbursments']=windows.CashDisbursmentsWindow(self.notes['Cash Disbursments'],self.app,deletedVar=self.showDeleted)
		self.notes['Cash Disbursments'].pack()
		self.notes['Operation and Maintenance Expense']=windows.OperationMaintenanceExpensesWindow(self.notes['Operation and Maintenance Expense'],self.app,deletedVar=self.showDeleted)
		self.notes['Operation and Maintenance Expense'].pack()

		self.notes['Other Assets and Liabilities']=windows2.OALWindow(self.notes['Other Assets and Liabilities'],self.app,deletedVar=self.showDeleted)
		self.notes['Other Assets and Liabilities'].pack()

		self.notes['Notes'] = windows2.NotesWindow(self.notes['Notes'],self.app,deletedVar=self.showDeleted)
		self.notes['Notes'].pack()

		self.notes['Cash Flows'] = cashflowswindow.CashFlowsWindow(self.notes['Cash Flows'],self.app,deletedVar=self.showDeleted)
		self.notes['Cash Flows'].pack()

		self.notes['Statement of Cash Flows'] = StatementWindow(self.notes['Statement of Cash Flows'],self.app,deletedVar=self.showDeleted)
		self.notes['Statement of Cash Flows'].pack(fill=BOTH,expand=1)

		self.notebook.bind("<<NotebookTabChanged>>",self.refreshPage)

	#callbacks
	def refreshPage(self,*a):
		selectedpage = self.notebook.select()
		tabName = self.notebook.tab(selectedpage,option="text")
		self.notes[tabName].populateTree()

	def about(self):
		pass

	def exportSelectedNote(self):
		noteName = self.notebook.tab(self.notebook.select(),"text")
		self.notes[noteName].exportToExcel()

	def exportEverything(self):
		excelBuilder = windows.ExcelBuilder()
		for i in ["Cash Receipts","Cash Disbursments","Cash Flows","Other Assets and Liabilities","Notes",
			"Operation and Maintenance Expense"]:
			self.notes[i].addSheet(excelBuilder)

		fileName = 'Everything_' + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y") + '.xls'
		excelBuilder.setFileName(fileName)

		excelBuilder.build()

if __name__=="__main__":
	root = Tk()
	app = MainProgram(root)
	if os.path.exists(os.path.join("assets","logo.gif")):
		img = PhotoImage(file=resource_path(os.path.join("assets","logo.gif")))
		root.tk.call('wm','iconphoto',root._w,img)
	app.mainloop()