from living import Living
from office import office

class Amity:

	def prePopulate(self, lSpaces, oSpaces):

		# naming the rooms

		# living spaces
		counter = 1
		for i  in lSpaces:
			liv = Living()
			liv.setName('Room ' + str(counter))
			self.occupants.append(liv)

		# office spaces
		counter = 1
		for j in oSpaces:
			off = Office()
			off.setName('Office ' + str(counter))
			self.occupants.append(off)
