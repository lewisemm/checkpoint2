import os
import unittest
import sqlite3
import json

from sqlalchemy import create_engine

from faker import Factory

from sqlalchemy_paginator.exceptions import EmptyPage

from requests import get

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

class TestBucketListID(unittest.TestCase):
	
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

	def test_bucketlist_id_unauthorized_get(self):
		"""
		Test unauthenticated get request to url '/bucketlists/<int:id>'.
		"""
		response = self.client.get('/bucketlists/1')
		self.assertEqual(response.status, '401 UNAUTHORIZED')

	def test_bucketlist_id_authorized(self):
		"""
		Test authenticated request to url '/bucketlists/<int:id>'.
		Methods tested include GET, PUT and DELETE
		"""

		token = register_and_login_user(self.client)

		# Bucketlist non existent
		response = self.client.get('/bucketlists/1', headers={'username':token})
		self.assertEqual(response.status, '404 NOT FOUND')

		# create a bucketlist
		bucketlist = {
			'name': fake.name()
		}
		response = self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
		resp_dict = json.loads(response.data)
		bucket_id = resp_dict.get('id')

		# then update it
		new_name = fake.name()
		response = self.client.put('/bucketlists/' + str(bucket_id), data={'name':new_name}, headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('name', new_name))

		# then get it
		response = self.client.get('/bucketlists/' + str(bucket_id), headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('name', new_name))


		# then delete it
		response = self.client.delete('/bucketlists/' + str(bucket_id), headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('message'), 'bucketlist of id ' + str(bucket_id) + ' has been deleted')

		# post method not allowed
		response = self.client.post('/bucketlists/' + str(bucket_id), data=bucketlist, headers={'username':token})
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('message'), 'The method is not allowed for the requested URL.')

	# def test_bucketlist_id_pagination_authorized(self):
	# 	"""
	# 	Tests authenticated pagination request to '/bucketlists/<int:id>'.
	# 	Creates five bucketlists and requests 5 pages from the API.
	# 	"""
	# 	# create 5 bucket lists
	# 	five_bl = []
	# 	for no in range(5):
	# 		five_bl.append(dict(name=fake.name()))

	# 	token = register_and_login_user(self.client)
	# 	# post them to the database
	# 	for bucketlist in five_bl:
	# 		self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
	# 	# send a paginated get request (one item per page)
	# 	# response = self.client.get('/bucketlists?limit=1', headers={'username':token})
	# 	response = get('http://localhost/bucketlists?limit=1', headers={'username': token})
	# 	# response = self.client.get('/bucketlists?limit=1', headers={'username':token})
	# 	# iterate through the paged results
	# 	for no in range(1, 6):
	# 		response = self.client.get('/bucketlists/page/' + str(no), headers={'username':token})
	# 		resp_list = json.loads(response.data)
	# 		# ipdb.set_trace()
	# 		self.assertEqual(five_bl[no-1].get('name'), resp_list[no-1].get('name'))
	# 	# check for exception when non-existent is accessed
	# 	with self.assertRaises(EmptyPage):
	# 		response = self.client.get('/bucketlists/page/' + str(6), headers={'username':token})