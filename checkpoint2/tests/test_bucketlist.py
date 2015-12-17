import os
import unittest
import sqlite3
import json

from sqlalchemy import create_engine
from faker import Factory

from models.models import init_db

import api

fake = Factory.create()

def register_and_login_user(client):
	username = fake.user_name()
	password = fake.password()

	# register the user
	response = client.post('/user/registration', data={'username':username, 'password':password})
	# login the user
	response = client.post('/auth/login', data={'username':username, 'password':password})

	token = json.loads(response.data).get('token')

	return token

class TestBucketList(unittest.TestCase):
	
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

	def test_bucketlist_unauthorized_get(self):
		"""
		Test unauthenticated get request to url '/bucketlists/'.
		"""
		response = self.client.get('/bucketlists/')
		self.assertEqual(response.status, '401 UNAUTHORIZED')
		self.assertTrue('Unauthorized Access' in response.data)

	def test_bucketlist_unauthorized_post(self):
		"""
		Test unauthenticated post request to url '/bucketlists/'.
		"""
		bucketlist = {
			'name': fake.name()
		}

		response = self.client.post('/bucketlists/', data=bucketlist)
		self.assertEqual(response.status, '401 UNAUTHORIZED')
		self.assertTrue('Unauthorized Access' in response.data)

	def test_bucketlist_authorized_get(self):
		"""
		Test authenticated get request to url '/bucketlists/'.
		"""

		token = register_and_login_user(self.client)
		# pass the token in headers under username key to authenticate requests
		response = self.client.get('/bucketlists/', headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		# empty list expected since the database has no bucketlists yet
		self.assertTrue('[]' in response.data)

		del token

	def test_bucketlist_authorized_post(self):
		"""
		Test authenticated post request to url '/bucketlists/'.
		"""
		bucketlist1 = {
			'name': fake.name()
		}

		token = register_and_login_user(self.client)
		response = self.client.post('/bucketlists/', data=bucketlist1, headers={'username':token})
		self.assertEqual(response.status, '201 CREATED')

		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('name'), bucketlist1.get('name'))

		del token

	def test_bucketlist_method_not_allowed(self):
		"""
		Test put and delete http methods.
		"""
		
		response = self.client.put('/bucketlists/')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

		response = self.client.delete('/bucketlists/')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')


if __name__ == '__main__':
	unittest.main()