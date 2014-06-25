from Tkinter import *
from ttk import *

class ReadingBox(Frame,object):
	def __init__(self,parent,text="",height=5,scrollX=True,scrollY=False,**kwargs):
		Frame.__init__(self,parent,**kwargs)
		self.parent=parent
		upperFrame = Frame(self.parent)
		self.outputArea = Text(upperFrame,height=height,background='grey')
		if scrollX:
			self.outputArea.configure(wrap="none")
			xScroll = Scrollbar(self.parent,orient="horizontal",command=self.outputArea.xview)
			self.outputArea.configure(xscroll=xScroll.set)
			xScroll.pack(side=BOTTOM,fill=X,expand=0)
		if scrollY:
			yScroll= Scrollbar(upperFrame,orient="vertical",command=self.outputArea.yview)
			self.outputArea.configure(yscroll=yScroll.set)
			yScroll.pack(side=LEFT,fill=Y,expand=0)

		self.outputArea.pack(side=TOP,fill=BOTH,expand=1)
		self.outputArea.insert('1.0',text)
		self.outputArea.configure(state='disabled')
		upperFrame.pack(side=TOP,fill=BOTH,expand=1)

if __name__=="__main__":
	root = Tk()
	app = ReadingBox(root,text="This is a test of the readingbox's capabilities.")
	app.mainloop()