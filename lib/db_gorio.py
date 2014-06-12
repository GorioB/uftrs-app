import sqlite3
import datetime
conn = sqlite3.connect("db.sqlite3")
defaultLength=40
class DataField:
	def __init__(self,dataType=None,content=None):
		self.dataType=dataType
		self.content=content

class DataEntry:
	def __init__(self,identifier,status=None,needsRoot=None,pk=0,timestamp=None,notes=None,remarks=None):
		self.identifier = identifier
		if status:
			self.status = status
		else:
			self.status = DataField("text","")
		if needsRoot:
			self.needsRoot = needsRoot
		else:
			self.needsRoot = DataField("text","False")
		self.pk = pk
		if timestamp:
			self.timestamp=timestamp
		else:
			self.timestamp = DataField("text","None")
		if notes:
			self.notes=notes
		else:
			self.notes=DataField("text","None")
		if remarks:
			self.remarks = remarks
		else:
			self.remarks=DataField("text","None")

	def createTable(self):
		fields = [[i,vars(self)[i]] for i in vars(self) if i!="identifier" and i!='pk']
		createQuery = "CREATE TABLE IF NOT EXISTS "+self.identifier+"(\n\tpk INTEGER PRIMARY KEY"
		fieldsList=[]
		for i in fields:
			createQuery=createQuery+",\n\t"+i[0]+" "+i[1].dataType.upper()

		createQuery=createQuery+");"
		try:
			c = conn.cursor()
			c.execute(createQuery)
			conn.commit()
			return 0
		except Exception,e:
			print e
			return 1

	def checkIfExists(self,pk):
		query = "SELECT COUNT(1) FROM "+self.identifier+" WHERE pk = "+str(pk)
		c = conn.cursor()
		c.execute(query)
		return c.fetchone()[0]

	def save(self):
		c = conn.cursor()
		if self.createTable():
			return 1
		fields = [[i,vars(self)[i]] for i in vars(self) if i!='identifier' and i!='pk']
		if self.checkIfExists(self.pk):
			return 1
		else:
			if not self.pk:
				query = "INSERT INTO "+self.identifier+" ("+",".join([i[0] for i in fields])+") VALUES ("+",".join(["?" for i in fields])+");"
				vals = [i[1].content for i in fields]
				try:
					c.execute(query,vals)
					c.execute("SELECT last_insert_rowid();")
					self.pk = int(c.fetchone()[0])
				except Exception, e:
					print e
					return 1
			else:
				query = "INSERT INTO "+self.identifier+" (pk,"+",".join([i[0] for i in fields])+") VALUES (?,"+",".join(["?" for i in fields])+");"
				vals = [int(self.pk)]+[i[1].content for i in fields]
				try:
					c.execute(query,vals)
				except Exception,e:
					print e
					return 1
		conn.commit()
		return 0

	def delete(self):
		self.status = DataField("text","DELETED: "+str(datetime.datetime.now()))
		query = "UPDATE "+self.identifier+" SET status=? WHERE pk="+str(self.pk)
		c = conn.cursor()
		c.execute(query,(self.status.content,))
		conn.commit()
		return 0


if __name__=="__main__":
	d = DataEntry("test",status=DataField("TEXT","PIE"))