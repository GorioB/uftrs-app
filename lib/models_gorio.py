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

		[self.setIntegerFields(i) for i in integerFields]
		[self.setRealFields(i) for i in realFields]

if __name__=="__main__":
	d = CashReceipt(payor="gorio",pk=1)