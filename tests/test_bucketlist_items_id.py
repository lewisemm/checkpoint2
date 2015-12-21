from test_base_class import TestBaseClass, register_and_login_user
import json

def create_bucketlist_and_item(**kwargs):
	# create the bucketlist
	bucketlist = {
		'name': kwargs.get('fake').name()
	}
	response = kwargs.get('client').post('/bucketlists/',
										data=bucketlist,
										headers={'username': kwargs.get('username')}
										)
	resp_dict = json.loads(response.data)
	buck_id = resp_dict.get('id')

	# create the item in the bucketlist
	item = {
		'name': kwargs.get('fake').name()
	}
	response = kwargs.get('client').post('/bucketlists/' + str(buck_id) + '/items/',
										data=item,
										headers={'username': kwargs.get('username')}
										)

	resp_dict = json.loads(response.data)
	return resp_dict.get('name')	

class TestBucketListItemsID(TestBaseClass):

	def test_bucketlist_items_id_unauthenticated(self):
		"""
		Test unauthenticated put and delete request to url '/bucketlists/<int:id>/items/<int:item_id>'.
		"""
		response = self.client.put('/bucketlists/1/items/1')
		self.assertEqual(response.status, '401 UNAUTHORIZED')
		self.assertTrue('Unauthorized Access' in response.data)

		response = self.client.delete('/bucketlists/1/items/1')
		self.assertEqual(response.status, '401 UNAUTHORIZED')
		self.assertTrue('Unauthorized Access' in response.data)

	def test_bucketlist_items_id_method_not_allowed(self):
		"""
		Test get and post (not allowed) request to url '/bucketlists/<int:id>/items/<int:item_id>'.
		"""
		response = self.client.get('/bucketlists/1/items/1')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

		response = self.client.post('/bucketlists/1/items/1')
		self.assertEqual(response.status, '405 METHOD NOT ALLOWED')

	def test_bucketlist_items_id_put_method(self):
		"""
		Test put request to url '/bucketlists/<int:id>/items/<int:item_id>'.
		"""

		token = register_and_login_user(self.client)

		updated_item = {
			'name': self.fake.name(),
			'done': 'True'
		}

		old_item_name = create_bucketlist_and_item(fake=self.fake, client=self.client, username=token)

		response = self.client.put('/bucketlists/1/items/1', data=updated_item, headers={'username': token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertNotEqual(resp_dict.get('name'), old_item_name)
		self.assertEqual(resp_dict.get('name'), updated_item.get('name'))

	def test_bucketlist_items_id_put_method_non_existent(self):
		"""
		Test put request to a bucketlist that doesn't exist.
		url: '/bucketlists/<int:id>/items/<int:item_id>'.
		"""

		token = register_and_login_user(self.client)

		updated_item = {
			'name': self.fake.name(),
			'done': 'True'
		}

		response = self.client.put('/bucketlists/2/items/1', data=updated_item, headers={'username': token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "Bucket of id 2 doesn't exist")

	def test_bucketlist_items_id_delete_method(self):
		"""
		Test delete request to url '/bucketlists/<int:id>/items/<int:item_id>'.
		Also test delete response once item has been deleted and is non-existent.
		"""

		token = register_and_login_user(self.client)

		item_name = create_bucketlist_and_item(fake=self.fake, client=self.client, username=token)

		# expect delete
		response = self.client.delete('/bucketlists/1/items/1', headers={'username': token})
		self.assertEqual(response.status, '200 OK')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "Item of id 1 in bucketlist of id 1 has been deleted")

		# expect item doesn't exist
		response = self.client.delete('/bucketlists/1/items/1', headers={'username': token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "Item of id 1 in bucketlist of id 1 doesn't exist")

	def test_bucketlist_items_id_delete_method_non_existent(self):
		"""
		Test delete request to url '/bucketlists/<int:id>/items/<int:item_id>'
		when non-existent bucketlist id is specified.
		"""

		token = register_and_login_user(self.client)

		item_name = create_bucketlist_and_item(fake=self.fake, client=self.client, username=token)


		# expect item doesn't exist
		response = self.client.delete('/bucketlists/2/items/1', headers={'username': token})
		self.assertEqual(response.status, '404 NOT FOUND')
		resp_dict = json.loads(response.data)
		self.assertEqual(resp_dict.get('message'), "Bucket of id 2 doesn't exist")