import room
from overflow import OverflowException
from people.fellow import Fellow

# Living spaces have a default maximum of 4 people
# Only fellows can occupy living spaces
class Living(room.Room):

	# constructor
	def __init__(self):
		self.occupants = []
		self.max = 4


	def getMax(self):

		return self.max



	def addFellow(self, fellow):
		
		if isinstance(fellow, Fellow):

			if ( len(self.occupants) < self.max):

				self.occupants.append(fellow)

			else:

				raise OverflowException('This living space is full!')

		else:

			raise TypeError('Living spaces are meant for Fellows only!')

	def getOccupants(self):
		return self.occupants
