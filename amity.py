from living import Living
from office import Office
from staff import Staff
from fellow import Fellow
from random import random
from overflow import OverflowException
import os

class Amity:

	# constructor
	def __init__(self):
		self.livingRooms = []
		self.officeRooms = []

	def prePopulate(self):
		
		# retrieve existing room names at data/allocation.txt

		allocation = open('data/allocated.txt')

		while (True):
			line = allocation.readline()
			if not line:
				break

			if (line[0] == '+'):
				# living spaces start with '+' in the file
				aLivingRoom = Living()
				aLivingRoom.setName(line[1::])
				self.livingRooms.append(aLivingRoom)

			elif (line[0] == '-'):
				# office spaces start with '-' in the file
				anOfficeRoom = Office()
				anOfficeRoom.setName(line[1::])
				self.officeRooms.append(anOfficeRoom)

			elif (line[0] == '\t'):
				# insert these people at the lastIndex
				lastIndex = len(self.livingRooms) - 1

				# Create a fellow object from the name on the file
				fellow = Fellow(line[1::])
				self.livingRooms[lastIndex].addFellow(fellow)


		allocation.close()


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

						try:
							allocated = open('allocated.txt', 'w')
							allocated.write(self.office[rand].getName() )
							#allocated.write(self.office[rand].getOccupants().getName() + ', ')

						except IOError:
							print '*** An IOError occured! *** \n', e, '\n'

						finally:
							allocated.close()
						
						print 'Insert Successful! Allocated to ', self.office[rand].getName()

						break

			else:
				print 'There are no more office spaces available.'


		def livingSpaceAllocation(person):

			# Assume there's no space available until proven otherwise
			available = False

			for eachRoom in self.livingRooms:

				if len(eachRoom.occupants) < eachRoom.max:

					# This means there's a space available in one of the rooms
					available = True

					break

			if available:

				# Try allocating this person a living space as long as he encounters OverflowException
				# because there's a space (guaranteed) somewhere
				while (True):

					rand = int(random() * 10)

					# random room selection
					currentRoom = self.livingRooms[rand]
					
					try:
						
						currentRoom.addFellow(person)

					except OverflowException:

						# loop afresh to find another random room
						continue

					# when attempting to allocate staff a living space
					except TypeError:

						# loop afresh to find another random room
						continue

					else:

						# if person has found a room, persist this info.
						try:

							allocated = open('data/allocated.txt', 'r+')
							temp = open('data/temp.txt', 'w')

							# get the starting index where the room's name first appears
							for lines in allocated.readlines():

								temp.write(lines)

								if lines[1::] == currentRoom.getName():
									temp.write('\n\t' + person.getName() + '\n')

							os.remove('data/allocated.txt')
							os.rename('data/temp.txt', 'data/allocated.txt')
									
						except Exception as e:
							print '*** An Exception occured! *** \n', e

						finally:
							allocated.close()
							temp.close()

						print 'Insert Successful! Allocated to ', currentRoom.getName()

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