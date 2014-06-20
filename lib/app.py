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
		cf = CashFlow(source=c.identifier+":"+str(c.pk),timestamp=timeFuncs.getEpochTime())
		return cf.save()

	def newCashDisbursment(self,dateOfTransaction,category,event,purpose,nature,
		amount,liquidatingPerson,docNo,notes):
		cd = CashDisbursment(dateOfTransaction=dateOfTransaction,category=category,
			event=event,purpose=purpose,nature=nature,amount=amount,liquidatingPerson=liquidatingPerson,
			docNo=docNo,notes=notes,timestamp=timeFuncs.getEpochTime())

		return cd.save()

	def newOAL(self,OALType,details,category=None):
		oal= OAL(timestamp=timeFuncs.getEpochTime(),
			OALType=OALType,
			details=details,
			category=categor)
		return oal.save()

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
		cf = CashFlow(source=ome.identifier+":"+str(ome.pk),timestamp = timeFuncs.getEpochTime())
		if cf.save(): return 1
		return 0

	def newNote(self,noteType,noteNumber,dateOfTransaction=None,purpose=None,nature=None,amount=None,liquidatingPerson=None,docNo=None,notes=None,event=None,flowDirection=None,description=None):
		if noteType=='od':
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
				noteNumber=noteNumber)
			if note.save(): return 1
			cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber,timestamp=timeFuncs.getEpochTime())
			if cf.save(): return 1
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
			cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber,timestamp=timeFuncs.getEpochTime())
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
				cf = CashFlow(source=note.identifier+":"+str(note.pk),note=noteNumber,timestmap=timeFuncs.getEpochTime())
			else:
				cfList = listEntries(CashFlow)
				inflowHit = [i for i in cfList if i.getContents().nature.content==note.nature.content]
				if inflowHit:
					inflowHit=inflowHit[0]
					inflowHit.addField("TEXT",note=(inflowHit.note.content+','+str(noteNumber)).strip(","))
					inflowHit.save()
		else:
			return 1
		return 0

	#EDIT
	def _getCashFlow(model,pk):
		return [i for i in listEntries(CashFlow) if i.source.content==model.identifier+":"+pk]


	def _editEntry(self,model,pk,**kwargs):
		m = getEntry(pk,model)
		m.delete()
		oldpk=m.pk
		m.pk=0
		m.addField("TEXT",remarks=(str(m.remarks.content)+";Edited from: "+str(oldpk)).strip(';')+";",status="")
		m.addField("INTEGER",timestamp=timeFuncs.getEpochTime())
		for key,value in kwargs.items():
			setattr(m,key,DataField("TEXT",value))
		if m.save(): return (-1,-1)
		return oldpk,m.pk

	def editCashReceipt(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(CashReceipt,pk,**kwargs)
		if oldpk+newpk==-2:
			return 1
		cashFlows = self._getCashFlow(CashReceipt,pk)
		for cashFlow in cashFlows:
			cashFlow.addField("TEXT",source="cashreceipt:"+str(newpk))
			return cashFlow.save()

		return 0

	def editCashDisbursment(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(CashDisbursment,pk,**kwargs)
		return oldpk+newpk==-2

	def editOAL(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(OAL,pk,**kwargs)
		return oldpk+newpk==-2

	def editOME(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(OME,pk,**kwargs)
		cashFlows = self._getCashFlow(OME,pk)
		for cashFlow in cashFlows:
			cashFlow.addField("TEXT",source="ome:"+str(newpk))
			return cashFlow.save()
		return 0

	def editNote(self,notetype,pk,**kwargs):
		modelOptions={'od':ODNote,'lti':LTINote,'cocp':COCPNote,'oo':OONote}
		if 'noteNumber' in kwargs.keys():
			note = getEntry(pk,modelOptions[notetype])
			oldNoteNumber = note.noteNumber.content
			cashFlowList = [i for i in listEntries(CashFlow) if oldNoteNumber in i.note.content]
			for i in cashFlowList:
				i.addField("TEXT",note=i.note.content.replace(oldNoteNumber,kwargs['noteNumber']))
				i.save()
		oldpk,newpk = self._editEntry(modelOptions['notetype'],pk,**kwargs)
		cashFlowList = [i for i in listEntries(CashFlow) if i.source.content==notetype+"note:"+str(oldpk)]
		for i in cashFlowList:
			i.addField("TEXT",source=notetype+":"+str(newpk))
			i.save()
		return 0

	def editCashflow(self,pk,**kwargs):
		oldpk,newpk=self._editEntry(CashFlow,pk,**kwargs)
		return oldpk+newpk==-2

	#LIST
	def _listGeneral(self,model,showDeleted=False):
		if not showDeleted:
			return [i for i in listEntries(model) if i.status.content!="DELETED"]
		else:
			return listEntries(model)

	def listCashReceipts(self,showDeleted=False):
		return self._listGeneral(CashReceipt,showDeleted)

	def listCashDisbursments(self,showDeleted=False):
		return self._listGeneral(CashDisbursment,showDeleted)

	def listOALs(self,showDeleted=False):
		return self._listGeneral(OAL,showDeleted)

	def listOMEs(self,showDeleted=False):
		return self._listGeneral(OME,showDeleted)

	def listNotes(self,showDeleted=False):
		return self._listGeneral(COCPNote,showDeleted)+self._listGeneral(OONote,showDeleted)+self._listGeneral(OONote,showDeleted)+self._listGeneral(ODNote,showDeleted)

	def listCashflows(self,showDeleted=False):
		return self._listGeneral(CashFlow,showDeleted)

	#DELETE
	def deleteCashReceipt(self,pk):
		a = getEntry(pk,CashReceipt)
		cashFlows = self._getCashFlow(CashReceipt,pk)
		for i in cashFlows:
			i.delete()
		a.delete()
		return 0

	def deleteCashDisbursment(self,pk):
		a = getEntry(pk,CashDisbursment)
		a.delete()
		return 0

	def deleteOAL(self,pk):
		a = getEntry(pk,OAL)
		a.delete()
		return 0

	def deleteOME(self,pk):
		a = getEntry(pk,OME)
		cashFlows = self._getCashFlow(OME,pk)
		for i in cashFlows:
			i.delete()
		a.delete()
		return 0

	def deleteNote(self,notetype,pk):
		noteTypes={'od':ODNote,'lti':LTINote,'cocp':COCPNote,'oo':OONote}
		a = getEntry(pk,noteTypes[notetype])
		a.delete()
		notes = [i for i in self.listNotes(False) if i.noteNumber.content==a.noteNumber.content]
		if not notes:
			relatedCashFlows = [i for i in listEntries(CashFlow) if a.noteNumber.content in i.note]
			for i in relatedCashFlows:
				i.addField("TEXT",note=i.note.content.replace(a.noteNumber.content,'').replace(",,",','))
				i.save()