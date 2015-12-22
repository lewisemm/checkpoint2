[![Build Status](https://travis-ci.org/andela-lkabui/checkpoint2.svg?branch=develop)](https://travis-ci.org/andela-lkabui/checkpoint2)
[![Coverage Status](https://coveralls.io/repos/andela-lkabui/checkpoint2/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela-lkabui/checkpoint2?branch=develop)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/060712fe227e4c2387ebd9fee6b7da22/badge.svg)](https://www.quantifiedcode.com/app/project/060712fe227e4c2387ebd9fee6b7da22)
# Checkpoint 2

## Bucketlist API

### Introduction
* The bucketlist application API is built on top of [Flask](http://flask.pocoo.org) framework and makes use of several `libraries` to enhance its functionality.
* The `libraries` in use include;
   * **`passlib`** - It's used to hash the user's plain text password. Also used to verify plain text passwords from the client against the hashes in the database.
   * **`itsdangerous`** - It's used to generate tokens from users once they log in. It's also used to identify users from tokens when authentication (in methods annotated with `@auth.login_verified`) is required.
   * **`Flask-RESTful`** - It has been used to organise resources into class based views. It has also been used to help serialize and display the API's models into response objects.
   * **`Flask-HttpAuth`** - It's used to handle client authentication for resources where public access is denied. This API improvises this library's `@auth.verify_password` annotation to authenticate users via tokens.
   * **`sqlalchemy`** - The ORM that's used to transate database tables into python language objects through the use of models. It also handles CRUD operations and database initializations.
   * **`fake-factory`** - This API employs the use of this library in the unittests. It generates random values for input when testing.
   * **`ipdb`** - A Python debugger. It's used to help intercept, understand and detect bugs in code during the development process.
   * **`MySQL-python`** - The Python MySQL connector. This is the package that enables connections to be made to the underlying `MySQL` development database.
   * **`SQLAlchemy-Paginator`** - A pagination library that receives an `sqlalchemy query object` as its first argument and a `limit (results per page in int)` as the second argument and creates a pagination object through which the query's content can be accessed through pages.
   * **`coverage`** - This package is used to execute the tests. It also generates a test coverage report based on the lines of source code executed from the running tests.

### Installation
* Navigate to your directory of choice on terminal.
* Clone this repository.
  * Using ssh;
    * `git clone git@github.com:andela-lkabui/checkpoints.git`
  * Using http;
    * `https://github.com/andela-lkabui/checkpoints.git`
* Install the project's library dependencies. Navigate to the root folder of the project and run the following command.
  * `pip install -r requirements.txt`
* Install the project's database dependencies.
  * Install [MySQL](https://www.mysql.com/downloads/) - development database
  * Install [sqlite](https://www.sqlite.org/download.html) - testing database
* **```Note: The project doesn't impose any restrictictions regarding the use of these two databases. Any relational database should work. These are just the databases that were used during the development and testing stages and thus don't require extra libraries to be installed.```**
* To run the app, run the following command;
  * `python api.py`

### Routes, Methods and Functionality
* **`/user/registration`**
  * Method: POST
    * Creates a new user who can later use the API.
    * Requires `username` and `password` to be provided by the client for creation.
* **`/auth/login`**
  * Method: POST
    * Verifies a client's username and password against the values in the database and then generates a token for use in the API if the verification is successful.
    * Requires the client to provide a username and password.
    * Sets the `is_active` field in the user's model to `True`
* **`/auth/logout`**
  * Method: GET
    * Logs a user out.
    * Sets the `is_active` field in the user's model to `False`. This invalidates further authentication requests regardless of whether the token is valid.
* **`/bucketlists/`**
  * Method: POST
    * Create a new bucket list.
    * Requires the client to provide a bucketlist name.
    * Also requires the client to be authenticated.
  * Method: GET
    * Lists all the bucket lists that have been created in the API.
    * Requires the client to be authenticated.
* **`/bucketlists/<id>`**
  * Method: GET
    * Gets the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires the client to be authenticated.
  * Method: PUT
    * Updates the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires the client to provide a new bucketlist name.
    * Also requires the client to be authenticated.
  * Method: DELETE
    * Deletes the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires the client to be authenticated.
* **`/bucketlists/<id>/items/`**
  * Method: POST
    * Creates a new item in the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires client to provide an item name.
    * Also requires the client to be both authenticated and to be the owner of the bucketlist into which items are being inserted.
* **`/bucketlists/<id>/items/<item_id>`**
  * Method: PUT
    * Updates the item of id `<item_id>` in the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires the client to provide the name of the item and/or the done status of the item.
    * Also requires the client to be both authenticated and to be the owner of the bucketlist in which items are being edited.
  * Method: DELETE
    * Deletes the item of id `<item_id>` in the bucketlist whose id is equivalent to the `<id>` in the URL.
    * Requires the client to be both autheticated and to be the owner of the bucketlist from which the item is being deleted.

### Tests
* The `tests` have been created using Python's `unittest` module.
* The `tests` are run with the `coverage` package to enable generation of test coverage reports.
* To run the tests;
  * Navigate to the project's root directory (where the `requirements.txt` file is located)
  * Run the following command;
    * `coverage run -m unittest discover tests`
  * The tests are successful if all of them run with no failures and/or errors.
  ```shell
    .............................
    ----------------------------------------------------------------------
    Ran 29 tests in 27.776s

    OK
  ```
