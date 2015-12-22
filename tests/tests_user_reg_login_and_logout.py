from test_base_class import TestBaseClass, register_and_login_user

class TestRegistrationLoginLogout(TestBaseClass):

	def test_registration_no_password(self):
		"""
		Test the registration of a new user without a password.
		"""
		response = self.client.post('/user/registration', data={'username': self.fake.user_name()})
		self.assertEqual(response.status, '400 BAD REQUEST')
		self.assertTrue('Password missing!' in response.data)

	def test_registration_no_username(self):
		"""
		Test the registration of a new user without a username.
		"""
		response = self.client.post('/user/registration', data={'password': self.fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')
		self.assertTrue('Username missing!' in response.data)
		
	def test_registration_user_exists(self):
		"""
		Test the registration of a new user with a username that already exists.
		"""
		user1 = {
			'username': self.fake.user_name(),
			'password': self.fake.password()
		}
		# register the first user
		response = self.client.post('/user/registration', data=user1)

		user2 = {
			'username': user1.get('username'),
			'password': self.fake.password()
		}

		# register the second user with the first user's username
		response = self.client.post('/user/registration', data=user2)
		self.assertEqual(response.status, '403 FORBIDDEN')
		self.assertTrue('User already exists!' in response.data)
		
	def test_successful_registration(self):
		"""
		Test the registration of a new user.
		"""
		response = self.client.post('/user/registration', data={'username': self.fake.user_name(), 'password': self.fake.password()})
		self.assertTrue('User successfully registered!' in response.data)
		self.assertEqual(response.status, '201 CREATED')

	def test_login_non_existent(self):
		"""
		Test the login attempt from non existent user.
		"""
		response = self.client.post('/auth/login', data={'username': self.fake.user_name(), 'password': self.fake.password()})
		self.assertEqual(response.status, '400 BAD REQUEST')
		self.assertTrue('That username does not exist!' in response.data)

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
		self.assertTrue('Invalid password!' in response.data)

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

	def test_successful_logout(self):
		"""
		Test a successful logout attempt.
		"""

		token = register_and_login_user(self.client)

		# logout
		response = self.client.get('/auth/logout', headers={'username': token})
		self.assertEqual(response.status, '200 OK')
		self.assertTrue('logged out' in response.data)

		# Try to logout when just logged out
		response = self.client.get('/auth/logout', headers={'username': token})
		self.assertEqual(response.status, '401 UNAUTHORIZED')
		self.assertTrue('Unauthorized Access' in response.data)

if __name__ == '__main__':
	unittest.main()