# to be merged into the main DB script later on
import sqlite3
import hashlib

dbName = "dbName"
conn = sqlite3.connect(dbName)

class DataField(object):
	"""docstring for DataField"""
	def __init__(self, username, password, isRoot=0):
		self.username = username
		self.password = password
		self.isRoot = isRoot
		self.cursor = conn.cursor()
		
	def saveUser(self):
		"""Saves the user into the database"""
		# TODO: if (table doesn't exist) create table (username text, passwordHash text, isRoot integer)
		self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (self.username, self.passwordHash, self.isRoot))

	def auth(self):
		"""Checks if the username-password combination is valid"""

	def checkIfRoot(self):
		"""Checks against the database if user is root"""
		if ~self.auth(): return False
		# TODO: check against database's isRoot

	@property
	def password(self):
		return self._password
	@password.setter
	def password(self, value):
		"""Setter for password that auto-recomputes passwordHash"""
		self._password = value
		self.passwordHash = hashlib.sha224(value).hexdigest()

	@property
	def isRoot(self):
		return self._isRoot
	@isRoot.setter
	def isRoot(self, value):
		"""Setter that only sets isRoot to 0 or 1"""
		if value==0: self._isRoot = 0
		else: self._isRoot = 1
	

class DropDownMenu(object):
	"""docstring for DropDownMenu"""
	def __init__(self, identifier):
		self.identifier = identifier
		
	def getOptions(self):
		"""returns the list of options"""

	def addOption(self, option):
		"""add an option to the list of options"""

	def searchOption(self, string):
		"""returns the list of options that could autocomplete the passed string"""