# Checkpoint 1

## Office Space Allocation

### Purpose

The office space allocation apps models a room allocation system. Allocations are made at random and identical data ought to produce  different allocations with each run.

### Implementation

* This app uses the text files in the **data** folder to persist and edit staff and fellow allocation.
* Living and Office space instances each have a constant maximum number of occupants. If an attempt is made to add a person while the space is at capacity, an exception is raised with a message to tell the user that the space is full.
* Living spaces throw an extra exception (TypeError) when an attempt is made to add a staff member to a living space.

### How to use

1. Open Terminal on your computer.
2. Run ```python checkpoint1.py```. The app produces a menu similar to the one below. To select an item, input the number corresponding to the menu you want and press the enter key.

	```
		1. Allocate people to rooms
  		2. Get list of allocations
		3. Print allocation list
		4. List unallocated people
		5. List people in a room

		0. Quit application

	```

### Classes and Methods

	1. Room
		* Superclass to Office and Living class definitions
		* Has getter and setter methods for name attribute.

		1.1 Office
			* Subclass of the Room class
			* Has control variable, ```max```, that is initialized with each new instance.
			* Has method **addPerson** that only accepts objects of class Person, otherwise, a TypeError is raised. This method also checks for current occupants before it adds a new person and raises an **OverFlowException** if the room is already full.
			* Has method **getOccupants** that is a getter for occupants attribute.

		1.2 Living
			* Subclass of Room class
			* Has control variable, ```max```, that is initialized with each new instance.
			* Has method **addFellow** that only accepts objects of class Fellow, otherwise a TypeError is raised. This method also checks for current occupants before it adds a new person and raises an **OverflowException** if the room is already full.
			* Has method **getOccupants** that is a getter for the occupants attribute.

	2. Person
		* Superclass to Fellow and Staff.
		* Has getter and setter methods for name and gender attributes.

		2.1 Staff
			* Subclass of the Person class
			
		2.2 Fellow
			* Subclass of the Person class

	3. Amity
		* The campus. It’s composed of Living spaces and Office spaces.

		3.1 
			



