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
from db import *
import timeFuncs
class App(object):
	"""Main app class that exposes methods for the GUI module to access"""
	def __init__(self):
		self._activeUser = db2.User("dummy", "dummy")
		self._initTables()

	def isAdmin(self):
		"""AKA isRoot. Returns True if the app instance's active user is an admin/root"""
		return self._activeUser.checkIfRoot()

	def listOptions(self, identifier):
		"""Returns a list of options (list of strings) for the given identifier e.g. 'payors'"""
		return db2.DropDownMenu(identifier).getOptions()

	def listDropDownIdentifiers(self):
		return db2.DropDownMenu.getIdentifiers()

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
	#initTables
	def _initTables(self):
		for i in [BalanceInfo,CashReceipt,CashDisbursment,OAL,OME,COCPNote,OONote,LTINote,ODNote,AppProperty,CashFlow]:
			a = i()
			a.createTable()	
	#NEW
	def newCashReceipt(self,**kwargs):
		c = CashReceipt(**kwargs)
		if c.save(): return 1
		cf = CashFlow(source=c.identifier+":"+str(c.pk.content))
		return cf.save()

	def newCashDisbursment(self,**kwargs):
		return CashDisbursment(**kwargs).save()


	def newOAL(self,**kwargs):
		return OAL(**kwargs).save()

	def newOME(self,**kwargs):
		ome = OME(**kwargs)
		if ome.save():return 1
		cf = CashFlow(source=ome.identifier+":"+str(ome.pk.content))
		if cf.save(): return 1
		return 0

	def newNote(self,noteType,noteNumber,**kwargs):
		if noteType=='ODNote':
			note = ODNote(noteNumber=noteNumber,**kwargs)
			note.save()
		elif noteType=='LTINote':
			note = LTINote(noteNumber=noteNumber,**kwargs)
			if note.save(): return 1
			cf = CashFlow(source=note.identifier+":"+str(note.pk.content),note=noteNumber)
			if cf.save(): return 1
		elif noteType=='OONote':
			note = OONote(noteNumber=noteNumber,**kwargs)
			if note.save(): return 1
			cf = CashFlow(source=note.identifier+":"+str(note.pk.content),note=noteNumber)
			if cf.save(): return 1
		elif noteType=='COCPNote':
			note = COCPNote(noteNumber=noteNumber,**kwargs)
			if note.save(): return 1
			flowDirection=kwargs['flowDirection']
			sameEventNotes = [i for i in self._listGeneral(COCPNote) if i.event.content==kwargs['event']]
			for i in sameEventNotes:
				pointingCashFlows = [j for j in self.listCashflows(False) if i.noteNumber.content in j.note.content]
				for k in pointingCashFlows:
					k.note.set(k.note.content.replace(i.noteNumber.content,noteNumber))
					k.save()
				i.noteNumber.content=noteNumber
				i.save()

			if flowDirection=="Outflow":
				cf = CashFlow(source=note.identifier+":"+str(note.pk.content),note=noteNumber)
				cf.save()
			else:
				cfList = listEntries(CashFlow)
				if cfList:
					inflowHit = [i for i in cfList if i.getContents().nature.content==note.nature.content]
					for i in inflowHit:
						i.note.set((i.note.content+","+str(noteNumber)).strip(","))
						#inflowHit.addField("TEXT",note=(inflowHit.note.content+','+str(noteNumber)).strip(","))
						i.save()
		else:
			return 1
		return 0

	def getNoteNumber(self,key):
		COCPNotes= [i for i in self.listNotes(showDeleted=True) if i.__class__==COCPNote]
		for i in COCPNotes:
			if i.event.content==key:
				return i.noteNumber.content

		if key=="LTINote":
			LTINotes = [i for i in self.listNotes(showDeleted=True) if i.__class__==LTINote]
			for i in LTINotes:
				return i.noteNumber.content
		elif key=="OONote":
			OONotes = [i for i in self.listNotes(showDeleted=True) if i.__class__==OONote]
			for i in OONotes:
				return i.noteNumber.content

		notenumbers =[int(i.noteNumber.content) for i in self.listNotes(showDeleted=True)]
		notenumbers.sort()
		if notenumbers:
			return (notenumbers[-1])+1
		return 1


	#EDIT
	def _getCashFlow(self,model,pk):
		return [i for i in listEntries(CashFlow) if i.source.content==model.__name__+":"+str(pk)]


	def _editEntry(self,model,pk,**kwargs):
		m = getEntry(pk,model)
		if not m:
			return -1,-1
		m.delete()
		oldpk=m.pk.content
		m.pk.set(0)
		m.remarks.set("Edited from:"+str(oldpk))
		#m.addField("TEXT",remarks=(str(m.remarks.content)+";Edited from: "+str(oldpk)).strip(';')+";",status="")
		#m.addField("INTEGER",timestamp=timeFuncs.getEpochTime())
		m.status.set("")
		m.timestamp.set(timeFuncs.getEpochTime())
		for key,value in kwargs.items():
			setattr(m,key,DataField("TEXT",value))
		if m.save(): return (-1,-1)
		return oldpk,m.pk.content

	def editCashReceipt(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(CashReceipt,pk,**kwargs)
		if oldpk+newpk==-2:
			return newpk
		cashFlows = self._getCashFlow(CashReceipt,pk)
		for cashFlow in cashFlows:
			cashFlow.source.set("CashReceipt:"+str(newpk))
			#cashFlow.addField("TEXT",source="cashreceipt:"+str(newpk))
			return cashFlow.save()

		return newpk
	def editCashDisbursment(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(CashDisbursment,pk,**kwargs)
		return newpk

	def editOAL(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(OAL,pk,**kwargs)
		return newpk

	def toggleOAL(self,pk,tog):
		oal = getEntry(pk,OAL)
		oal.includeInStatement.content=tog
		oal.save()

	def editOME(self,pk,**kwargs):
		oldpk,newpk = self._editEntry(OME,pk,**kwargs)
		cashFlows = self._getCashFlow(OME,pk)
		for cashFlow in cashFlows:
			cashFlow.source.set("OME:"+str(newpk))
			#cashFlow.addField("TEXT",source="ome:"+str(newpk))
			return cashFlow.save()
		return newpk

	def editNote(self,notetype,pk,**kwargs):
		modelOptions={'ODNote':ODNote,'LTINote':LTINote,'COCPNote':COCPNote,'OONote':OONote}
		if 'noteNumber' in kwargs.keys():
			note = getEntry(pk,modelOptions[notetype])
			oldNoteNumber = note.noteNumber.content
			if notetype=="COCPNote":
				event = note.event.content
				sameEventNotes = [i for i in self._listGeneral(COCPNote) if i.event.content==event]
				for i in sameEventNotes:
					i.noteNumber.content=kwargs['noteNumber']
					i.save()
				cashFlowList = [i for i in listEntries(CashFlow) if oldNoteNumber in i.note.content]
				for i in cashFlowList:
					i.note.set(i.note.content.replace(oldNoteNumber,kwargs['noteNumber']))
					i.save()
			else:
				numbersList = [i for i in self.listNotes(False) if i.noteNumber.content==oldNoteNumber and i.identifier==notetype]
				if len(numbersList)==1:
					cashFlowList = [i for i in listEntries(CashFlow) if oldNoteNumber in i.note.content and notetype in i.source.content]
					for i in cashFlowList:
						i.note.set(i.note.content.replace(oldNoteNumber,kwargs['noteNumber']))
						#i.addField("TEXT",note=i.note.content.replace(oldNoteNumber,kwargs['noteNumber']))
						i.save()
		oldpk,newpk = self._editEntry(modelOptions[notetype],pk,**kwargs)
		cashFlowList = [i for i in listEntries(CashFlow) if i.source.content==notetype+":"+str(oldpk)]
		for i in cashFlowList:
			i.source.set(notetype+":"+str(newpk))
			#i.addField("TEXT",source=notetype+":"+str(newpk))
			i.save()
		return newpk

	def editCashflow(self,pk,**kwargs):
		oldpk,newpk=self._editEntry(CashFlow,pk,**kwargs)
		return newpk

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
		return self._listGeneral(COCPNote,showDeleted)+self._listGeneral(LTINote,showDeleted)+self._listGeneral(OONote,showDeleted)+self._listGeneral(ODNote,showDeleted)

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
		noteTypes={'ODNote':ODNote,'LTINote':LTINote,'COCPNote':COCPNote,'OONote':OONote}
		a = getEntry(pk,noteTypes[notetype])
		a.delete()
		cashFlows = self._getCashFlow(noteTypes[notetype],pk)
		for i in cashFlows:
			i.delete()
		notes = [i for i in self.listNotes(showDeleted=False) if i.noteNumber.content==a.noteNumber.content]
		if not notes:
			relatedCashFlows = [i for i in listEntries(CashFlow) if a.noteNumber.content in i.note.content]
			for i in relatedCashFlows:
				i.note.set(i.note.content.replace(a.noteNumber.content,'').replace(",,",','))
				if i.note.content==",":
					i.note.set("")
				#i.addField("TEXT",note=i.note.content.replace(a.noteNumber.content,'').replace(",,",','))
				i.save()

	def getStatementNotes(self):
		cashFlowList = self.listCashflows(showDeleted=False)
		cashFlowList = filterDOT(self,cashFlowList)
		noteNums = sorted(list(set(reduce(list.__add__,[i.note.content.split(",") for i in cashFlowList if i.note.content!=''],[]))),key=lambda el: int(el))
		relevantNotes = [i for i in self.listNotes() if i.noteNumber.content in noteNums]
		return relevantNotes

	def getBalanceInfo(self):
		bi = getEntry(1,BalanceInfo)
		if bi:
			return bi
		return None

	def updateBalanceInfo(self,**kwargs):
		bi = BalanceInfo(pk=1,**kwargs)
		bi.save()
		return 1
	#properties
	@property
	def timeFrame(self):
		tFrame = [i for i in listEntries(AppProperty) if i.label.content=="timeStart"]+[i for i in listEntries(AppProperty) if i.label.content=="timeEnd"]
		if len(tFrame)==2:
			return (int(tFrame[0].value.content),int(tFrame[1].value.content))
		else:
			return (0,0)
		return 0

	@timeFrame.setter
	def timeFrame(self,timeRange):
		tStart = self.getProperty("timeStart")
		tEnd = self.getProperty("timeEnd")
		startPK=0
		endPK=0
		if tStart!=1:
			startPK = tStart.pk.content
		if tEnd!=1:
			endPK = tEnd.pk.content
		tStart = AppProperty(pk=startPK,label="timeStart",value=timeRange[0]).save()
		tEnd = AppProperty(pk=endPK,label="timeEnd",value=timeRange[1]).save()

	def getProperty(self,label):
		propList = [i for i in listEntries(AppProperty) if i.label.content==label]
		if propList:
			return propList[0]
		else:
			return 1

	def getOAL(self,pk):
		return getEntry(pk,OAL)

	@property
	def councilName(self):
		cn = [i for i in listEntries(AppProperty) if i.label.content=="councilName"]
		if cn:
			return cn[0].value.content
		else:
			return ""

	@councilName.setter
	def councilName(self, value):
		cn = self.getProperty("councilName")
		if cn!=1:
			pk=cn.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="councilName",value=value).save()

	@property
	def cashOnHand(self):
		coh = self.getProperty("cashOnHand")
		if coh==1:
			return ""
		return coh.value.content

	@cashOnHand.setter
	def cashOnHand(self, value):
		coh = self.getProperty("cashOnHand")
		if coh!=1:
			pk=coh.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="cashOnHand",value=value).save()

	@property
	def cashInBank(self):
		cib = self.getProperty("cashInBank")
		if cib==1:
			return ""
		return cib.value.content

	@cashInBank.setter
	def cashInBank(self, value):
		cib = self.getProperty("cashInBank")
		if cib!=1:
			pk = cib.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="cashInBank",value=value).save()

	@property
	def preparedBy(self):
		cib = self.getProperty("preparedBy")
		if cib==1:
			return ""
		return cib.value.content

	@preparedBy.setter
	def preparedBy(self, value):
		cib = self.getProperty("preparedBy")
		if cib!=1:
			pk = cib.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="preparedBy",value=value).save()

	@property
	def notedBy(self):
		cib = self.getProperty("notedBy")
		if cib==1:
			return ""
		return cib.value.content

	@notedBy.setter
	def notedBy(self, value):
		cib = self.getProperty("notedBy")
		if cib!=1:
			pk = cib.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="notedBy",value=value).save()
	
	@property
	def balance(self):
		balance = self.getProperty("balance")
		if balance==1:
			return (0,0)
		else:
			return (int(balance.value.content.split(":")[0]),float(balance.value.content.split(":")[1]))

	@balance.setter
	def balance(self, value):
		#value should be in the format (secondsFromEpoch,integer value)
		balance = self.getProperty("balance")
		if balance!=1:
			pk = balance.pk.content
		else:
			pk=0

		AppProperty(pk=pk,label="balance",value=value).save()

def filterDOT(app,flowList):
	start,end = app.timeFrame
	f = [i for i in flowList if int(i.getContents().dateOfTransaction.content)>=int(start)]
	return [i for i in f if int(i.getContents().dateOfTransaction.content)<=int(end)]