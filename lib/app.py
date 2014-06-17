# App Class
# 	User _activeUser
# 	createUser(username,password,isRoot)
# 	changePass(username,oldpassword,newpassword)
# 	login(username,password)
# 	exportExcel(entryList)
# 	printStatement()

# 	Either generates a pdf file or directly accesses the printer. See references and design documents for format.
# 	newCashReceipt(**kwargs)
# 	editCashReceipt()
# 	listCashReceipts() 

# 		and so on
# 	listOptions(identifier)
# 	searchOption(identifier, option)
# 	addOption(identifier, option)
# 	removeOption(identifier, option)

import db2
from models import *
import timeFuncs
class App(object):
	"""Main app class that exposes methods for the GUI module to access"""
	def __init__(self):
		self._activeUser = db2.User("dummy", "dummy")

	def createUser(self, username, password, isRoot):
		"""Creates a new user if username isn't taken, otherwise returns -1. isRoot value should be 0 or 1"""
		if db2.User.userExists(username):
			return -1
		else:
			newUser = db2.User(username, password)
			newUser.saveUser(isRoot)

	def changePass(self, username, oldpassword, newpassword):
		"""Changes the user's password if username-oldpassword combo is valid."""
		if db2.User(username, oldpassword).auth():
			changedUser = db2.User(username, newpassword)
			if changedUser.checkIfRoot():
				changedUser.saveUser(1)
			else:
				changedUser.saveUser(0)
		else:
			return -1

	def login(self, username, password):
		"""Returns true if the username-password combination is valid"""
		self._activeUser = db2.User(username, password)
		return self._activeUser.auth()

	def listOptions(self, identifier):
		"""Returns a list of options (list of strings) for the given identifier e.g. 'payors'"""
		return db2.DropDownMenu(identifier).getOptions()

	def searchOption(self, identifier, option):
		"""Returns a list of options (list of strings) that can complete the passed option"""
		return db2.DropDownMenu(identifier).searchOption(option)

	def addOption(self, identifier, option):
		"""Adds an option to the list of options"""
		db2.DropDownMenu(identifier).addOption(option)

	def removeOption(self, identifier, option):
		"""Removes an option from the list of options"""
		db2.DropDownMenu(identifier).removeOption(option)

	#DB API FUNCTIONS
	#NEW
	def newCashReceipt(self,dateOfTransaction,category,nature,
		amount,payor,receiptNumber,notes):
		c = CashReceipt(dateOfTransaction=dateOfTransaction,
			category=category,nature=nature,
			amount=amount,payor=payor,receiptNumber=receiptNumber,notes=notes,
			timestamp=timeFuncs.getEpochTime())
		if c.save(): return 1
		cf = CashFlow(source=c.identifier+":"+str(c.pk))
		if cf.save(): return 1
		return 0

	def newCashDisbursment(self,dateOfTransaction,category,event,purpose,nature,
		amount,liquidatingPerson,docNo,notes):
		cd = CashDisbursment(dateOfTransaction=dateOfTransaction,category=category,
			event=event,purpose=purpose,nature=nature,amount=amount,liquidatingPerson=liquidatingPerson,
			docNo=docNo,notes=notes,timestamp=timefuncs.getEpochTime())

		if cd.save():return 1
		return 0

	def newOAL(self,**kwargs):
		pass

	def newOME(self,dateOfTransaction,purpose,nature,amount,liquidatingPerson,receiptNumber,notes):
		ome = OME(dateOfTransaction=dateOfTransaction,
			purpose=purpose,
			nature=nature,
			amount=amount,
			liquidatingPerson=liquidatingPerson,
			receiptNumber=receiptNumber,
			notes=notes,
			timestamp=timeFuncs.getEpochTime())
		if ome.save():return 1
		cf = CashFlow(source=ome.identifier+":"+str(ome.pk))
		if cf.save(): return 1
		return 0

	def newNote(self,noteType,noteNumber,dateOfTransaction=None,purpose=None,nature=None,amount=None,liquidatingPerson=None,docNo=None,notes=None,event=None,flowDirection=None,description=None):
		if noteType=='odn':
			note = ODNote(timestamp=timeFuncs.getEpochTime(),
				description=description,noteNumber=noteNumber)
			note.save()
		elif noteType=='lti':
			note = LTINote(timestamp=timeFuncs.getEpochTime(),dateOfTransaction=dateOfTransaction,
				purpose=purpose,
				nature=nature,
				amount=amount,
				liquidatingPerson=liquidatingPerson,
				docNo=docNo,
				notes=notes,
				noteNUmber=noteNumber)
			if note.save(): return 1
			cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber)
			if cv.save(): return 1
		elif noteType=='oo':
			note = OONote(timestamp=timeFuncs.getEpochTime(),dateOfTransaction=dateOfTransaction,
				purpose=purpose,
				nature=nature,
				amount=amount,
				liquidatingPerson=liquidatingPerson,
				docNo=docNo,
				notes=notes,
				noteNumber=noteNumber)
			if note.save(): return 1
			cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber)
			if cf.save(): return 1
		elif noteType=='cocp':
			note = COCPNote(timestamp=timeFuncs.getEpochTime(),
				dateOfTransaction=dateOfTransaction,
				event=event,
				flowDirection=flowDirection,
				purpose=purpose,
				nature=nature,
				amount=amount,
				liquidatingPerson=liquidatingPerson,
				docNo=docNo,
				notes=notes,
				noteNumber=noteNumber)
			if note.save(): return 1
			if flowDirection=="Outflow":
				cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber)
			else:
				cfList = listEntries(CashFlow)
				inflowHit = [i for i in cfList if i.getContents().nature.content==note.nature.content]
				if inflowHit:
					inflowHit=inflowHit[0]
					inflowHit.addField("TEXT",note=inflowHit.note.content+','+str(noteNumber).strip(","))
					inflowHit.save()
		else:
			return 1
		return 0

	#EDIT
	def editCashReceipt(self,**kwargs):
		pass
	def editCashDisbursment(self,**kwargs):
		pass
	def editOAL(self,**kwargs):
		pass
	def editOME(self,**kwargs):
		pass
	def editNote(self,**kwargs):
		pass
	def editCashflow(self,**kwargs):
		pass
	#LIST
	def listCashReceipts(self,**kwargs):
		pass
	def listCashDisbursments(self,**kwargs):
		pass
	def listOALs(self,**kwargs):
		pass
	def listOMEs(self,**kwargs):
		pass
	def listNotes(self,**kwargs):
		pass
	def listCashflows(self,**kwargs):
		pass
