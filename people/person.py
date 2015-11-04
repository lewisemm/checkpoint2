# Person is the superclass to Staff and Fellow
# Every person has a name and gender


class Person:

	# constructor accepting name argument
    def __init__(self, name):
        self.name = name

    def getName(self):
    	""" Returns the name of a person instance. """

        return self.name

    def setGender(self, gender):
    	""" Sets the gender of a person instance. """

        self.gender = gender

    def getGender(self):
    	""" Returns the gender of a person instance. """

        return self.gender
