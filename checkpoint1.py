# Room is the superclass to Living and Office
# Every room has a name
class Room:

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

# Living spaces have a default maximum of 4 people
class Living(Room):

	def getMax(self):

		self.max = 4

		return self.max

	def addFellow(self, fellow):

		if isinstance(fellow, Fellow):

			if (len(self.occupants) <= self.max):

				self.occupants.append(fellow)

			else:

				print 'The room is filled to capacity!'

		else:

			print 'Living spaces are meant for Fellows only!'

# Office spaces have a default maximum of 6 people
class Office(Room):

	def getMax(self):
		self.max = 6
		return self.max

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


# Fellow has the option to board
class Fellow(Person):

	def setBoarding(self, option):
		self.option = option

	def isBoarding(self):
		return self.option


# Staff cannot be allocated a living space
# but can be allocated an office
class Staff(Person):
	
	def isBoarding(self):
		return false;

	def setOffice(self, office):
		self.office = office;
		
	def getOffice(self):
		return self.office;
		
# Populating Amity with 20 spaces (10 living, 10 office)
living = [Living()] * 10
offices = [Office()] * 10

amity = [living, offices]

for 

tandao = Office()
tandao.setName('Tandao')
print 'The first name is ', tandao.getName(), ' and I am an office.'
print 'My max capacity is ', tandao.getMax(), ' people.'


malindi = Living()
malindi.setName('Malindi')
print 'The second name is ', malindi.getName(), ' and I am a living space.'
print 'My max capacity is ', malindi.getMax(), ' people.'

