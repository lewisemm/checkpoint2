import room
from overflow import OverflowException

# Living spaces have a default maximum of 4 people
# Only fellows can occupy living spaces
class Living(room.Room):

	def getMax(self):
		self.max = 4
		return self.max

	def addFellow(self, fellow):
		if isinstance(fellow, Fellow):
			if ( len(self.occupants) < self.max):
				self.occupants.append(fellow)
			else:
				raise OverflowException('This living space is full!')
		else:
			raise TypeError('Living spaces are meant for Fellows only!')
