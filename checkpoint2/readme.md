# Bucketlist API

## Introduction
* The bucketlist application API is built on top of `Flask` and uses several `libraries` to enhance its functionality.
* The `libraries` in use include;
   * **`passlib`** - It's used to hash the user's plain text password. Also used to identify a user from a given token
   * **`itsdangerous`** - It's used to generate tokens from users and identify users from tokens.
   * **`Flask-RESTful`** - It's used to organise resources into class based views
   * **`Flask-HttpAuth`** - It's used to handle user authentication. This API improvises this ability to help authenticate users via tokens.
   * **`sqlalchemy`** - The ORM that's used to transate database tables into language objects through the use of models. It also handles CRUD operations and datanase configurations

## Routes
* **`/auth/login`**
  * Method - POST
    * Logs a user in
* **`/auth/logout`**
  * Method - GET
    * Logs a user out
* **`/bucketlists/`**
  * Method - POST
    * Create a new bucket list
  * Method - GET
    * List all the bucket lists that have been created
* **`/bucketlists/<id>`**
  * Method - GET
    * Get a single bucket list
  * Method - PUT
    * Update this bucket list
  * Method - DELETE
    * Delete this single bucket list
* **`/bucketlists/<id>/items/`**
  * Method - POST
    * Creates a new item in a bucket list
* **`/bucketlists/<id>/items/<item_id>`**
  * Method - PUT
    * Updates a bucket list item
  * Method - DELETE
    * Deletes an item in a bucket list