import os
from random import random

from spaces.living import Living
from spaces.office import Office
from people.staff import Staff
from people.fellow import Fellow
from custom.overflow import OverflowException
from custom import utilities

file_path = utilities.getPath('data/')
 

def office_allocation(person, officeList):
    """ Allocates Andelans to an office at random. """
    # first check if there's room in any office
    available = False
    # find at least one available space to enable allocation
    for ofisi in officeList:
        if len(ofisi.occupants) < ofisi.max:
            available = True
            break

    if available:
        # Try allocating this person an office as long as he encounters OverflowException
        # because we know from variable 'available' that there's a space somewhere

        officeCount = len(officeList)
        while (True):
            rand = int(random() * officeCount)
            currentOffice = officeList[rand]
            try:
                currentOffice.addPeople(person)
            except OverflowException:
                print 'Cannot allocate ', person.name, ' to ', currentOffice.name, ' ... moving on.'
                continue
            else:
                edits = ''
                try:

                    allocated = open(file_path + 'allocated.txt', 'r+')
                    for line in allocated.readlines():
                        edits += line
                        if (line[1::] == currentOffice.name):
                            if isinstance(person, Fellow):
                                edits += '\n\t#' + \
                                    person.name + '\n'
                            elif isinstance(person, Staff):
                                edits += '\n\t>' + \
                                    person.name + '\n'

                    # reposition pointer back to beginning to
                    # overwrite old data with this modified version
                    allocated.seek(0)
                    allocated.write(edits)
                except Exception as e:
                    print '*** An Exception occured! *** \n', e, '\n'
                finally:
                    allocated.close()
                print 'Insert Successful! Allocated ', person.name, ' to  ', currentOffice.name 
                break
    else:
        print 'There are no more office spaces available.'

def living_space_allocation(person, livingList):
    """ Allocates fellows to a living space at random. """
    # Assume there's no space available until proven otherwise
    available = False
    for eachRoom in livingList:
        if len(eachRoom.occupants) < eachRoom.max:
        # This means there's a space available in one of the rooms
            available = True
            break
    if available:
        # Try allocating this person a living space as long as he encounters OverflowException
        # because there's a space (guaranteed) somewhere
        roomCount = len(livingList)
        while (True):
            rand = int(random() * roomCount)
            # random room selection
            currentRoom = livingList[rand]
            try:
                currentRoom.addFellow(person)
            except OverflowException:
                print 'Cannot allocate ', person.name, ' to ', currentRoom.name, ' ... moving on.'
                # loop afresh to find another random room
                continue
            # when attempting to allocate staff a living space
            except TypeError:
                # loop afresh to find another random room
                continue
            else:
                # if person has found a room, persist this info.
                edits = ''
                try:
                    allocated = open(file_path + 'allocated.txt', 'r+')
                    # get the starting index where the room's name
                    # first appears
                    for lines in allocated.readlines():
                        edits += lines
                        if lines[1::] == currentRoom.name:
                            edits += '\n\t' + person.name + '\n'

                    # reposition pointer back to beginning to
                    # overwrite old data with this modified version
                    allocated.seek(0)
                    allocated.write(edits)
                except Exception as e:
                    print '*** An Exception occured! *** \n', e
                finally:
                    allocated.close()
                print 'Insert Successful! Allocated to living space ', currentRoom.name, ' to ', person.name
                break
    else:
        print 'There are no more living spaces available.'


class Amity:

    # constructor
    def __init__(self):
        self.livingRooms = []
        self.officeRooms = []
        
    def prePopulate(self):
    	""" Initializes state from text files in the data folder of the app. """
    	# retrieve existing room names at data/allocation.txt
        allocation = open(file_path + 'allocated.txt')
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
            elif (line[0] == '\t' and line[1] != '>' and line[1] != '#'):
                # This is a fellow in a living space
                # insert the current fellow at the lastIndex
                lastIndex = len(self.livingRooms) - 1
                # Create a fellow object from the name on the file
                fellow = Fellow(line[1::])
                self.livingRooms[lastIndex].addFellow(fellow)
            elif (line[0] == '\t' and line[1] == '#'):
                # This is a fellow in an office space
                # insert these people at the lastIndex
                lastIndex = len(self.officeRooms) - 1
                # Create a fellow object from the name on the file
                fellow = Fellow(line[2::])
                self.officeRooms[lastIndex].addPeople(fellow)
            elif (line[0] == '\t' and line[1] == '>'):
                # This is a staff member in an office space
                # insert these people at the lastIndex
                lastIndex = len(self.officeRooms) - 1
                # Create a staff object from the name on the file
                staff = Staff(line[2::])
                self.officeRooms[lastIndex].addPeople(staff)
        allocation.close()

    def allocate(self, person, spaceType):
        """ Allocates Andelans to an office or a living space space at random. """
        if isinstance(person, Staff):
            office_allocation(person, self.officeRooms)
        elif isinstance(person, Fellow):
            if (spaceType == 'Office'):
                office_allocation(person, self.officeRooms)
            elif (spaceType == 'Living'):
                living_space_allocation(person, self.livingRooms)

