class unexpectedType(Exception):
	def __init__(self, variable, type = None):
		self.variable = variable
		self.type = type
		
	def __str__(self):
		return "[!]Expecting type: " + repr(self.type) + " for " + self.variable
