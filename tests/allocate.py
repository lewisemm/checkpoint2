import unittest
import os
from amity import Amity
from people.staff import Staff
from people.fellow import Fellow
from custom.overflow import OverflowException


class TestAllocationFromFile(unittest.TestCase):


    def setUp(self):
        """ Creates the context on which tests will be run. """
        # Create users for the test and write them to file
        users = ">Anthony Nandaa\n#Eric Gichuri\n#Mahad Walusimbi\n>Godson Ukpere\n##Kevin Ndungu\n>Joshua Mwaniki\n"
        alloFile = open('data/input.txt', 'w+')
        alloFile.write(users)
        alloFile.close()

        # Create rooms for the test and write them to file
        spaces = "+Heroku\n\tThomas Nyambati\n\tJeremy Kithome\n\tCollin Mutembei\n\tBrian Koech\n+Sound Cloud\n+Node\n+Digital Ocean\n\tGertrude Nyenyeshi\n\tStacey A.\n-Staff Room\n-Office 1\n-Office 2\n-Office 3\n-Office 4\n-Office 5\n"
        roomsFile = open('data/allocated.txt', 'w+')
        roomsFile.write(spaces)
        roomsFile.close()

        # Initialize amity campus
        self.campus = Amity()
        self.campus.prePopulate()

    def tearDown(self):
        """ Performs housekeeping to clean up test files after tests have been executed. """
        os.remove('data/input.txt')
        os.remove('data/allocated.txt')

    def test_prepopulate(self):
        """ Expects 4 living spaces and 6 office rooms. """
        self.assertEqual(len(self.campus.getLivingRooms()), 4)
        self.assertEqual(len(self.campus.getOfficeRooms()), 6)

    def test_unallocated_people(self):
        """ Expect unallocateed people to be 6. """
        uFile = open('data/input.txt')
        unallocated = []
        for line in uFile.readlines():
            unallocated.append(line)
        self.assertEqual(len(unallocated), 6)

    def test_fellows_allocated_living(self):
        """ Expect fellows allocated living spaces to be 6. """
        aFile = open('data/allocated.txt')
        allocated = []
        for line in aFile.readlines():
            if (line[0] == '\t'):
                allocated.append(line)
        self.assertEqual(len(allocated), 6)
    

    def test_allocate_through_app(self):
        """ Expects exception when allocation is performed on a full room. """
        # Expect the first room (Heroku) to have 4 occupants
        heroku = self.campus.getLivingRooms()[0]
        self.assertEqual(len(heroku.getOccupants()), 4)

        # Expect the fourth room (Digital Ocean) to have 2 occupants
        docean = self.campus.getLivingRooms()[3]
        self.assertEqual(len(docean.getOccupants()), 2)

        # Expect OverflowException because heroku is full
        aFellow = Fellow("Martin Nate")
        with self.assertRaises(OverflowException):
            heroku.addFellow(aFellow)

        # Expect TypeError when staff added to living space
        staffer = Staff("Hellen Maina")
        with self.assertRaises(TypeError):
            heroku.addFellow(staffer)

    if __name__ == '__main__':
        unittest.main()
