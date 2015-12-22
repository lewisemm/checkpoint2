import json

from sqlalchemy_paginator.exceptions import EmptyPage
from test_base_class import TestBaseClass, register_and_login_user

class TestBucketListID(TestBaseClass):
	
	def test_bucketlist_id_unauthorized_get(self):
		"""
		Test unauthenticated get request to url '/bucketlists/<int:id>'.
		"""
		response = self.client.get('/bucketlists/1')
		self.assertEqual(response.status, '401 UNAUTHORIZED')

	def test_bucketlist_id_unauthorized_put(self):
		"""
		Test unauthenticated put request to url '/bucketlists/<int:id>'.
		"""
		response = self.client.put('/bucketlists/1')
		self.assertEqual(response.status, '401 UNAUTHORIZED')

	def test_bucketlist_id_unauthorized_delete(self):
		"""
		Test unauthenticated delete request to url '/bucketlists/<int:id>'.
		"""
		response = self.client.delete('/bucketlists/1')
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
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), 'Bucket of id 1 doesnt exist')

		# create a bucketlist to later test put, get(again) and delete methods
		bucketlist = {
			'name': self.fake.name()
		}
		response = self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
		resp_dict = json.loads(response.data)
		bucket_id = resp_dict.get('id')

		# the put method
		new_name = self.fake.name()
		response = self.client.put('/bucketlists/' + str(bucket_id), data={'name':new_name}, headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('name', new_name))

		# the put method - (non-existent bucketlist)
		new_name = self.fake.name()
		response = self.client.put('/bucketlists/2', data={'name':new_name}, headers={'username':token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "That bucket list id doesn't exist")

		# the get method
		response = self.client.get('/bucketlists/' + str(bucket_id), headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('name', new_name))


		# the delete method
		response = self.client.delete('/bucketlists/' + str(bucket_id), headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('message'), 'bucketlist of id ' + str(bucket_id) + ' has been deleted')

		# the delete method again (will be non-existent)
		response = self.client.delete('/bucketlists/' + str(bucket_id), headers={'username':token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertTrue(resp_dict.get('message'), "Bucket of id " + str(bucket_id) + " doesn't exist")

	def test_bucketlist_id_method_not_allowed(self):
		"""
		Test post http method on url '/bucketlists/<int:id>'.
		"""
		
		response = self.client.post('/bucketlists/1')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')