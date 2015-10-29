from living import Living
from office import Office
		
# Populating Amity with 20 spaces (10 living, 10 office)

# Ten empty living spaces
living = [None] * 10

# Ten empty office spaces
offices = [None] * 10

# Naming the rooms
counter = 1

for counter in range( len(living)):
	living[counter] = Living()
	living[counter].setName('Room ' +  str(counter + 1) )

	offices[counter] = Office()
	offices[counter].setName('Office ' + str(counter + 1) )

	counter += 1

# Amity has 20 unoccupied rooms in total
amity = [living, offices]

# User Menu
answer = 0
while (not answer):
	print '-' * 80
	print '-' * 40, ' MENU ', '-' * 34
	print '-' * 80
	print '1. Allocate people to rooms.'
	print '2. Get list of allocations.'
	print '3. Print allocation list.'
	print '4. List unallocated people.'
	print '5. List people in a room.'
	print '-' * 80
	print '-' * 80
	answer = raw_input('Enter a number between 1 - 5 to choose. Enter Q (in caps) to quit. \n')

# Handling input from user at the menu
if ( answer == 'Q'):
	print 'Thank you for using this product. Goodbye.'
elif ( (answer >= 'A') or (answer <='z')):
	print 'Please choose between 1 - 5 or Q'
else:
	if ( int(answer) == 1):
		# sub menu
		pass
	elif ( int(answer) == 2):
		# get list of allocations
		pass
	elif ( int(answer) == 3):
		# print allocation list
		pass
	elif ( int(answer) == 4):
		# list unallocated people
		pass
	elif ( int(answer) == 5):
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

