import person

# Staff cannot be allocated a living space
# but can be allocated an office
class Staff(person.Person):
	
	def isBoarding(self):
		return False

	def setOffice(self, office):
		self.office = office
		
	def getOffice(self):
		return self.office
