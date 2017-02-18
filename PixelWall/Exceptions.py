class unexpectedType(Exception):
	def __init__(self, types = None,variable = None):
		self.variable = variable
        self.types = types

	def __str__(self):
		return "[!]Expecting type"+repr(self.types) ,"for:",repr(self.variable)
