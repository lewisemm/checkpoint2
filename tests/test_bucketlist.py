import json

from sqlalchemy_paginator.exceptions import EmptyPage

from test_base_class import TestBaseClass, register_and_login_user

class TestBucketList(TestBaseClass):

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
			'name': self.fake.name()
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
			'name': self.fake.name()
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

	def test_bucketlist_id_pagination_authorized(self):
		"""
		Tests authenticated pagination request to '/bucketlists/'.
		"""
		# create 5 bucket lists
		five_bl = []
		for no in range(5):
			five_bl.append(dict(name= self.fake.name()))

		token = register_and_login_user(self.client)
		# post them to the database
		for bucketlist in five_bl:
			self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
		# send a paginated get request (one item per page)
		response = self.client.get('/bucketlists/?limit=1', headers={'username':token})
		# iterate through the paged results
		for no in range(1, 6):
			response = self.client.get('/bucketlists/page/' + str(no), headers={'username':token})
			resp_dict = json.loads(response.data)
			self.assertEqual(five_bl[no-1].get('name'), resp_dict[0].get('name'))
		# page 6 doesn't exist
		response = self.client.get('/bucketlists/page/6', headers={'username':token})
		self.assertEqual(response.status, '404 NOT FOUND')
		self.assertTrue("Page doesn't exist" in response.data)

	def test_bucketlist_id_authorized_search_by_name(self):
		"""
		Tests fetch and retrieval of bucketlist through provision of a bucketlist name.
		"""
		# Create a bucketlist
		bucketlist = {
			'name': self.fake.name()
		}

		token = register_and_login_user(self.client)
		# post it to the database
		self.client.post('/bucketlists/', data=bucketlist, headers={'username':token})
		
		# provide bucketlist name for searching
		response = self.client.get('/bucketlists/?q=' + bucketlist.get('name'), headers={'username':token})
		self.assertEqual(response.status, '200 OK')
		self.assertTrue(bucketlist.get('name') in response.data)
		# search a random bucketlist name and don't expect to find it
		random_username = self.fake.name()
		response = self.client.get('/bucketlists/?q=' + random_username, headers={'username':token})
		self.assertTrue("[]" in response.data)

if __name__ == '__main__':
	unittest.main()