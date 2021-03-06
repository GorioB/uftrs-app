import sqlite3
import hashlib
import random
import string

DB_NAME = "db.sqlite3"

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

class User(object):
	"""docstring for User. Database table name is users"""
	def __init__(self, username, password):
		self.username = username
		self.password = password
		# create user table if it doesn't exist
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, passwordHash TEXT, secretQ TEXT, secretAns TEXT, isRoot INTEGER)")
		conn.commit()
		conn.close()

	def saveUser(self, secretQ, secretAns, isRoot=0):
		"""Saves/updates the user into the database. Optional: pass a 0 or 1 to specify isRoot value (0 by default)"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		if isRoot!=0: isRoot=1

		# hash the secret answer
		secretAns = hashlib.sha224(secretAns).hexdigest()

		if self.userExists(self.username):
			cursor.execute("UPDATE users SET username=?, passwordHash=?, secretQ=?, secretAns=?, isRoot=? WHERE username=?", 
				(self.username, self.passwordHash, secretQ, secretAns, isRoot, self.username))
		else:
			cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (self.username, self.passwordHash, secretQ, secretAns, isRoot))

		conn.commit()
		conn.close()

	def changePassword(self, newPassword):
		"""Sets the instance's password attribute and updates the passwordHash stored in the database"""
		self.password = newPassword
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("UPDATE users SET passwordHash=? WHERE username=?", (self.passwordHash, self.username))
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
		"""Returns the list of users in the database (includes all data, not just usernames)"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		userList = cursor.fetchall()
		conn.close()
		return userList

	@staticmethod
	def listUsernames():
		"""Returns the list of usernames (list of strings) in the database"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT username FROM users")
		userList = cursor.fetchall()
		conn.close()
		return [x[0] for x in userList]

	@staticmethod
	def userExists(username):
		"""Returns True if the passed username exists in the database"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		user = cursor.fetchone()
		conn.close()
		return user!=None

	@staticmethod
	def getSecretQuestion(username):
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT secretQ FROM users WHERE username=?", (username,))
		secretQ = cursor.fetchone()
		conn.close()
		return secretQ[0]

	@staticmethod
	def verifySecretAnswer(username, answer):
		"""Returns True if the passed answer to the passed usernam's secret question is correct"""
		submittedAnswer = hashlib.sha224(answer).hexdigest()

		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT secretAns FROM users WHERE username=?", (username,))
		correctAnswer = cursor.fetchone()
		conn.close()
		return correctAnswer[0]==submittedAnswer


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
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS dropdown(identifier TEXT, option TEXT, PRIMARY KEY (identifier, option))")
		conn.commit()
		conn.close()

	def getOptions(self):
		"""Returns the list of options (list of strings)"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT option FROM dropdown WHERE identifier=?", (self.identifier,))
		options = cursor.fetchall()
		conn.close()
		return [i[0] for i in options]

	@staticmethod
	def getIdentifiers():
		"""Returns the list of identifiers (list of strings)"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT identifier FROM dropdown")
		data = cursor.fetchall()
		conn.close()
		identifiers = [i[0] for i in data]
		return list(set(identifiers))

	def addOption(self, option):
		"""Adds an option to the list of options"""
		if self._optionExists(option):
			return
		else:
			conn = sqlite3.connect(DB_NAME)
			cursor = conn.cursor()
			cursor.execute("INSERT INTO dropdown VALUES (?, ?)", (self.identifier, option))
			conn.commit()
			conn.close()

	def removeOption(self, option):
		"""Removes an option from the list of options"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM dropdown WHERE identifier=? AND option=?", (self.identifier, option))
		conn.commit()
		conn.close()

	def searchOption(self, string):
		"""Returns the list of options that could autocomplete the passed string"""
		options = self.getOptions()
		possibleOptions = []
		for option in options:
			if option.startswith(string):
				possibleOptions.append(option)
		return possibleOptions

	def _optionExists(self, option):
		"""Returns true if the option exists"""
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM dropdown WHERE identifier=? AND option=?", (self.identifier, option))
		user = cursor.fetchone()
		conn.close()
		return user!=None

if __name__ == "__main__":
	# print DropDownMenu.getIdentifiers()
	print User.listUsernames()
