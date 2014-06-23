from Tkinter import *
from tk import *

class CashReceiptsWindow(Frame,object):
	def __init__(self,parent,app):
		Frame.__init__(self,parent)
		self.parent=parent
		self.app=app