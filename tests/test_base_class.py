import os
import unittest
import sqlite3
import json

from sqlalchemy import create_engine
from faker import Factory

from models.models import init_db

import api

def register_and_login_user(client):
	fake = Factory.create()

	username = fake.user_name()
	password = fake.password()

	# register the user
	response = client.post('/user/registration', data={'username':username, 'password':password})
	# login the user
	response = client.post('/auth/login', data={'username':username, 'password':password})

	token = json.loads(response.data).get('token')

	return token

class TestBaseClass(unittest.TestCase):
	
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

		self.fake = Factory.create()

	def tearDown(self):
		# revert the APP_SETTINGS to its previous state
		os.environ['APP_SETTINGS'] = self.prod_settings
		api.app.config.from_object(os.environ['APP_SETTINGS'])

		# delete the sqlite database file
		os.remove(self.db_file)