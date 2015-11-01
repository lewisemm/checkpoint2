from living import Living
from office import Office
import utilities
from amity import Amity
from fellow import Fellow
from staff import Staff

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

									#figure out how to read from file
									pass

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

									#figure out how to read from text file
									pass

			
			elif ( answer == 2):
				# get list of allocations
				pass
			elif ( answer == 3):
				# print allocation list
				pass
			elif ( answer == 4):
				# list unallocated people
				pass
			elif ( answer == 5):
				# sub menu
				pass




tandao = Office()
tandao.setName('Tandao')
print 'The first name is ', tandao.getName(), ' and I am an office.'
print 'My max overcapacity is ', tandao.getMax(), ' people.'


malindi = Living()
malindi.setName('Malindi')
print 'The second name is ', malindi.getName(), ' and I am a living space.'
print 'My max overcapacity is ', malindi.getMax(), ' people.'

