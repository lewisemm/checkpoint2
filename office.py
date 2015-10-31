import room
from overflow import OverflowException
from person import Person

# Office spaces have a default maximum of 6 people
class Office(room.Room):

	# constructor
	def __init__(self):
		self.occupants = []
		self.max = 6

	def getMax(self):

		return self.max


	def addPeople(self, person):

		if isinstance(person, Person):

			if ( len(self.occupants) < self.max):

				self.occupants.append(person)

			else:

				raise OverflowException('This office space is full!')

		else:

			raise TypeError('Office spaces are meant to be allocated to people (Staff & Fellows)')

	def getOccupants(self):
		return self.occupants
				
