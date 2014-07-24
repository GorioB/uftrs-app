def getOAL(app):
	assetTypes = ["accountsOutstanding","inventoriesAndOtherAssets","others"]
	assets = [getAndSort(app,i) for i in assetTypes]
	
	assetDescriptions = ["Accounts Outstanding (Payable/Receivable)",
		"Inventories and Other Material Assets",
		"Others"]

	superString = ""
	letters="A"
	for i in range(0,3):
		if assets[i]:
			superString+="\n"+letters+". "+assetDescriptions[i]+'\n'
			for entryIndex in range(0,len(assets[i])):
				superString+=str(entryIndex+1)+". "+assets[i][entryIndex].details.content+'\n'
			letters= chr(ord(letters)+1)

	return superString

def getAndSort(app,assetType):
	return sorted([i for i in app.listOALs() if i.OALType.content==assetType and i.includeInStatement.content=="True"],
		key=lambda j : int(j.timestamp.content))

if __name__=="__main__":
	from app import *
	a = App()
	getOAL(a)