from Tkinter import *
from ttk import *
from ttkcalendar import Calendar
import calendar
from lib.timeFuncs import *
from supercombobox import SuperComboBox
import datetime

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
		fMain = Frame(self,borderwidth="2px",relief="groove")
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



		self._calButton=calButton = Button(fLower,text="...",command=self.createCalendar,width=2)
		calButton.pack(side=RIGHT,fill=X,expand=0)

		years = range(1990,2030)
		self._yearField = SuperComboBox(fLower,values=years,justify=CENTER,state='readonly')
		self._yearField.pack(side=LEFT,fill=X,expand=1)

		# months=("January","February","March","April","May","June","July","August",
		# 	"September","October","November","December")
		#months = range(1,13)
		self.months = months = ("","January","February","March","April","May","June","July","August",
			"Semptember","October","November","December")
		self._monthField = SuperComboBox(fLower,values=months,justify=CENTER,state='readonly')
		self._monthField.pack(side=LEFT,fill=X,expand=1)

		days = range(1,32)
		self._dayField = SuperComboBox(fLower,values=days,justify=CENTER,state='readonly')
		self._dayField.pack(side=LEFT,fill=X,expand=1)

		self._yearField.set(datetime.datetime.now().year)
		self._monthField.set(months[datetime.datetime.now().month])
		self._dayField.set(datetime.datetime.now().day)

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
		self.text = (str(date.year)+"-"+str(self.months[date.month])+"-"+str(date.day))
		#self._calButton.config(text=str(date.year)+"-"+str(date.month)+"-"+str(date.day))
		self._calWindow.destroy()
		self._calendarCreated-=1

	@property
	def text(self):
		if self._yearField.get()=="" or self._monthField.get()=="" or self._dayField.get()=="":
			return ""
		return str(self._yearField.get())+"-"+str(self.months.index(self._monthField.get()))+"-"+str(self._dayField.get())
	@text.setter
	def text(self, value):
		year,month,day=("","","")
		if len(value.split("-"))==3:
			year,month,day = value.split("-")
		self._yearField.set(year)
		if month=="":
			month = 0
		self._monthField.set(self.months[int(month)])
		self._dayField.set(day)
	
	def bind(self,evt,cb):
		for i in [self._monthField,self._dayField,self._yearField]:
			i.bind(evt,cb)

if __name__=="__main__":
	root=Tk()
	app = CalendarBox(root)
	app.pack()
	app.mainloop()

