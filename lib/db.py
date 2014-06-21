import inspect
import sqlite3
from timeFuncs import getEpochTime
DB_NAME=("db.sqlite3")
class DataField:
	def __init__(self,dataType,content):
		self.dataType=dataType
		self.content=content

	def set(self,content):
		self.content=content

	def __repr__(self):
		return str(self.content)
class Binosaur:
	saur=3

class TextField(DataField):
	def __init__(self,content=""):
		DataField.__init__(self,"TEXT",content)

class IntegerField(DataField):
	def __init__(self,content=0):
		DataField.__init__(self,"INTEGER",content)

class RealField(DataField):
	def __init__(self,content=0.0):
		DataField.__init__(self,"REAL",content)
class PK(DataField):
	def __init__(self,content=0):
		DataField.__init__(self,"INTEGER PRIMARY KEY",content)

class DataEntry:
	def __init__(self,**kwargs):
		self.identifier = self.__class__.__name__
		self.pk = PK(0)
		self.timestamp = IntegerField(getEpochTime())
		self.status = TextField()
		self.remarks = TextField()

		for key in self._listClassVars():
			setattr(self,key,
				self.__class__.__dict__[key].__class__(self.__class__.__dict__[key].content))
			#setattr(self,key,self.__class__.__dict__[key])

		for key,value in kwargs.items():
			if key in vars(self).keys():
				vars(self)[key].set(value)
	#private methods
	def _listClassVars(self):
		return [name for name,obj in self.__class__.__dict__.iteritems()
			if not name.startswith("__") and not inspect.isroutine(obj)]

	def _getFields(self):
		return [[i,vars(self)[i]] for i in vars(self) if i!="identifier"]

	def _exists(self,pk):
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		query = "SELECT COUNT(1) FROM "+self.identifier+" WHERE pk ="+str(self.pk.content)
		c.execute(query)
		rVal = c.fetchone()[0]
		conn.close()
		return rVal

	#public methods
	def createTable(self):
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		fields = self._getFields()
		query = "CREATE TABLE IF NOT EXISTS "+self.identifier
		fieldString = ','.join([i[0]+" "+i[1].dataType for i in fields])
		query = query+"("+fieldString+");"
		try:
			c.execute(query)
			conn.commit()
			conn.close()
			return 0
		except Exception,e:
			print e
			conn.close()
			return 1


	def save(self):
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		fields = self._getFields()
		if self._exists(self.pk.content):
			query = "UPDATE "+self.identifier+" SET "+",".join([i[0]+"=?" for i in fields])+" WHERE pk="+str(self.pk.content)
			vals = [i[1].content for i in fields]
			try:
				c.execute(query,vals)
			except Exception, e:
				print conn.close()
				return 1
		else:
			if not self.pk.content:
				query = "INSERT INTO "+self.identifier+" ("+",".join([i[0] for i in fields if i[0]!='pk'])+") VALUES ("+",".join(["?" for i in fields if i[0]!='pk'])+");"
				vals = [i[1].content for i in fields if i[0]!='pk']
				try:
					
					c.execute(query,vals)
					c.execute("SELECT last_insert_rowid();")
					self.pk.set(int(c.fetchone()[0]))
				except Exception, e:
					print e
					conn.close()
					return 1
			else:
				query = "INSERT INTO "+self.identifier
				query = query+"("+",".join([i[0] for i in fields])+") VALUES ("+",".join(["?" for i in fields])+");"
				vals = [i[1].content for i in fields]
				try:
					
					c.execute(query,vals)
				except Exception,e:
					print e
					conn.close()
					return 1
		conn.commit()
		conn.close()
		return 0



	def delete(self):
		self.status.set("DELETED")
		self.save()

def _populateModel(model,fields,values):
	m = model()
	for i in range(0,len(fields)):
		vars(m)[fields[i][1]].set(values[i])
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

class testModel(DataEntry):
	text = TextField()
	num = IntegerField()
