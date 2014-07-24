from Tkinter import *
from ttk import *
from tkFont import Font
from windows import CashDisbursmentsWindow
from lib import notespreview
from notePreviewLines import *
from ScrolledFrame import *
from textable import *
from enumerateNotes import *
class PreviewPage(Frame,object):
	def __init__(self,parent,app,deletedVar,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.app=app
		self.parent=parent
		self.initUI()

	def initUI(self):
		self.mainFrame = VerticalScrolledFrame(self)
		self.mainFrame.pack(fill=BOTH,expand=1,side=TOP)
		self.noteChunk = NoteChunk(self.mainFrame.interior,self.app)
		self.noteChunk.pack(fill=BOTH,expand=1,side=TOP)

	def populateTree(self):
		self.noteChunk.update()
		

	def exportCallback(self):
		pass