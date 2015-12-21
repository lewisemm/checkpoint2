import json

from test_base_class import TestBaseClass, register_and_login_user

class TestRegistrationLoginLogout(TestBaseClass):
	
	def test_registration(self):
		"""
		Test the registration of a new user.
		"""
		response = self.client.post('/user/registration', data={'username': self.fake.user_name(), 'password': self.fake.password()})
		self.assertTrue('User successfully registered!' in response.data)
		self.assertEqual(response.status, '201 CREATED')

	def test_login_no_user_account(self):
		"""
		Test the login attempt from non existent user.
		"""
		response = self.client.post('/auth/login', data={'username': self.fake.user_name(), 'password': self.fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')

	def test_login_invalid_password(self):
		"""
		Test the login attempt from existing user, wrong password.
		"""
		username = self.fake.user_name()
		password = self.fake.password()

		# register the user
		response = self.client.post('/user/registration', data={'username':username, 'password':password})
		# log the user
		response = self.client.post('/auth/login', data={'username':username, 'password': self.fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')

	def test_successful_login(self):
		"""
		Test a successful login attempt.
		"""
		username = self.fake.user_name()
		password = self.fake.password()

		# register the user
		response = self.client.post('/user/registration', data={'username':username, 'password':password})
		# log the user
		response = self.client.post('/auth/login', data={'username':username, 'password':password})
		self.assertEqual(response.status, '200 OK')
		self.assertTrue('token' in response.data)

if __name__ == '__main__':
	unittest.main()