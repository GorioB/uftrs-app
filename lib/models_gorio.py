from db_gorio import *
class CashReceipt(DataEntry):
	def __init__(self,dateOfTransaction=None,category=None,
		nature=None,amount=None,
		payor=None,receiptNumber=None,
		status=None,needsRoot=None,
		pk=0,timestamp=None,
		notes=None,remarks=None):
		DataEntry.__init__(self,identifier="cashreceipt",pk=pk,
			dateOfTransaction=dateOfTransaction,category=category,nature=nature,
			amount=amount,payor=payor,receiptNumber=receiptNumber,status=status,
			needsRoot=needsRoot,timestamp=timestamp,notes=notes,remarks=remarks)

		integerFields=["dateOfTransaction"]

		realFields=["amount"]

		[self._setFieldTypes("INTEGER",i) for i in integerFields]
		[self._setFieldTypes("REAL",i) for i in realFields]

class Disbursment(DataEntry):
	def __init__(self,timestamp=None,dateOfTransaction=None,category=None,
		event=None,purpose=None,nature=None,amount=None,liquidatingPerson=None,
		docNo=None,notes=None,remarks=None,pk=0):
		DataEntry.__init__(self,identifier="disbursment",pk=pk,timestamp=timestamp,
			dateOfTransaction=dateOfTransaction,category=category,
			event=event,purpose=purpose,nature=nature,amount=amount,liquidatingPerson=liquidatingPerson,
			docNo=docNo,notes=notes,remarks=remarks)

		integerFields=["dateOfTransaction"]
		realFields=["amount"]
		[self._setFieldTypes("INTEGER",i) for i in integerFields]
		[self._setFieldTypes("REAL",i) for i in realFields]

class OAL(DataEntry):
	def __init__(self,timestamp=None,OALType=None,category=None,details=None,pk=0):
		DataEntry.__init__(self,identifier="oal",timestamp=timestamp,OALType=OALType,category=category,details=details,pk=pk)

class OME(DataEntry):
	def __init__(self,timestamp=None,dateOfTransaction=None,purpose=None,nature=None,
		amount=None,liquidatingPerson=None,receiptNumber=None,notes=None,remarks=None,pk=0):
		DataEntry.__init__(self,identifier="ome",
			timestamp=timestamp,
			dateOfTransaction=dateOfTransaction,
			purpose=purpose,
			nature=nature,
			amount=amount,
			liquidatingPerson=liquidatingPerson,
			receiptNumber=receiptNumber,
			notes=notes,
			remarks=remarks,
			pk=pk)

		integerFields=["dateOfTransaction"]
		realFields=["amount"]
		[self._setFieldTypes("INTEGER",i) for i in integerFields]
		[self._setFieldTypes("REAL",i) for i in realFields]

class CashFlow(DataEntry):
	def __init__(self,source=None,note=None,pk=0):
		DataEntry.__init__(self,identifier="cashflow",
			pk=pk,
			source=source,
			note=note)

class COCPNote(DataEntry):
	def __init__(self,timestamp=None,pk=0,dateOfTransaction=None,event=None,
		flowDirection=None,purpose=None,nature=None,amount=None,liquidatingPerson=None,
		docNo=None,notes=None,remarks=None):
		DataEntry.__init__(self,identifier="cocpnote",
			pk=pk,
			timestamp=timestamp,
			dateOfTransaction=dateOfTransaction,
			event=event,
			flowDirection=flowDirection,
			purpose=purpose,
			nature=nature,
			amount=amount,
			liquidatingPerson=liquidatingPerson,
			docNo=docNo,
			notes=notes,
			remarks=remarks)

		integerFields=["dateOfTransaction"]
		realFields=['amount']
		[self._setFieldTypes("INTEGER",i) for i in integerFields]
		[self._setFieldTypes("REAL",i) for i in realFields]

class LTIOONote(DataEntry):
	def __init__(self,timestamp=None,pk=0,dateOfTransaction=None,purpose=None,
		nature=None,amount=None,liquidatingPerson=None,docNo=None,notes=None,remarks=None):
		DataEntry.__init__(self,identifier="ltioonote",
			pk=pk
			timestamp=timestamp,
			dateOfTransaction=dateOfTransaction,
			purpose=purpose,
			nature=nature,
			amount=amount,
			liquidatingPerson=liquidatingPerson,
			docNo=docNo,
			notes=notes,
			remarks=remarks)

		integerFields=["dateOfTransaction"]
		realFields=["amount"]
		[self._setFieldTypes("INTEGER",i) for i in integerFields]
		[self._setFieldTypes("REAL",i) for i in realFields]

class AppProperty(DataEntry):
	def __init__(self,pk=0,label=None,value=None,timestamp=None):
		DataEntry.__init__(self,identifier="dataentry",pk=pk,label=label,value=value,timestamp=timestamp)
		
if __name__=="__main__":
	d = CashReceipt(payor="gorio",pk=1)