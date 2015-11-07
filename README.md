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

### Significant Classes and Methods

#### 1. Room
   * Superclass to Office and Living class definitions
   * Has getter and setter methods for name attribute.

   ##### 1.1 Office
      * Subclass of the Room class
      * Has control variable, ```max```, that is initialized with each new instance.
      * Has method **addPerson** that only accepts objects of class Person, otherwise, a TypeError is raised. This method also checks for current occupants before it adds a new person and raises an **OverFlowException** if the room is already full.
      * Has method **getOccupants** that is a getter for occupants attribute.

   ##### 1.2 Living
      * Subclass of Room class
      * Has control variable, ```max```, that is initialized with each new instance.
      * Has method **addFellow** that only accepts objects of class Fellow, otherwise a TypeError is raised. This method also checks for current occupants before it adds a new person and raises an **OverflowException** if the room is already full.
      * Has method **getOccupants** that is a getter for the occupants attribute.

#### 2. Person
   * Superclass to Fellow and Staff.
   * Has getter and setter methods for name and gender attributes.

   ##### 2.1 Staff
      * Subclass of the Person class

   ##### 2.2 Fellow
      * Subclass of the Person class

#### 3. Amity
   * The campus. It’s composed of Living spaces and Office spaces.

   ##### 3.1 prePopulate()
      *	Reads the allocated.txt to get a list of Offices and Living spaces. Living spaces in this file start with a '+' symbol while Office spaces start with a '-'
      * Allocations under living spaces are for fellows only and each allocation line on the file starts with a tab character **ONLY**.
      * Allocations under office spaces all start with a tab character too. To differentiate from living space allocations, a character is added after the tab character. '>' indicates a staff member allocation while '#' indicates a fellow allocation.

   ##### 3.2 getOfficeRooms()
      * Returns a list containing office spaces and their current occupants

   ##### 3.3 getLivingRooms()
      * Returns a list containing living spaces and their current occupants.

   ##### 3.4 allocate(person, spaceType)
      * Receives two arguments. The first is an object of class Person while the second is a string indicating the type of space to allocate (i.e. can either be 'Office' or 'Living')
      * If the first argument object is of instance Staff, the officeAllocation method is called.
      * If the first argument object is of instance Fellow, the spaceType argument determines which method (between livingSpaceAllocation and officeAllocation) whill be called.

   ##### 3.5 officeAllocation(person, officeList)
      * Allocates a person at a time to an office space.
      * First iterates through the officeList and stops if a space is found.
      * If a space is found, a loop will attempt to allocate the person to a random office. Chances are that an attempt will be made to allocate the person to an office that's already full. When this happens, an OverflowException will be thrown and the loop will continue running. Otherwise if a successful allocation is made, this information will be persisted to the allocated.txt file and the program breaks out of the loop.
      * If a space is not found, the program will show a message to the user informing him/her of this

   ##### 3.6 livingSpaceAllocation(person, livingList)
      * Allocates a person at a time to a living space.
      * First iterates through the livingList and stops if a space is found.
      * If a space is found, a loop will attempt to allocate the person to a random living space. Chances are that an attempt will be made to allocate the person to living space that's already full. When this happens, an OverflowException will be thrown and the loop will continue running. Otherwise if a successful allocation is made, this information will be persisted to the allocated.txt file and the program breaks out of the loop.
      * If a space is not found, the program will show a message to the user informing him/her of this
