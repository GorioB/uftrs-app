import sqlite3
import hashlib

DB_NAME = "dbName"

class User(object):
	"""docstring for User. Database table name is users"""
	def __init__(self, username, password):
		self.username = username
		self.password = password
		# create user table if it doesn't exist
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, passwordHash TEXT, isRoot INTEGER)")
		conn.commit()
		conn.close()

	def saveUser(self, isRoot=0):
		"""Saves/updates the user into the database. Optional: pass a 0 or 1 to specify isRoot value (0 by default)"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		if isRoot!=0: isRoot=1

		if self.userExists(self.username):
			cursor.execute("UPDATE users SET username=?, passwordHash=?, isRoot=? WHERE username=?", 
				(self.username, self.passwordHash, isRoot, self.username))
		else:
			cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (self.username, self.passwordHash, isRoot))

		conn.commit()
		conn.close()


	def auth(self):
		"""Returns True if the User instance's username-password combination is valid"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT passwordHash FROM users WHERE username=?", (self.username,))
		passwordHash = cursor.fetchone()
		conn.close()

		if passwordHash==None: return False
		return passwordHash[0]==self.passwordHash


	def checkIfRoot(self):
		"""Returns True if User instance is root and username-pass combo is valid"""
		if not self.auth(): return False
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT isRoot FROM users WHERE username=?", (self.username,))
		isRoot = cursor.fetchone()
		conn.close()
		return isRoot[0]==1


	@staticmethod
	def listUsers():
		"""Returns the list of users in the database"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		userList = cursor.fetchall()
		conn.close()
		return userList


	@staticmethod
	def userExists(username):
		"""Returns True if the passed username exists in the database"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		user = cursor.fetchone()
		conn.close()
		return user!=None


	@property
	def password(self):
		return self._password
	@password.setter
	def password(self, value):
		"""Setter for password that auto-recomputes passwordHash"""
		self._password = value
		self.passwordHash = hashlib.sha224(value).hexdigest()



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

