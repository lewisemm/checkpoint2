import room

# Office spaces have a default maximum of 6 people
class Office(room.Room):

	def getMax(self):
		self.max = 6
		return self.max

	def addPeople(self, person):
		if isinstance(person, Person):
			if ( len(self.occupants) <= self.max):
				self.occupants.append(person)
			else:
				print 'This office space is full!'
		else:
			print 'Office spaces are meant to be allocated to people (Staff & Fellows)'
