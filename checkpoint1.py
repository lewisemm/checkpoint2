from living import Living
from office import Office
import utilities
from amity import Amity
from fellow import Fellow
from staff import Staff
from random import random

campus = Amity()

# Populating from data/allocation.txt
campus.prePopulate()


# useeful vars
rangeError = 'Range error: *** Please select a number that is within the range'
valueError = 'Value error: *** Please enter a number in digit form ***\n'

# User Menu
while (True):

	utilities.mainMenu()

	answer = raw_input('Enter a number between 0 - 5 to select a menu.\n')

	try:
		# catch non integer input from the user
		answer = int(answer)

		# catch int that are outside the range in the menu
		if ( (answer < 0) or (answer > 5) ):
			utilities.clearScreen()
			print rangeError, ' 0 - 5 ***\n'
			continue

	except ValueError:
		utilities.clearScreen()
		print valueError

	else:
		if ( answer == 0):

			print 'Thank you for using this product. Goodbye. \n\n'

			break

		else:

			if ( answer == 1):
				# Allocate people to rooms

				utilities.clearScreen()

				while (True):

					# Choose either staff or fellow
					utilities.choosePersonMenu()

					chosen = raw_input('Enter a number between 0 - 2 to select a menu.\n')

					try:
						# catch non integer input from the user
						chosen = int(chosen)

						# catch int that are outside the range in the menu
						if ( (chosen < 0) or (chosen > 2) ):

							utilities.clearScreen()

							print rangeError, ' 0 - 5 ***\n'

							continue

					except ValueError:

						utilities.clearScreen()

						print valueError

					else:

						if (chosen == 0):

							# quit this menu
							break

						elif (chosen == 1):

							# Allocating staff (offices only)
							utilities.clearScreen()

							# Select app or text file data entry option
							utilities.appOrTextFileMenu()

							how = raw_input('Enter a number between 0 - 2 to select a menu \n')

							try:

								how = int(how)
						
								if ( (how < 0) or (how > 2)):

									utilities.clearScreen()

									print rangeError, ' 0 - 2 *** \n'

									continue

							except ValueError:

								utilities.clearScreen()

								print valueError

							else:

								if (how == 0):

									# Quit this menu
									break

								elif (how == 1):

									while (True):

										staffName = raw_input('Enter the name of the staff member. \n')

										if staffName:

											worker = Staff(staffName)

											campus.allocate(worker, 'Office')

											break

								elif (how == 2):

									# read from unallocated list file
									uStaff = open('data/input.txt')
									uStaffList = []
									edits = ''

									for line in uStaff.readlines():

										if line[0] == '>':
											
											staff = Staff(line[1::])
											uStaffList.append(staff)

										elif line[0] != '>':
											
											edits += line

									# re-write file and exclude unallocated staff (retrieved above)
									uStaff = open('data/input.txt', 'w')
									uStaff.write(edits)
									uStaff.close()

									# Allocate as long as there are office spaces and unallocated staff
									while ( len(uStaffList) > 0 ):

											randStaff = int(random() * len(uStaffList))
											campus.allocate(uStaffList[randStaff], 'Office')
											uStaffList.pop(randStaff)
											
									# Save unallocated people back to file
									if (len(uStaffList) > 0):

										uStaff = open('data/input.txt', 'a+')

										for staff in uStaffList:
											uStaff.write('>' + staff.getName())

						elif (chosen == 2):

							# Allocating fellows
							utilities.clearScreen()

							# Select the method for data input
							utilities.appOrTextFileMenu()

							how = raw_input('Enter a number between 0 - 2 to select a menu \n')

							try:

								how = int(how)
						
								if ( (how < 0) or (how > 2)):

									utilities.clearScreen()

									print rangeError, ' 0 - 2 *** \n'

									continue

							except ValueError:

								utilities.clearScreen()

								print valueError

							else:

								if (how == 0):

									# Quit this menu
									break

								elif (how == 1):
									# Allocate via app

									utilities.clearScreen()

									# select between office and living space
									utilities.chooseOfficeOrLivingMenu()

									space = raw_input('Enter a number between 0 - 2 to select a menu \n')

									try:

										space = int(space)
						
										if ( (space < 0) or (space > 2)):

											utilities.clearScreen()

											print rangeError, ' 0 - 2 *** \n'

											continue

									except ValueError:

										utilities.clearScreen()

										print valueError

									else:

										if (space == 0):
											break

										elif (space == 1):
											# Office space selected

											while (True):

												fellowName = raw_input('Enter the name of the fellow. \n')

												if fellowName:

													fellow = Fellow(fellowName)

													campus.allocate(fellow, 'Office')

													break

										elif (space == 2):
											# Living space selected

											while (True):

												fellowName = raw_input('Enter the name of the fellow. \n')

												if fellowName:

													fellow = Staff(fellowName)

													campus.allocate(fellow, 'Living')

													break
									

								elif (how == 2):
									# Allocate via text file

									utilities.clearScreen()

									# select between office and living space
									utilities.chooseOfficeOrLivingMenu()

									space = raw_input('Enter a number between 0 - 2 to select a menu \n')

									try:

										space = int(space)
						
										if ( (space < 0) or (space > 2)):

											utilities.clearScreen()

											print rangeError, ' 0 - 2 *** \n'

											continue

									except ValueError:

										utilities.clearScreen()

										print valueError

									else:

										if (space == 0):
											break

										elif (space == 1):
											# Office space selected

