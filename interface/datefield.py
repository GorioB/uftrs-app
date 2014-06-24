from Tkinter import *
from ttk import *
from ttkcalendar import Calendar
import calendar
from lib.timeFuncs import *

class CalendarBox(Frame,object):
	def __init__(self,parent,label="Label",toolTip=None,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.parent=parent
		self.label=label
		self._calendarCreated=0
		self.toolTip=toolTip
		self.initUI()

	def initUI(self):
		s = Style()
		s.configure("ToolTip.TLabel",background="yellow")

		#frames
		fMain = Frame(self.parent,borderwidth="2px",relief="groove")
		fMain.pack(fill=X,expand=1)

		fHigher = Frame(fMain)
		fLower = Frame(fMain)
		fHigher.pack(fill=X,expand=1,side=TOP)
		fLower.pack(fill=BOTH,expand=1,side=BOTTOM)

		fHigh_High=Frame(fHigher)
		self.fHigh_Low=Frame(fHigher)
		fHigh_High.pack(fill=X,expand=1)
		fRight = Frame(fHigh_High)
		fLeft = Frame(fHigh_High)
		fRight.pack(fill=NONE,side=RIGHT,expand=0)
		fLeft.pack(side=LEFT,fill=X,expand=1)

		#elements
		label = Label(fLeft,text=self.label)
		label.pack(side=LEFT,fill=BOTH,expand=1)



		self._calButton=calButton = Button(fLower,text=secsToDay(getEpochTime()),command=self.createCalendar)
		calButton.pack(fill=X,expand=1)

		#toolTip
		if self.toolTip:
			button = Button(fRight,text="?",width=2)
			button.pack(fill=NONE,expand=0)
			button.bind("<Enter>",self.hoverHelp)
			button.bind("<Leave>",self.leaveHelp)
			self.tooltipLabel = Label(self.fHigh_Low,text=self.toolTip,style="ToolTip.TLabel")
			self.tooltipLabel.pack(fill=X,expand=1)

	def hoverHelp(self,event):
		self.fHigh_Low.pack(fill=X,expand=1,side=TOP)

	def leaveHelp(self,event):
		self.fHigh_Low.pack_forget()

	def createCalendar(self):
		if not self._calendarCreated:
			self._calWindow=calWindow = Toplevel()
			calWindow.title("Calendar")
			calWindow.protocol("WM_DELETE_WINDOW",self.deleteCallback)
			self._ttkcal = ttkcal = Calendar(calWindow,firstweekday=calendar.SUNDAY)
			ttkcal.pack(expand=1,fill='both')
			ttkcal._calendar.bind("<ButtonPress-1>",self.calPressed,add="+")
			self._calendarCreated+=1


	def deleteCallback(self):
		self._calendarCreated-=1
		self._calWindow.destroy()
		
	def calPressed(self,event):
		date= self._ttkcal.selection
		self._calButton.config(text=str(date.year)+"-"+str(date.month)+"-"+str(date.day))
		self._calWindow.destroy()
		self._calendarCreated-=1

	@property
	def text(self):
	    return self._calButton.config('text')[-1]
	@text.setter
	def text(self, value):
	    self._calButton.config(text=value)
	

if __name__=="__main__":
	root=Tk()
	app = CalendarBox(root)
	app.mainloop()

