# Person is the superclass to Staff and Fellow
# Every person has a name and gender
class Person:
	def setName(self, name):
		self.name = name
	
	def getName(self):
		return self.name

	def setGender(self, gender):
		self.gender = gender

	def getGender(self):
		return self.gender
