from models import COCPNote,OME,OONote,LTINote
from timeFuncs import *
def getStartBalance(app,startDate):
	lastBalanceDate, balance = app.balance
	lastBalanceDate = int(lastBalanceDate)

	for i in app.listCashReceipts():
		print startDate, i.dateOfTransaction.content, lastBalanceDate
	inflows = [float(i.amount.content) for i in app.listCashReceipts() if int(i.dateOfTransaction.content)<int(startDate) and int(i.dateOfTransaction.content)>lastBalanceDate]
	outflowTypes = [OME,OONote,LTINote]
	outflows = []
	for j in outflowTypes:
		outflows+=[float(i.amount.content) for i in app._listGeneral(j) if int(i.dateOfTransaction.content)<int(startDate) and int(i.dateOfTransaction.content)>lastBalanceDate]
	outflows+=[float(i.amount.content) for i in app._listGeneral(COCPNote) if int(i.dateOfTransaction.content)<int(startDate) and int(i.dateOfTransaction.content)>lastBalanceDate and i.flowDirection.content=="Outflow"]
	netFlow = sum(inflows)-sum(outflows)

	return balance+netFlow


if __name__=="__main__":
	from timeFuncs import *
	from app import App
	a = App()
	p = stringToSecs("2020-07-24 00:00:00")
	print getStartBalance(a,p)