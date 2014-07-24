from db import *

class CashReceipt(DataEntry):
	dateOfTransaction = IntegerField()
	category = TextField()
	nature = TextField()
	amount = RealField()
	payor = TextField()
	receiptNumber = TextField()
	notes = TextField()

class CashDisbursment(DataEntry):
	dateOfTransaction = IntegerField()
	category = TextField()
	event = TextField()
	purpose = TextField()
	nature = TextField()
	amount = RealField()
	liquidatingPerson = TextField()
	docNo = TextField()
	notes = TextField()

class OAL(DataEntry):
	OALType = TextField()
	category = TextField()
	details = TextField()
	includeInStatement=TextField()

class OME(DataEntry):
	dateOfTransaction = IntegerField()
	purpose = TextField()
	nature = TextField()
	amount = RealField()
	liquidatingPerson = TextField()
	receiptNumber = TextField()
	notes = TextField()

class COCPNote(DataEntry):
	dateOfTransaction=IntegerField()
	event = TextField()
	flowDirection=TextField()
	purpose=TextField()
	nature=TextField()
	amount=RealField()
	liquidatingPerson=TextField()
	docNo=TextField()
	notes=TextField()
	noteNumber=TextField()

class OONote(DataEntry):
	dateOfTransaction=IntegerField()
	purpose=TextField()
	nature=TextField()
	amount=RealField()
	liquidatingPerson=TextField()
	docNo=TextField()
	notes=TextField()
	noteNumber=TextField()

class LTINote(DataEntry):
	dateOfTransaction=IntegerField()
	purpose=TextField()
	nature=TextField()
	amount=RealField()
	liquidatingPerson=TextField()
	docNo=TextField()
	notes=TextField()
	noteNumber=TextField()

class ODNote(DataEntry):
	includeInStatement=TextField()
	description=TextField()
	noteNumber=TextField()

class AppProperty(DataEntry):
	label=TextField()
	value=TextField()

class CashFlow(DataEntry):
	source =TextField()
	note=TextField()

	def getContents(self):
		MODELS_DICT={'CashReceipt':CashReceipt,
			'CashDisbursment':CashDisbursment,
			'OAL':OAL,'OME':OME,
			'COCPNote':COCPNote,'LTINote':LTINote,'ODNote':ODNote,'OONote':OONote,
			'AppProperty':AppProperty}
		if self.source:
			source=self.source.content.split(":")
			return getEntry(source[1],MODELS_DICT[source[0]])

class BalanceInfo(DataEntry):
	originalBalanceTimestamp=IntegerField()
	revisedBalanceTimestamp=IntegerField()
	chairName=TextField()
	witnessName=TextField()
	witnessPosition=TextField()
	reason=TextField()

if __name__=="__main__":
	for i in [CashReceipt,CashDisbursment,OAL,OME,COCPNote,OONote,LTINote,ODNote,AppProperty,CashFlow,BalanceInfo]:
		a = i()
		a.createTable()	