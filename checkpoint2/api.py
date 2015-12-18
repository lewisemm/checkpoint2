import os

from flask import Flask, request

from flask_restful import Resource, Api, reqparse, fields, marshal_with

from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, MetaData, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

from models import models

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

api = Api(app)

auth = HTTPBasicAuth()

def init_session():
	engine = create_engine(app.config.get('DATABASE_URL'))
	session = sessionmaker()
	session.configure(bind=engine)
	return session()

manager = init_session()

access_denied = {'message': 'Access denied!'}

def get_request_token():
	return request.headers.get('username')

def is_bucketlist_owner(bucketlist):
	token = get_request_token()
	# Ensure the owner od the bucketlist is the only one who can update it
	if models.User.verify_auth_token(token, manager).username == bucketlist.created_by:
		return True
	else:
		return False

@auth.verify_password
def verify_password(username_or_token, password):
	token = get_request_token()
	if token:
		user = models.User.verify_auth_token(token, manager)
		if user:
			return user
		else:
			return False
	else:
		return False


class Registration(Resource):
	def post(self):

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
			else:
				return {'message': 'Password missing!'}, 400
		else:
			return {'message': 'Username missing!'}, 400
		
		user = models.User(username=username)
		user.hash_password(password)
		manager.add(user)
		manager.commit()
		return {'message': 'User successfully registered!'}, 201

api.add_resource(Registration, '/user/registration')


class BucketList(Resource):
	item_fields = {
		'id': fields.Integer(attribute='item_id'),
		'name': fields.String,
		'date_created': fields.String,
		'date_modified': fields.String,
		'done': fields.Boolean
	}

	bucketlist_fields = {
		'id': fields.Integer(attribute='buck_id'),
		'name': fields.String,
		'items': fields.Nested(item_fields),
		'date_created': fields.String,
		'date_modified': fields.String,
		'created_by': fields.String
	}
	
	@auth.login_required
	@marshal_with(bucketlist_fields)
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name')

		args = parser.parse_args()
		name = args['name']

		token = get_request_token()
		created_by = models.User.verify_auth_token(token, manager).username

		bucket = models.BucketList(name=name, created_by=created_by)
		manager.add(bucket)
		manager.commit()
		return bucket, 201

	@auth.login_required
	@marshal_with(bucketlist_fields)
	def get(self, limit=20, q=None):
		if q:
			result = manager.query(models.BucketList).filter_by(name=q).order_by(desc(models.BucketList.date_created)).all()
			if result:
				return result, 200
			else:
				return {'message': "Bucketlist with name " + q + " doesn't exist"}, 404
		else:
			result = manager.query(models.BucketList).order_by(desc(models.BucketList.date_created)).all()
			return result, 200

api.add_resource(BucketList, '/bucketlists/', '/bucketlists/<q>')


class BucketListID(Resource):
	item_fields = {
		'id': fields.Integer(attribute='item_id'),
		'name': fields.String,
		'date_created': fields.String,
		'date_modified': fields.String,
		'done': fields.Boolean
	}

	bucketlist_fields = {
		'id': fields.Integer(attribute='buck_id'),
		'name': fields.String,
		'items': fields.Nested(item_fields),
		'date_created': fields.String,
		'date_modified': fields.String,
		'created_by': fields.String
	}

	@auth.login_required
	@marshal_with(bucketlist_fields)
	def put(self, id):
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
				return bucketlist, 200
			else:
				return access_denied, 403
		else:
			return {'message': "That bucket list id doesn't exist"}, 404

	@auth.login_required
	@marshal_with(bucketlist_fields)
	def get(self, id):
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			return bucketlist, 200
		else:
			return {'message': 'Bucket of id ' + str(id) + ' doesnt exist'}, 404
	
	@auth.login_required
	def delete(self, id):
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
				
				# status codes cause an error that has something to do with serialization
				return {'message': 'Bucket of id ' + str(id) + ' has been deleted'}, 200
			else:
				pass
				return access_denied, 403
		else:
			return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListID, '/bucketlists/<int:id>')


class BucketListItems(Resource):
	item_fields = {
		'id': fields.Integer(attribute='item_id'),
		'name': fields.String,
		'date_created': fields.String,
		'date_modified': fields.String,
		'done': fields.Boolean
	}
	
	@auth.login_required
	@marshal_with(item_fields)
	def post(self, id):
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
				return item, 201
			else:
				return access_denied, 403
		else:
			return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListItems, '/bucketlists/<int:id>/items/')


class BucketListItemsID(Resource):
	@auth.login_required
	def put(self, id, item_id):
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
				return {'message': "Item of id " + str(item_id) + " from bucket of id " + str(id) + " has been updated"}, 200
			else:
				return access_denied, 403
		else:
			return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

	@auth.login_required
	def delete(self, id, item_id):
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				item = manager.query(models.Item).filter_by(item_id=item_id, bucket_id=bucketlist.buck_id).first()
				if item:
					manager.delete(item)
					manager.commit()
					return {'message': 'Item of id ' + str(item_id) + ' in bucketlist of id ' + str(id) + ' has been deleted'}, 200
				else:
					return {'message': "Item of id " + str(item_id) + " in bucketlist of id " + str(id) + " doesn't exist"}, 404
			else:
				return access_denied, 403
		else:
			return {'message': "Bucket of id " + str(id) + " doesn't exist"}, 404

api.add_resource(BucketListItemsID, '/bucketlists/<int:id>/items/<int:item_id>')


class Login(Resource):
	def post(self):
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
				return {'token': decoded}, 200
			else:
				return {'message': 'Invalid password!'}, 400
		else:
			return {'message': 'That username does not exist!'}, 400

api.add_resource(Login, '/auth/login')
		
@app.route('/auth/logout', methods=['GET'])
@auth.login_required
def logout():

	if request.method == 'GET':
	    # logout_user()
	    pass
	return render_template('logout.html', current_user)
    
if __name__ == '__main__':
	app.run()
