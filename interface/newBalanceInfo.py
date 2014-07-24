from Tkinter import *
from ttk import *
from datefield import *
from textfield import *
from helpbox import *
from lib.floattostr import *
from lib.app import *

def cf(fields):
	keys = fields.keys()
	if 'notes' in keys:
		keys.remove("notes")
	if 'remarks' in keys:
		keys.remove("remarks")
	if 'timestmap' in keys:
		keys.remove("timestamp")
	for i in keys:
		if fields[i].text=="":
			createHelpBox("Please fill all fields")
			return 1

def center(win):
	win.update_idletasks()
	width = win.winfo_width()
	height=win.winfo_height()
	x = (win.winfo_screenwidth() // 2) - (width // 2)
	y = (win.winfo_screenheight() // 2) - (height // 2)
	win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class NewBalanceBox(Frame,object):
	def __init__(self,parent,app):
		Frame.__init__(self,parent)
		self.app = app
		self.parent=parent
		self.fields={}
		self.fields['oldTS']=oldTS = CalendarBox(self,label="Date and Time of Previous Balance")
		oldTS.pack(fill=X,expand=1)
		self.fields['newTS']=newTS = CalendarBox(self,label="Date and Time of New Balance")
		newTS.pack(fill=X,expand=1)

		self.fields['cashBalanceBox'] = TextFieldBox(self,label="Balance")
		self.fields['chairName'] = TextFieldBox(self,label="Chairperson's Name")
		self.fields['witName'] = TextFieldBox(self,label="Witness' Name")
		self.fields['witCouPos'] = TextFieldBox(self,label="Witness' Council Position",toolTip="Witness should be a council member but not the financial councilor.")
		self.fields['reason'] = TextFieldBox(self,label="Reason For Change")
		saveB = Button(self,text="Save",command=self.saveCB)
		saveB.pack(fill=X,expand=1)
		self.popFields()
	def saveCB(self,*a):
		if cf(self.fields):
			return 1
		if not self.app.isAdmin():
			createHelpBox("Only an Administrator Account can make this change.")
			return 1
		self.app.updateBalanceInfo(
			originalBalanceTimestamp=stringToSecs(self.fields['oldTS'].text+" 00:00:00"),
			revisedBalanceTimestamp=stringToSecs(self.fields['newTS'].text+" 00:00:00"),
			chairName = self.fields['chairName'].text,
			witnessName = self.fields['witName'].text,
			witnessPosition=self.fields['witCouPos'].text,
			reason = self.fields['reason'].text)
		self.app.balance=str(stringToSecs(self.fields['newTS'].text+" 0:0:0"))+":"+str(strToFloat(self.fields['cashBalanceBox'].text))
		self.popFields()
		self.parent.destroy()
	def popFields(self):
		b = self.app.getBalanceInfo()
		if b:
			self.fields['oldTS'].text=secsToDay(b.originalBalanceTimestamp.content)
			self.fields['newTS'].text=secsToDay(b.revisedBalanceTimestamp.content)
			self.fields['chairName'].text=b.chairName.content
			self.fields['witName'].text = b.witnessName.content
			self.fields['witCouPos'].text = b.witnessPosition.content
			self.fields['reason'].text=b.reason.content
			self.fields['cashBalanceBox'].text=floatToStr(self.app.balance[1])
if __name__=="__main__":
	root=Tk()
	a = App()
	appl = NewBalanceBox(root,a)
	appl.pack(fill=BOTH,expand=1)
	appl.mainloop()