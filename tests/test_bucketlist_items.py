import json

from test_base_class import TestBaseClass, register_and_login_user

class TestBucketListItems(TestBaseClass):

	def test_unauthenticated_access(self):
		"""
		Tests unauthenticated request to '/bucketlists/id/items'.
		"""
		item = {
			'name': self.fake.name()
		}
		response = self.client.post('/bucketlists/1/items/', data=item)
		self.assertEqual(response.status, '401 UNAUTHORIZED')

	def test_bucketlist_items_method_not_allowed(self):
		"""
		Test get, put and delete http method on url '/bucketlists/<int:id>/items/'.
		"""
		
		response = self.client.get('/bucketlists/1/items/')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

		response = self.client.put('/bucketlists/1/items/')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

		response = self.client.delete('/bucketlists/1/items/')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

	def test_bucketlist_items_authenticated_post(self):
		"""
		Tests post request on '/bucketlists/<int:id>/items/'.
		"""

		token = register_and_login_user(self.client)
		bucketlist = {
			'name': self.fake.name()
		}

		# create a bucketlist first
		response = self.client.post('/bucketlists/', data=bucketlist, headers={'username': token})
		resp_dict = json.loads(response.data)
		buck_id = resp_dict.get('id')

		# then create an item in that bucketlist
		item = {
			'name': self.fake.name()
		}
		response = self.client.post('/bucketlists/' + str(buck_id) + '/items/', data=item, headers={'username': token})
		self.assertEqual(response.status, '201 CREATED')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('name'), item.get('name'))
		self.assertEqual(resp_dict.get('id'), 1)

		# create item in bucketlist that doesn't exist
		item = {
			'name': self.fake.name()
		}
		response = self.client.post('/bucketlists/2/items/', data=item, headers={'username': token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "Bucket of id 2 doesn't exist")