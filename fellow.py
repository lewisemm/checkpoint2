import person

# Fellow has the option to board
class Fellow(person.Person):

	# store the name of the living space where the fellow is allocated
	def setBoardingRoom(self, boardingRoom):

		self.boardingRoom = boardingRoom


	# store the name of the office space where the fellow is allocated
	def setOfficeRoom(self, officeRoom):

		self.officeRoom = officeRoom


	# the getters
	# ------------------

	def getBoardingRoom(self):

		return self.boardingRoom


	def getOfficeRoom(self):
		
		return self.officeRoom
