import sqlite3
import datetime
import inspect
DB_NAME = "db.sqlite3"
class DataField:
	def __init__(self,dataType=None,content=None):
		self.dataType=dataType
		self.content=content

	def __str__(self):
		return self.dataType+": "+self.content

class DataEntry:
	def __init__(self,identifier,pk=0,timestamp=None,status=None,**kwargs):
		self.identifier = identifier
		self.pk = pk
		if timestamp:
			self.timestamp=DataField("TEXT",timestamp)
		else:
			self.timestamp=DataField("TEXT","None")
		if status:
			self.status = DataField("TEXT",status)
		else:
			self.status=DataField("TEXT","")
		for key,value in kwargs.items():
			setattr(self,key,DataField("TEXT",value))

		self._setFieldTypes("INTEGER","timestamp")

	def addField(self,dataType,**kwargs):
		for key,value in kwargs.items():
			setattr(self,key,DataField(dataType,value))

	def _setFieldTypes(self,fieldType,*args):
		for i in args:
			setattr(self,i,DataField(fieldType,vars(self)[i].content))

	def _createTable(self):
		conn = sqlite3.connect(DB_NAME)
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
			conn.close()
			return 0
		except Exception,e:
			print e
			conn.close()
			return 1

	def _checkIfExists(self,pk):
		conn = sqlite3.connect(DB_NAME)
		query = "SELECT COUNT(1) FROM "+self.identifier+" WHERE pk = "+str(pk)
		c = conn.cursor()
		c.execute(query)
		rVal = c.fetchone()[0]
		conn.close()
		return rVal

	def save(self):
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		if self._createTable():
			return 1
		fields = [[i,vars(self)[i]] for i in vars(self) if i!='identifier' and i!='pk']
		if self._checkIfExists(self.pk):
			query = "UPDATE "+self.identifier+" SET "+",".join([i[0]+"=?" for i in fields])+" WHERE pk="+str(self.pk)
			vals = [i[1].content for i in fields]
			try:
				c.execute(query,vals)
			except Exception, e:
				print e
				conn.close()
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
					conn.close()
					return 1
			else:
				query = "INSERT INTO "+self.identifier+" (pk,"+",".join([i[0] for i in fields])+") VALUES (?,"+",".join(["?" for i in fields])+");"
				vals = [int(self.pk)]+[i[1].content for i in fields]
				try:
					c.execute(query,vals)
				except Exception,e:
					print e
					conn.close()
					return 1
		conn.commit()
		conn.close()
		return 0

	def delete(self,edit=0):
		conn = sqlite3.connect(DB_NAME)
		if not edit:
			self.status = DataField("TEXT","DELETED")
		else:
			self.status = DataField("TEXT","EDITED")
		query = "UPDATE "+self.identifier+" SET status=? WHERE pk="+str(self.pk)
		c = conn.cursor()
		c.execute(query,(self.status.content,))
		conn.commit()
		conn.close()
		return 0

	def __str__(self):
		 return self.identifier+" Entry. pk = "+str(self.pk)

def _populateModel(model,fields,values):
	m = model()#testvalue. Replace with actual models
	for i in range(0,len(fields)):
		vars(m)[fields[i][1]]=DataField(fields[i][2],values[i])
	m.pk = int(m.pk.content)
	return m

def getEntry(pk,model):
	conn = sqlite3.connect(DB_NAME)
	m = model()#testvalue. Replace with actual models
	c = conn.cursor()
	query = "SELECT * FROM "+m.identifier+" WHERE pk=?;"
	c.execute(query,(pk,))
	vals = c.fetchone()
	query = "PRAGMA table_info("+m.identifier+");"
	c.execute(query)
	columns = c.fetchall()
	conn.close()
	if vals:
		return _populateModel(model,columns,vals)
	else:
		return None

def listEntries(model):
	conn = sqlite3.connect(DB_NAME)
	m = model()
	c = conn.cursor()
	query = "SELECT * FROM "+m.identifier+";"
	c.execute(query)
	results = c.fetchall()
	query = "PRAGMA table_info("+m.identifier+");"
	c.execute(query)
	columns=c.fetchall()
	objectList = [_populateModel(model,columns,i) for i in results]
	conn.close()
	return objectList

if __name__=="__main__":
	#d = DataEntry("test",status=DataField("TEXT","PIE"))
	e= listEntries(DataEntry)