from living import Living
from office import Office
import utilities
from amity import Amity
from fellow import Fellow

campus = Amity()

# Populating (10 living, 10 office)
campus.prePopulate(10, 10)


# useeful vars
allocator = '1. Allocate people to rooms.'
rangeError = 'Range error: *** Please select a number that is within the range'
valueError = 'Value error: *** Please enter a number in digit form ***\n'

# User Menu
while (True):
	print '-' * 80
	print '-' * 40, ' MAIN MENU ', '-' * 28
	print '-' * 80
	print ' ' * 80
	print allocator
	print '2. Get list of allocations.'
	print '3. Print allocation list.'
	print '4. List unallocated people.'
	print '5. List people in a room.'
	print ' ' * 80
	print '0. Quit application.'
	print ' ' * 80
	print '-' * 80

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
		# Handling input from user at the menu
		if ( answer == 0):
			print 'Thank you for using this product. Goodbye. \n\n'
			break

		else:

			if ( answer == 1):
				# sub menu: either staff or fellow allocation

				utilities.clearScreen()

				while(True):
					print '-' * 80
					print '-' * 40, allocator, '-' * (40 - len(allocator) )
					print '-' * 80
					print ' ' * 80
					print '1. Allocate Fellow'
					print '2. Allocate Staff'
					print ' ' * 80
					print '0. Quit sub-menu'
					print ' ' * 80
					print '-' * 80

					alloc = raw_input('Enter a number between 0 - 2 to select a menu \n')

					try:
						alloc = int(alloc)
						
						if ( (alloc < 0) or (alloc > 2)):
							utilities.clearScreen()
							print rangeError, ' 0 - 2 *** \n'
							continue

					except ValueError:
						utilities.clearScreen()
						print valueError

					else:

						if (alloc == 0):
							utilities.clearScreen()
							print 'Exiting ***', allocator, '*** MENU ... \n'
							break
						elif (alloc == 1):
							# allocate fellow

							utilities.clearScreen()
							header = ' ALLOCATION METHOD '

							while(True):
								print '-' * 80
								print '-' * 40, header, '-' * (40 - len(header))
								print '-' * 80
								print ' ' * 80
								print '1. Allocate through the app'
								print '2. Allocate through text file'
								print ' ' * 80
								print '0. Exit sub-menu'
								print ' ' * 80
								print '-' * 80

								choice = raw_input('Enter a number between 0 - 2 to select a manu \n')

								try:
									choice = int(choice)

									if ( (choice < 0) or (choice > 2)):
										utilities.clearScreen()
										print rangeError, ' 0 - 2 *** \n'
										continue

								except:
									utilities.clearScreen()
									print valueError

								else:
									if (choice == 0):
										utilities.clearScreen()
										print 'Exiting *** ', header, ' MENU *** \n'
										break;
									elif (choice == 1):
										# allocate via app
										utilities.clearScreen()

										while (True):

											name = raw_input('Enter the name of the fellow: \n')

											if name:
												fellow = Fellow()
												fellow.setName(name)

												campus.allocate(fellow, 'Living')
												break

										
										
									elif (choice == 2):
										# allocate via text file
										pass
							
						elif (alloc == 2):
							# allocate staff
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

