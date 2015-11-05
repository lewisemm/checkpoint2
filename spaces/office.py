import room
from custom.overflow import OverflowException
from people.person import Person

# Office spaces have a default maximum of 6 people
class Office(room.Room):
    # constructor
    def __init__(self):
        self.occupants = []
        self.max = 6

    def getMax(self):
        """ Returns the maximum number of occupants allowed for instances of Office. """
        return self.max
        
    def addPeople(self, person):
        """ Adds people (either Staff or Fellow) to an office. Rejects all other instance types. """
        if isinstance(person, Person):
            if (len(self.occupants) < self.max):
                self.occupants.append(person)
            else:
                raise OverflowException('This office space is full!')
        else:
            raise TypeError('Office spaces are meant to be allocated to people (Staff & Fellows)')

    def getOccupants(self):
    	
    	""" Returns a list of all current occupants of an instance of Office. """
    	
        return self.occupants
