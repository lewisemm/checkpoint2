import os

from flask import Flask, request

from flask_restful import Resource, Api, reqparse, fields, marshal

from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, MetaData, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

from sqlalchemy_paginator import Paginator
from sqlalchemy_paginator.exceptions import EmptyPage

from models import models

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

api = Api(app)

auth = HTTPBasicAuth()

def init_session():
	"""
	This method configures and the app's current database and returns a session instance for use
	during CRUD operations.
	"""
	engine = create_engine(app.config.get('DATABASE_URL'))
	session = sessionmaker()
	session.configure(bind=engine)
	return session()

manager = init_session()

access_denied = {'message': 'Access denied!'}

def get_request_token():
	"""
	This method is used to retrieve a user's token from the username key of the request's header.
	"""
	return request.headers.get('username')

def is_bucketlist_owner(bucketlist):
	"""
	This method requires a bucketlist as an argument and checks its creator against the currently
	logged in user. If the current user has the same username as the created_by field of the bucketlist,
	this method returns True, otherwise, it returns False.
	"""
	token = get_request_token()
	# Ensure the owner od the bucketlist is the only one who can update it
	if models.User.verify_auth_token(token, manager).username == bucketlist.created_by:
		return True
	return False

def paging(fields, paginator, page):
	"""
	This method receives field, paginator and page arguments. It uses paginator and page arguments
	to paginate sqlalchemy query sets. The fields argument is used by marshal to return serialized results.
	"""
	try:
		return marshal(paginator.page(page).object_list, fields), 200 
	except EmptyPage:
		return {'message': "Page doesn't exist"}, 404

@auth.verify_password
def verify_password(username_or_token, password):
	"""
	The two arguments are not required in this function's body. They are simply there to avoid errors
	from the Flask-HTTPAuth library.
	The method is improvised to authenticate users from tokens instead of authentication via sessions
	as Flask-HTTPAuth originally intented.
	"""
	token = get_request_token()
	if token:
		user = models.User.verify_auth_token(token, manager)
		if user:
			if user.is_active:
				return user
			return False
		return False
	return False


class Registration(Resource):
	"""
	The class resource for the '/user/registration' endpoint.
	"""
	def post(self):
		"""
		This method facilitates the creation of new users in the Bucketlist API.
		""" 

		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('password')

		args = parser.parse_args()
		username = args['username']
		password = args['password']

		if username:
			if password:
				exists = manager.query(models.User).filter_by(username = username).first()
				if exists:
					return {'message': 'User already exists!'}, 403
				user = models.User(username=username)
				user.hash_password(password)
				manager.add(user)
				manager.commit()
				return {'message': 'User successfully registered!'}, 201
			# else:
			return {'message': 'Password missing!'}, 400
		# else:
		return {'message': 'Username missing!'}, 400
		
		

api.add_resource(Registration, '/user/registration')

class Limit(object):
	"""
	This class's attribute helps maintains the limit (content per page limit)
	across separate client page requests.
	"""
	limit = 20


