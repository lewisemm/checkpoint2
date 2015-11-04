from spaces.living import Living
from spaces.office import Office
from people.staff import Staff
from people.fellow import Fellow
from random import random
from custom.overflow import OverflowException
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
        """ Allocates Andelans to an office space at random. """

        def officeAllocation(person):
            """ Allocates Andelans to an office. """

            # first check if there's room in any office
            available = False

            # find at least one available space to enable allocation
            for ofisi in self.officeRooms:

                if len(ofisi.getOccupants()) < ofisi.max:

                    available = True

                    break

            if available:
                # Try allocating this person an office as long as he encounters OverflowException
                # because we know from variable 'available' that there's a
                # space somewhere

                officeCount = len(self.officeRooms)

                while (True):

                    rand = int(random() * officeCount)

                    currentOffice = self.officeRooms[rand]

                    try:

                        currentOffice.addPeople(person)

                    except OverflowException:

                        print 'Cannot allocate to ', currentOffice.getName(), ' ... moving on.'
                        # loop afresh and search for another room
                        continue

                    else:

                        edits = ''

                        try:

                            allocated = open('data/allocated.txt', 'r+')

                            for line in allocated.readlines():

                                edits += line

                                if (line[1::] == currentOffice.getName()):

                                    if isinstance(person, Fellow):

                                        edits += '\n\t#' + \
                                            person.getName() + '\n'

                                    elif isinstance(person, Staff):

                                        edits += '\n\t>' + \
                                            person.getName() + '\n'

                            # reposition pointer back to beginning to
                            # overwrite old data with this modified version
                            allocated.seek(0)

                            # write the modified version
                            allocated.write(edits)

                        except Exception as e:
                            print '*** An Exception occured! *** \n', e, '\n'

                        finally:
                            allocated.close()

                        print 'Insert Successful! Allocated to office space ', currentOffice.getName()

                        break

            else:
                print 'There are no more office spaces available.'

        def livingSpaceAllocation(person):
            """ Allocates fellows to a living space at random. """

            # Assume there's no space available until proven otherwise
            available = False

            for eachRoom in self.livingRooms:

                if len(eachRoom.getOccupants()) < eachRoom.max:

                    # This means there's a space available in one of the rooms
                    available = True

                    break

            if available:

                # Try allocating this person a living space as long as he encounters OverflowException
                # because there's a space (guaranteed) somewhere

                roomCount = len(self.livingRooms)

                while (True):

                    rand = int(random() * roomCount)

                    # random room selection
                    currentRoom = self.livingRooms[rand]

                    try:

                        currentRoom.addFellow(person)

                    except OverflowException:
                        print 'Cannot allocate to ', currentRoom.getName(), ' ... moving on.'
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

                            # get the starting index where the room's name
                            # first appears
                            for lines in allocated.readlines():

                                temp.write(lines)

                                if lines[1::] == currentRoom.getName():
                                    temp.write(
                                        '\n\t' + person.getName() + '\n')

                            os.remove('data/allocated.txt')
                            os.rename('data/temp.txt', 'data/allocated.txt')

                        except Exception as e:
                            print '*** An Exception occured! *** \n', e

                        finally:
                            allocated.close()
                            temp.close()

                        print 'Insert Successful! Allocated to living space ', currentRoom.getName()

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

    def getLivingRooms(self):
        return self.livingRooms

    def getOfficeRooms(self):
        return self.officeRooms
