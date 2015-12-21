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
