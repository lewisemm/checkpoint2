import unittest

from app import app, db
# from flask.ext.testing import TestCase

class TestBucketList(unittest.TestCase):

	# def create_app(self):
	# 	app = Flask(__name__)
	# 	app.config['TESTING'] = True
	# 	return app

	def setUp(self):
		"""
		Creates a user account then retrieves a token that will be used to perform the test methods listed below.
		Also creates a default bucketlist.
		"""
		app.config['TESTING'] = True
		app.config['DATABASE_URL_TEST'] = 'mysql://admin:admin@127.0.0.1:3306/checkpoint2_test'
		db.create_all()
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_login(self):
		print self.app

	# def test_logout(self):
	# 	pass

	# def test_create_bucketlist(self):
	# 	pass
	# def test_list_created_bucketlist(self):
	# 	pass
	# def test_get_single_bucketlist(self):
	# 	pass
	# def test_update_single_bucketlist(self):
	# 	pass
	# def test_delete_single_bucketlist(self):
	# 	pass
	# def test_create_item_in_bucketlist(self):
	# 	pass
	# def test_update_item_in_bucketlist(self):
	# 	pass
	# def test_delete_item_in_bucketlist(self):
	# 	pass
if __name__ == '__main__':
    unittest.main()