#########################
											# read from unallocated list file
											uFellowFile = open('data/input.txt')
											uFellowList = []
											edits = ''

											for line in uFellowFile.readlines():

												if line[0] == '#' and line[1] == '#':
											
													fellow = Fellow(line[2::])
													uFellowList.append(fellow)

												elif line[1] != '#':
											
													edits += line

											# re-write file and exclude unallocated staff (retrieved above)
											uFellowFile = open('data/input.txt', 'w')
											uFellowFile.write(edits)
											uFellowFile.close()

											# Allocate as long as there are office spaces and unallocated staff
											while ( len(uFellowList) > 0 ):

												randFellow = int(random() * len(uFellowList))
												campus.allocate(uFellowList[randFellow], 'Office')
												uFellowList.pop(randFellow)
											
											# Save unallocated people back to file
											if (len(uFellowList) > 0):

												uFellowFile = open('data/input.txt', 'a+')

												for fellw in uFellowFile:
													uFellowFile.write('#' + fellw.getName())
#########################											
											

										elif (space == 2):
											# Living space selected
											pass
											
			
			elif ( answer == 2):
				# get list of allocations
				pass

			elif ( answer == 3):
				# print allocation list

				utilities.clearScreen()
				
				allocations = open('data/allocated.txt')

				for lines in allocations.readlines():

					if lines[0:-1] == 'Living':

						# A header (visual separator)
						print 'Living Spaces (Fellows Only) \n', '-' * 80, '\n'

					elif lines[0] == '+':

						# The name of a living space
						print lines[1::]
						print '-' * 40

					elif lines[0] == '\t' and lines[1] != '>' and lines[1] != '#':
						# if it starts with a tab and it's not an office allocation

						print '\t', lines[1::]

					elif lines[0:-1] == 'Office':

						print '\n\n', 'Office Spaces \n', '-' * 80, '\n'

					elif lines[0] == '-':

						# The name of an office space
						print lines[1::], '\n', '-' * 40

					elif lines[0] == '\t' and lines[1] == '>':

						# Staff members in offices
						print '\t (S): ', lines[2::]

					elif lines[0] == '\t' and lines[1] == '#':

						# Fellows in offices
						print '\t (F): ', lines[2::]




			elif ( answer == 4):
				# list unallocated people

				utilities.clearScreen()

				fellowList = campus.getUnallocatedFellows()
				staffList = campus.getUnallocatedStaff()

				# print the unallocated staff

				print '\n\n\n', '-' * 40, ' Staff List ', '-' * 40

				for staff in staffList:

					print staff

				# print the unallocated fellows

				print '-' * 40, ' Fellow List ', '-' * 40

				for fellow in fellowList:

					print fellow

			elif ( answer == 5):
				# sub menu
				pass
