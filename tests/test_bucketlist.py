from test_base_class import TestBaseClass, register_and_login_user
import json

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


if __name__ == '__main__':
	unittest.main()