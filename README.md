# Checkpoint 1

## Office Space Allocation

### Purpose

The office space allocation apps models a room allocation system. Allocations are made at random and identical data ought to produce  different allocations with each run.

### Implementation

* This app uses the text files in the **data** directory to persist and edit staff and fellow allocation.
* `Living` and `Office` space instances each have a constant maximum number of occupants. If an attempt is made to add a person while the space is at capacity, an exception (`OverflowException`) will be raised with a message to tell the user that the space is full.
* `Living` instances throw an extra exception (`TypeError`) when an attempt is made to add a `Staff` instance to a living space.

### How to use

1. Open Terminal on your computer.
2. Navigate to the project’s root directory (the checkpoint’s directory.)
3. Run `python checkpoint1.py`. The app produces a menu similar to the one below. To select an item, input the number corresponding to the menu you want and press the enter key.

	```
		1. Allocate people to rooms
		2. Get list of allocations
		3. Print allocation list
		4. List unallocated people
		5. List people in a room

		0. Quit application

	```

### Significant Classes and Methods

#### 1. `Room`
   * Superclass to `Office` and `Living` class definitions
   
   ##### 1.1 `Office`
      * Subclass of the `Room` class
      * Has control variable, `max`, that is initialized with each new instance.
      * Has method **addPerson** that only accepts objects of class `Person`, otherwise, a `TypeError` is raised. This method also checks for current occupants before it adds a new person and raises an `OverFlowException` if the room is already full.
      
   ##### 1.2 `Living`
      * Subclass of `Room` class
      * Has control variable, `max`, that is initialized with each new instance.
      * Has method **addFellow** that only accepts objects of class `Fellow`, otherwise a `TypeError` is raised. This method also checks for current occupants before it adds a new person and raises an `OverflowException` if the room is already full.
      
#### 2. `Person`
   * Superclass to `Fellow` and `Staff`.
   
   ##### 2.1 `Staff`
      * Subclass of the `Person` class

   ##### 2.2 `Fellow`
      * Subclass of the `Person` class

#### 3. `Amity`
   * The campus. It’s composed of `Living` spaces and `Office` spaces.

   ##### 3.1 prePopulate()
      *	Reads the `allocated.txt` to get a list of `Offices` and `Living` spaces. `Living` spaces in this file start with a '`+`' symbol while Office spaces start with a '`-`'
      * Allocations under living spaces are for `Fellow` instances only. Allocations for these are represented on the `allocated.txt` file with a line that starts with a tab character **ONLY**.
      * Allocations under office spaces in the `allocation.txt` file all start with a tab character too. To differentiate from living space allocations, a character is added after the tab character. '`>`' indicates a staff member allocation while '`#`' indicates a fellow allocation.

   ##### 3.2 allocate(person, spaceType)
      * Receives two arguments. The first is an object of class `Person` while the second is a `string` indicating the type of space to allocate (i.e. the `string` can either be 'Office' or 'Living')
      * If the first argument object is of instance `Staff`, the **officeAllocation** method is called.
      * If the first argument object is of instance `Fellow`, the spaceType argument will determine which method (between **livingSpaceAllocation** and **officeAllocation**) will be called.

   ##### 3.3 officeAllocation(person, officeList)
      * Allocates a person at a time to an office space.
      * First iterates through the officeList and stops if a space is found.
      * If a space is found, a loop will attempt to allocate the person to a random office. Chances are that an attempt will be made to allocate the person to an office that's already full. When this happens, an `OverflowException` will be thrown and the loop will continue running. Otherwise if a successful allocation is made, this information will be persisted to the `allocated.txt` file and the program breaks out of the loop.
      * If a space is not found, the program will show a message to the user informing him/her of this

   ##### 3.4 livingSpaceAllocation(person, livingList)
      * Allocates a person at a time to a living space.
      * First iterates through the livingList and stops if a space is found.
      * If a space is found, a loop will attempt to allocate the person to a random living space. Chances are that an attempt will be made to allocate the person to living space that's already full. When this happens, an `OverflowException` will be thrown and the loop will continue running. Otherwise if a successful allocation is made, this information will be persisted to the `allocated.txt` file and the program breaks out of the loop.
      * If a space is not found, the program will show a message to the user informing him/her of this

#### 4. `Tests`
   * Tests done using the `unittest` module.

   ##### 4.1 setUp()
      * Creates context for running tests.
      * Creates the `input.txt` file and initializes it with six people (three staff members, two fellows [to be allocated living spaces], and one fellow [to be allocated an office])
      * Creates the `allocated.txt` file and **initializes** it with **four living spaces** (`Heroku`, `Sound Cloud`, `Node`, `Digital Ocean`) and **five office spaces** (`Staff Room`, `Office 1`, `Office 2`, `Office 3`, `Office 4` and `Office 5`)
      * `Heroku` already has maximum occupants.
      * Creates the Amity campus and initializes offices and living spaces with occupants data from the `allocated.txt` file.

   ##### 4.2 tearDown()
      * Deletes the `input.txt` and `allocated.txt` files once tests are run. (Performs housekeeping)

   ##### 4.3 test_prepopulate()
      * Tests for four living rooms as read from the file that was created during setUp()
      * Tests for six office spaces as read from the file that was created during setUp()

   ##### 4.4 test_unallocated_people()
      * Retrieve data from `input.txt` (created during setUp()) and expect six unallocated people.

   ##### 4.5 test_fellows_allocated_living()
      * Read from the `allocated.txt` file created during setUp() and expect six fellows.

   ##### 4.6 test_allocate_through_app()
      * Expects room `Heroku` to have four occupants.
      * Expects `Digital Ocean` to have two occupants. 
      * Tests for exception. Attempt is made to add a fellow to room `Heroku` (which is already full) and the test expects an `OverflowException` to be raised.
      * Tests for exception. Attempt is made to add a staff member to a living space and a `TypeError` is raised.

#### 5. Running the tests
   Tests are run through the `unittest` module with test discovery.

   * Navigate to the project’s root directory i.e. the checkpoints directory
   * Run the following command
      *  `python -m unittest discover tests `
   * The tests are considered successful if there are no failures on the log.