class BucketList(Resource):
	"""
	The class resource for the '/bucketlists/' and /bucketlists/page/<int:page> endpoints'.
	"""

	def __init__(self):
		item_fields = {
			'id': fields.Integer(attribute='item_id'),
			'name': fields.String,
			'date_created': fields.String,
			'date_modified': fields.String,
			'done': fields.Boolean
		}

		self.bucketlist_fields = {
			'id': fields.Integer(attribute='buck_id'),
			'name': fields.String,
			'items': fields.Nested(item_fields),
			'date_created': fields.String,
			'date_modified': fields.String,
			'created_by': fields.String
		}
	
	@auth.login_required
	def post(self):
		"""
		This method facilitates the creation of new bucketlist items in the Bucketlist API.
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('name')

		args = parser.parse_args()
		name = args['name']

		token = get_request_token()
		created_by = models.User.verify_auth_token(token, manager).username

		bucket = models.BucketList(name=name, created_by=created_by)
		manager.add(bucket)
		manager.commit()
		return marshal(bucket, self.bucketlist_fields), 201

	@auth.login_required
	def get(self, page=1):
		"""
		This method facilitates the retrieval of existing bucketlists from the database.
		It also allows client specified pagination of results and also has a search bucketlist by name option.
		The default pagination of results is 20 items per page unless otherwise specified.
		"""
		
		try:
			# Get the limit specified by the client
			limit = int(request.args.get('limit', 0))
		except ValueError:
			# If limit specified by client isn't number type, ignore
			# that and default to 20
			limit = 20

		if limit:
			# if limit is greater than maximum, default to 100
			if limit > 100:
				Limit.limit = 100
			elif limit < 1:
			# if limit is <= 0, default to 20
				Limit.limit = 20
			else:
				Limit.limit = limit
		
		current_user = models.User.verify_auth_token(get_request_token(), manager)

		# the "search bucketlist by name" parameter
		q = request.args.get('q')
		if q:
			result = manager.query(models.BucketList).filter_by(name=q, created_by=current_user.username).order_by(desc(models.BucketList.date_created))
			if result:
				paginator = Paginator(result, Limit.limit)
				paged_response = paging(self.bucketlist_fields, paginator, page)
				return paged_response
			return {'message': "Bucketlist with name " + q + " doesn't exist"}, 404
		else:
			# when no parameter has been specified
			result = manager.query(models.BucketList).filter_by(created_by=current_user.username).order_by(desc(models.BucketList.date_created))
			paginator = Paginator(result, Limit.limit)
			# return the first page of the results by default
			paged_response = paging(self.bucketlist_fields, paginator, page)
			return paged_response

api.add_resource(BucketList, '/bucketlists/page/<int:page>', '/bucketlists/')


class BucketListID(Resource):
	"""
	This is the class resource for the bucketlist of the specified id at '/bucketlists/<int:id>' endpoint.
	"""

	def __init__(self):
		item_fields = {
			'id': fields.Integer(attribute='item_id'),
			'name': fields.String,
			'date_created': fields.String,
			'date_modified': fields.String,
			'done': fields.Boolean
		}

		self.bucketlist_fields = {
			'id': fields.Integer(attribute='buck_id'),
			'name': fields.String,
			'items': fields.Nested(item_fields),
			'date_created': fields.String,
			'date_modified': fields.String,
			'created_by': fields.String
		}

	@auth.login_required
	def put(self, id):
		"""
		This method facilitates the editing of the properties of the bucketlist of the specified id (i.e. name and date date modified).
		"""
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()

		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				parser = reqparse.RequestParser()
				parser.add_argument('name')

				args = parser.parse_args()
				bucketlist.name = args['name']
				bucketlist.date_modified = func.now()
				manager.add(bucketlist)
				manager.commit()
				return marshal(bucketlist, self.bucketlist_fields), 200
			return access_denied, 403
		return {'message': "That bucket list id doesn't exist"}, 404

	@auth.login_required
	def get(self, id):
		"""
		This method facilitates the retrieval of the bucketlist of the specified id and its
		associated items (if any).
		"""
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			return marshal(bucketlist, self.bucketlist_fields), 200
		return {'message': 'Bucket of id ' + str(id) + ' doesnt exist'}, 404
	
	@auth.login_required
	def delete(self, id):
		"""
		This method facilitates the complete removal of the bucketlist of the specified id
		from the database.
		"""
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()

		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				# delete all the items under this bucketlist first to prevent Integrity errors
				del_items = manager.query(models.Item).filter_by(bucket_id=id).all()
				if del_items:
					manager.delete(del_items)
					manager.commit()
				# delete the bucketlist itself
				manager.delete(bucketlist)
				manager.commit()
				
				return {'message': 'Bucket of id ' + str(id) + ' has been deleted'}, 200
			return access_denied, 403
		return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListID, '/bucketlists/<int:id>')


class BucketListItems(Resource):
	"""
	This is the class resource for the '/bucketlists/<int:id>/items/' endpoint.
	"""

	def __init__(self):
		self.item_fields = {
			'id': fields.Integer(attribute='item_id'),
			'name': fields.String,
			'date_created': fields.String,
			'date_modified': fields.String,
			'done': fields.Boolean
		}
	
	@auth.login_required
	def post(self, id):
		"""
		This method facilitates the addition of items inside a bucketlist.
		"""
		# check if bucketlist exists
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				parser = reqparse.RequestParser()
				parser.add_argument('name')
				args = parser.parse_args()
				name = args['name']

				item = models.Item(name=name, bucket_id=bucketlist.buck_id)
				manager.add(item)
				manager.commit()
				return marshal(item, self.item_fields), 201
			return access_denied, 403
		return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListItems, '/bucketlists/<int:id>/items/')


class BucketListItemsID(Resource):
	"""
	This is the class resource for the '/bucketlists/<int:id>/items/<int:item_id>' endpoint.
	"""

	def __init__(self):
		self.item_fields = {
			'id': fields.Integer(attribute='item_id'),
			'name': fields.String,
			'date_created': fields.String,
			'date_modified': fields.String,
			'done': fields.Boolean
		}

	@auth.login_required
	def put(self, id, item_id):
		"""
		This method facilitates the editing of an item of the specified item_id
		inside a bucketlist of the specified id.
		"""
		# check if bucketlist exists
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				parser = reqparse.RequestParser()
				parser.add_argument('name')
				parser.add_argument('done')
				args = parser.parse_args()

				item = manager.query(models.Item).filter_by(item_id=item_id).first()
				if args['name']:
					item.name = args['name']
				item.date_modified = func.now()
				if args['done']:
					if args['done'] == 'True':
						item.done = True
					elif args['done'] == 'False':
						item.done = False
				manager.add(item)
				manager.commit()
				return marshal(item, self.item_fields), 200
			return access_denied, 403
		return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

	@auth.login_required
	def delete(self, id, item_id):
		"""
		This method facilitates the complete removal of an item of id item_id from a bucketlist
		of id id.
		"""
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				item = manager.query(models.Item).filter_by(item_id=item_id, bucket_id=bucketlist.buck_id).first()
				if item:
					manager.delete(item)
					manager.commit()
					return {'message': 'Item of id ' + str(item_id) + ' in bucketlist of id ' + str(id) + ' has been deleted'}, 200
				return {'message': "Item of id " + str(item_id) + " in bucketlist of id " + str(id) + " doesn't exist"}, 404
			return access_denied, 403
		return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListItemsID, '/bucketlists/<int:id>/items/<int:item_id>')


class Login(Resource):
	"""
	This is the class resource for the '/auth/login' endpoint.
	"""

	def post(self):
		"""
		This method facilitates authentication of existing users and grants access
		to the Bucketlist API.
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('password')

		args = parser.parse_args()
		username = args.get('username')
		password = args.get('password')

		user = manager.query(models.User).filter_by(username=username).first()
		if user:
			if user.verify_password(password):
				token = user.generate_auth_token()
				decoded = token.decode('ascii')
				user.is_active = True
				manager.add(user)
				manager.commit()
				return {'token': decoded}, 200
			return {'message': 'Invalid password!'}, 400
		return {'message': 'That username does not exist!'}, 400

api.add_resource(Login, '/auth/login')
		

class Logout(Resource):

	@auth.login_required
	def get(self):
		user = models.User.verify_auth_token(get_request_token(), manager)
		user.is_active = False
		manager.add(user)
		manager.commit()
		return {'message': 'User ' + user.username + ' logged out'}, 200

		
api.add_resource(Logout, '/auth/logout')

	
if __name__ == '__main__':
	app.run()
