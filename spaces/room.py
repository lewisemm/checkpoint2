# Room is the superclass to Living and Office
# Every room has a name


class Room:

    def setName(self, name):
    	""" Sets the name for any instance of Room. """
        self.name = name

    def getName(self):
    	""" Gets the name for any instance of Room. """
        return self.name
