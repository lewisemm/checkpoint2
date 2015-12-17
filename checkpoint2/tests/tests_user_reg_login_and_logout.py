import os
import unittest
import sqlite3

from sqlalchemy import create_engine
from faker import Factory

from models import init_db

import api

fake = Factory.create()

class TestRegistrationLoginLogout(unittest.TestCase):
	
	def setUp(self):
		self.app = api.app

		# Store the state of APP_SETTINGS before modifying it
		# These will later be restored in the tearDown method
		self.prod_settings = os.environ['APP_SETTINGS']
		os.environ['APP_SETTINGS'] = 'config.config.TestingConfig'
		# configure the app with the test settings
		self.app.config.from_object(os.environ['APP_SETTINGS'])

		# set the engine and session (in api.py) with test settings
		api.manager = api.init_session()

		# get the sqlite database file's path by slicing away the 'sqlite:///' prefix
		self.db_file = self.app.config.get('DATABASE_URL')[10:]
		# create the database file on disk
		sqlite3.connect(self.db_file)
		# create the tables from the models in models.py
		init_db(self.app.config.get('DATABASE_URL'))

		# the client that will be used to test the REST API
		self.client = self.app.test_client()

	def tearDown(self):
		# revert the APP_SETTINGS to its previous state
		os.environ['APP_SETTINGS'] = self.prod_settings
		api.app.config.from_object(os.environ['APP_SETTINGS'])

		# delete the sqlite database file
		os.remove(self.db_file)
	
	def test_registration(self):
		"""
		Test the registration of a new user.
		"""
		response = self.client.post('/user/registration', data={'username':fake.user_name(), 'password':fake.password()})
		self.assertTrue('User successfully registered!' in response.data)
		self.assertEqual(response.status, '201 CREATED')

	def test_login_no_user_account(self):
		"""
		Test the login attempt from non existent user.
		"""
		response = self.client.post('/auth/login', data={'username':fake.user_name(), 'password':fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')

	def test_login_invalid_password(self):
		"""
		Test the login attempt from existing user, wrong password.
		"""
		username = fake.user_name()
		password = fake.password()

		# register the user
		response = self.client.post('/user/registration', data={'username':username, 'password':password})
		# log the user
		response = self.client.post('/auth/login', data={'username':username, 'password':fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')

	def test_successful_login(self):
		"""
		Test a successful login attempt.
		"""
		username = fake.user_name()
		password = fake.password()

		# register the user
		response = self.client.post('/user/registration', data={'username':username, 'password':password})
		# log the user
		response = self.client.post('/auth/login', data={'username':username, 'password':password})
		self.assertEqual(response.status, '200 OK')
		self.assertTrue('token' in response.data)

if __name__ == '__main__':
	unittest.main()