from living import Living
from office import Office
from staff import Staff
from fellow import Fellow
from random import random
from overflow import OverflowException

class Amity:

	# constructor
	def __init__(self):
		self.living = []
		self.office = []

	def prePopulate(self, lSpaces, oSpaces):
		
		# naming living spaces
		counter = 1
		for i in range(lSpaces):
			liv = Living()
			liv.setName('Room ' + str(counter))
			self.living.append(liv)
			counter += 1

		# naming office spaces
		counter = 1
		for j in range(oSpaces):
			off = Office()
			off.setName('Office ' + str(counter))
			self.office.append(off)
			counter += 1

	


	def allocate(self, person, spaceType):

		def officeAllocation(person):
			# first check if there's room in any office
			available = False

			# find at least one available space to enable allocation
			for ofisi in self.office:
				if len(ofisi.occupants) < ofisi.max:
					available = True
					break;

			if available:
				# Try allocating this person an office as long as he encounters OverflowException
				# because we know from variable 'available' that there's a space somewhere
				while (True):

					rand = int(random() * 10)
				
					try:

						self.office[rand].addPeople(person)

					except OverflowException:

						continue

					else:

						print 'Insert Successful! Allocated to ', self.office[rand].getName()

						break

			else:
				print 'There are no more office spaces available.'


		def livingSpaceAllocation(person):
			available = False

			for room in self.living:
				if len(room.occupants) < room.max:
					available = True
					break;

			if available:
				# Try allocating this person a living space as long as he encounters OverflowException
				# because we know there's a space somewhere
				while (True):

					rand = int(random() * 10)
					
					try:

						self.living[rand].addFellow(person)

					except OverflowException:

						continue

					# when attempting to allocate staff a living space
					except TypeError:

						continue

					else:

						print 'Insert Successful! Allocated to ', self.living[rand].getName()

						break

			else:
				print 'There are no more living spaces available.'


		if isinstance(person, Staff):
			officeAllocation(person)

		elif isinstance(person, Fellow):

			if (spaceType == 'Office'):

				officeAllocation(person)

			elif (spaceType == 'Living'):

				livingSpaceAllocation(person)