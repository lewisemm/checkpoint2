from room import Room
from custom.overflow import OverflowException
from people.fellow import Fellow

# Living spaces have a default maximum of 4 people
# Only fellows can occupy living spaces


class Living(Room):

    def __init__(self):
        self.occupants = []
        self.max = 4

    def addFellow(self, fellow):
    	""" Adds a Fellow to a living space. Rejects Staff members."""
        if isinstance(fellow, Fellow):
            if (len(self.occupants) < self.max):
                self.occupants.append(fellow)
            else:
                raise OverflowException('This living space is full!')
        else:
            raise TypeError('Living spaces are meant for Fellows only!')