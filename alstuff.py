# to be merged into the main DB script later on

class DataField(object):
	"""docstring for DataField"""
	def __init__(self, username, password, dbName, isRoot=False):
		self.username = username
		self.password = password
		self.dbName = dbName
		self.isRoot = False
		
	def saveUser(self):
		"""Saves the user into the database"""

	def auth(self):
		"""Checks if the username-password combination is valid"""

class DropDownMenu(object):
	"""docstring for DropDownMenu"""
	def __init__(self, identifier, dbName):
		self.identifier = identifier
		self.dbName = dbName
		
	def getOptions(self):
		"""returns the list of options"""

	def addOption(self, option):
		"""add an option to the list of options"""

	def searchOption(self, string):
		"""returns the list of options that could autocomplete the passed string"""


# 	User
# userName
# password
# isRoot
# saveUser()
# auth()
# DropDownMenu 
# getOptions()
# addOption(option)
# searchOption(string)
