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
			'name': self.fake.name()
		}
		response = self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
		resp_dict = json.loads(response.data)
		bucket_id = resp_dict.get('id')

		# then update it
		new_name = self.fake.name()
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