import os

from flask import Flask, render_template, Markup, request, redirect, url_for, flash, g, abort
from flask.json import jsonify

from flask_restful import Resource, Api, reqparse, fields, marshal_with

from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, MetaData, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

import models

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

@app.route('/user/registration', methods=['GET', 'POST'])
def registration():
	if request.method == 'GET':
		return render_template('register.html', error=None)
	elif request.method == 'POST':
		try:
			json_data = request.get_json()
			username = str(json_data['username'])
			password = str(json_data['password'])
			if username is None or password is None:
				return render_template('register.html', error='Username and/or password missing!')
			exists = manager.query(models.User).filter_by(username = username).first()
			if exists:
				return render_template('register.html', error='User already exists!')
			user = models.User(username=username)
			user.hash_password(password)
			manager.add(user)
			manager.commit()
			return render_template('register.html', error='User successfully registered!')
		except Exception as e:
			return render_template('register.html', error=e)


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
		return bucket

	@auth.login_required
	@marshal_with(bucketlist_fields)
	def get(self, limit=20):
		result = manager.query(models.BucketList).order_by(desc(models.BucketList.date_created)).all()
		return result
		
api.add_resource(BucketList, '/bucketlists/')

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
				return jsonify(access_denied), 401
		else:
			return jsonify({'message': 'That bucket list id doesnt exist'}), 404

	@auth.login_required
	@marshal_with(bucketlist_fields)
	def get(self, id):
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			return bucketlist, 200
		else:
			return jsonify({'message': 'Bucket of id ' + str(id) + ' doesnt exist'}), 404
	
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
				return jsonify({'message': 'Bucket of id ' + str(id) + ' has been deleted'})
			else:
				pass
				return jsonify(access_denied)
		else:
			return jsonify({'message': 'Bucket of id ' + str(id) + ' doesnt exist'})

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
			parser = reqparse.RequestParser()
			parser.add_argument('name')
			args = parser.parse_args()
			name = args['name']

			item = models.Item(name=name, bucket_id=bucketlist.buck_id)
			manager.add(item)
			manager.commit()

			# return jsonify({'message': 'Item added to bucketlist id ' + str(id)}), 201
			return item, 201
		else:
			return jsonify({'bucketlist': 'Bucket of id ' + str(id) + ' doesnt exist'})

api.add_resource(BucketListItems, '/bucketlists/<int:id>/items/')


class BucketListItemsID(Resource):
	@auth.login_required
	def put(self, id, item_id):
		# check if bucketlist exists
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				json_data = request.get_json()
				item = manager.query(models.Item).filter_by(item_id=item_id).first()
				item.name = json_data['name']
				item.date_modified = func.now()
				if json_data['done'] == 'True':
					item.done = True
				elif json_data['done'] == 'False':
					item.done = False
				manager.add(item)
				manager.commit()
				return jsonify({'message': 'Item of id ' + str(item_id) + ' from bucket of id ' + str(id) + ' has been updated'})
			else:
				return jsonify(access_denied)
		else:
			return jsonify({'message': 'Bucket of id ' + str(id) + ' doesnt exist'})


	@auth.login_required
	def delete(self, id, item_id):
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		if bucketlist:
			if is_bucketlist_owner(bucketlist):
				if is_bucketlist_owner(bucketlist):
					item = manager.query(models.Item).filter_by(item_id=item_id, bucket_id=bucketlist.buck_id).first()
					if item:
						manager.delete(item)
						manager.commit()

						return jsonify({'message': 'Item of id ' + str(item_id) + ' in bucket of id ' + str(id) + ' has been deleted'})
					else:
						return jsonify({'message': 'Item of id ' + str(item_id) + ' in bucket of id ' + str(id) + ' doesnt exist'})
				else:
					return jsonify({'message': 'Item of id ' + str(item_id) + ' in bucket of id ' + str(id) + ' doesnt exist'})
			else:
				return jsonify(access_denied)
		else:
			return jsonify({'message': 'Bucket of id ' + str(id) + ' doesnt exist'})

api.add_resource(BucketListItemsID, '/bucketlists/<int:id>/items/<int:item_id>')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', error=None)
	
	elif request.method == 'POST':
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
				return jsonify({'token': decoded}), 200
			else:
				return render_template('login.html', error='Invalid password!'), 400
		else:
			return render_template('login.html', error='That username does not exist!'), 400
		
@app.route('/auth/logout', methods=['GET'])
@auth.login_required
def logout():

	if request.method == 'GET':
	    # logout_user()
	    pass
	return render_template('logout.html', current_user)
    
if __name__ == '__main__':
	app.run()
