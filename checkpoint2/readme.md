# Bucketlist API

## Introduction
* The bucketlist application API is built on top of `Flask` and uses several `libraries` to enhance its functionality.
* The `libraries` in use include;
   * **`passlib`** - It's used to hash the user's plain text password. Also used to identify a user from a given token
   * **`itsdangerous`** - It's used to generate tokens from users and identify users from tokens.
   * **`Flask-RESTful`** - It's used to organise resources into class based views
   * **`Flask-HttpAuth`** - It's used to handle user authentication. This API improvises this library's features to help authenticate users via tokens.
   * **`sqlalchemy`** - The ORM that's used to transate database tables into language objects through the use of models. It also handles CRUD operations and database configurations

## Routes
* **`/auth/login`**
  * Method - POST
    * Verifies a user's credentials and generates a token for use in the API thereafter.
* **`/auth/logout`**
  * Method - GET
    * Logs a user out.
* **`/bucketlists/`**
  * Method - POST
    * Create a new bucket list.
  * Method - GET
    * Lists all the bucket lists that have been created in the API.
* **`/bucketlists/<id>`**
  * Method - GET
    * Gets the bucketlist whose id is equivalent to the `<id>` in the URL.
  * Method - PUT
    * Updates the bucketlist whose id is equivalent to the `<id>` in the URL.
  * Method - DELETE
    * Deletes the bucketlist whose id is equivalent to the `<id>` in the URL.
* **`/bucketlists/<id>/items/`**
  * Method - POST
    * Creates a new item in the bucketlist whose id is equivalent to the `<id>` in the URL.
* **`/bucketlists/<id>/items/<item_id>`**
  * Method - PUT
    * Updates the item of id `<item_id>` in the bucketlist whose id is equivalent to the `<id>` in the URL.
  * Method - DELETE
    * Deletes the item of id `<item_id` in the bucketlist whose id is equivalent to the `<id>` in the URL.