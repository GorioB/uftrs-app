from lib.app import App
from lib.db2 import User, DropDownMenu
from interface.autocomplete import AutocompleteBox
from interface import textfield
from Tkinter import *
from ttk import *
from main import *
import os

class DropDownEditor(Frame,object):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.app = App()
		self.pack()

		# Window settings
		self.parent.title("UFTRS Accounting System")
		self.parent.geometry("360x500")
		self.initUI()

	def initUI(self):
		# Create identifier drop down menu
		self.identifierSelector = AutocompleteBox(self.parent, label="Select a drop-down menu to edit",toolTip = "placeholder")
		self.identifierSelector.initDropDown(self.app.listDropDownIdentifiers())
		self.identifierSelector.comboBox.bind('<<ComboboxSelected>>', self.handleIdentifierSelect)
		self.identifierSelector.pack()

		Label(self.parent).pack()

		# Create listbox widget
		listFrame = Frame(self.parent)
		scrollBar = Scrollbar(listFrame,orient=VERTICAL)
		self.optionsListBox = Listbox(listFrame, selectmode=SINGLE ,yscrollcommand=scrollBar.set)
		scrollBar.config(command=self.optionsListBox.yview)
		scrollBar.pack(side=RIGHT,fill=Y)
		self.optionsListBox.pack(side=LEFT,fill=BOTH,expand=1)
		listFrame.pack(fill=BOTH,expand=1)

		deleteButton = Button(self.parent, text="Delete selection entry", command=self.handleDeleteButton)
		deleteButton.pack()

		Label(self.parent, text="OR").pack()

		Label(self.parent, text="Add a new entry").pack()
		self.newOptionEntry = Entry(self.parent)
		self.newOptionEntry.pack()
		addButton = Button(self.parent, text="Add entry", command=self.handleAddButton)
		addButton.pack()

	def refreshList(self):
		identifier = self.identifierSelector.text
		options = self.app.listOptions(identifier)
		self.optionsListBox.delete(0, END)
		for option in options:
			self.optionsListBox.insert(END, option)

	def handleIdentifierSelect(self, *args):
		self.refreshList()

	def handleDeleteButton(self):
		selectedItems = self.optionsListBox.curselection()
		if len(selectedItems)==0:
			return

		isLastItem = False
		if int(selectedItems[0]) == self.optionsListBox.size()-1:
			isLastItem = True

		# Delete entry
		selectedEntry = self.optionsListBox.get(selectedItems[0])
		identifier = self.identifierSelector.text
		self.app.removeOption(identifier, selectedEntry)
		self.refreshList()

		# Select another entry
		if isLastItem:
			size = self.optionsListBox.size()
			self.optionsListBox.select_set(size - 1)
		else:
			self.optionsListBox.select_set(selectedItems[0])


	def handleAddButton(self):
		identifier = self.identifierSelector.text
		newEntry = self.newOptionEntry.get()
		if newEntry=="" or identifier=="":
			return
		self.app.addOption(identifier, newEntry)
		self.refreshList()


if __name__=="__main__":
	root = Tk()
	app = DropDownEditor(root)
	
	app.mainloop()