overcapacity = 'The room is filled to capacity!'

# Room is the superclass to Living and Office
# Every room has a name
class Room:

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

# Living spaces have a default maximum of 4 people
# Only fellows can occupy living spaces
class Living(Room):

	def getMax(self):
		self.max = 4
		return self.max

	def addFellow(self, fellow):
		if isinstance(fellow, Fellow):
			if ( len(self.occupants) < self.max):
				self.occupants.append(fellow)
			else:
				print overcapacity
		else:
			print 'Living spaces are meant for Fellows only!'

# Office spaces have a default maximum of 6 people
class Office(Room):

	def getMax(self):
		self.max = 6
		return self.max

	def addPeople(self, person):
		if isinstance(person, Person):
			if ( len(self.occupants) <= self.max):
				self.occupants.append(person)
			else:
				print overcapacity
		else:
			print 'Office spaces are meant to be allocated to people (Staff & Fellows)'

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
		return False;

	def setOffice(self, office):
		self.office = office;
		
	def getOffice(self):
		return self.office;
		
# Populating Amity with 20 spaces (10 living, 10 office)

# Ten empty living spaces
living = [None] * 10

# Ten empty office spaces
offices = [None] * 10

# Naming the rooms
counter = 1

for counter in range( len(living)):
	living[counter] = Living()
	living[counter].setName('Room ' +  str(counter + 1) )

	offices[counter] = Office()
	offices[counter].setName('Office ' + str(counter + 1) )

	counter += 1

# Amity has 20 unoccupied rooms in total
amity = [living, offices]



tandao = Office()
tandao.setName('Tandao')
print 'The first name is ', tandao.getName(), ' and I am an office.'
print 'My max overcapacity is ', tandao.getMax(), ' people.'


malindi = Living()
malindi.setName('Malindi')
print 'The second name is ', malindi.getName(), ' and I am a living space.'
print 'My max overcapacity is ', malindi.getMax(), ' people.'

