# App Class
# 	User _activeUser
# 	createUser(username,password,isRoot)
# 	changePass(username,oldpassword,newpassword)
# 	login(username,password)
# 	exportExcel(entryList)
# 	printStatement()

# 	Either generates a pdf file or directly accesses the printer. See references and design documents for format.
# 	newCashReceipt(**kwargs)
# 	editCashReceipt()
# 	listCashReceipts() 

# 		and so on
# 	listOptions(identifier)
# 	searchOption(identifier, option)
# 	addOption(identifier, option)
# 	removeOption(identifier, option)

import db2

class App(object):
	"""Main app class that exposes methods for the GUI module to access"""
	def __init__(self, arg):
		self._activeUser = db2.User("dummy", "dummy")

	def createUser(self, username, password, isRoot):
		"""Creates a new user if username isn't taken, otherwise returns -1. isRoot value should be 0 or 1"""
		if db2.User.userExists(username):
			return -1
		else:
			newUser = db2.User(username, password)
			newUser.saveUser(isRoot)

	def changePass(self, username, oldpassword, newpassword):
		"""Changes the user's password if username-oldpassword combo is valid."""
		if db2.User(username, oldpassword).auth():
			changedUser = db2.User(username, newpassword)
			if changedUser.checkIfRoot():
				changedUser.saveUser(1)
			else:
				changedUser.saveUser(0)
		else:
			return -1

	def login(self, username, password):
		"""Returns true if the username-password combination is valid"""
		self._activeUser = db2.User(username, password)
		return self._activeUser.auth()

	def listOptions(identifier):
		"""Returns a list of options (list of strings) for the given identifier e.g. 'payors'"""
		return db2.DropDownMenu(identifier).getOptions()

	def searchOption(identifier, option):
		"""Returns a list of options (list of strings) that can complete the passed option"""
		return db2.DropDownMenu(identifier).searchOption(option)

	def addOption(identifier, option):
		"""Adds an option to the list of options"""
		db2.DropDownMenu(identifier).addOption(option)

	def removeOption(identifier, option):
		"""Removes an option from the list of options"""
		db2.DropDownMenu(identifier).removeOption(option)
