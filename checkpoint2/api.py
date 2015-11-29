import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.json import jsonify
from flask.ext.httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

import ipdb

import models

app = Flask(__name__)
api = Api(app)

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///api.db')
session = sessionmaker()
session.configure(bind=engine)
manager = session()

@auth.verify_password
def verify_password(username_or_token, password):

	user = models.User.verify_auth_token(username_or_token)

	if not user:
		user = manager.query(models.User).filter_by(username = username_or_token).first()

		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

class NewUser(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('username', type=str, help='Username')
			parser.add_argument('password', type=str, help='Password')

			args = parser.parse_args()
			username = args['username']
			password = args['password']

			if username is None or password is None:
							return {'message': 'Some arguments missing'}
			if manager.query(models.User).filter_by(username = username).first() is not None:
							return {'message': 'User already exists'}
			user = models.User(username = username)
			user.hash_password(password)
			manager.add(user)
			manager.commit()

			return {'message': 'User created successfully'}
		except Exception as e:
			return {'error': str(e)}

api.add_resource(NewUser, '/user/registration')

class BucketList(Resource):
	@auth.login_required
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('name', type=str, help='Name of the bucket list')
			parser.add_argument('created_by', type=str, help='Name of the user who created bucket list')

			args = parser.parse_args()
			name = args['name']
			created_by = args['created_by']

			bucket = models.BucketList(name=name, created_by=created_by)
			# ipdb.set_trace()
			manager = session()
			manager.add(bucket)
			manager.commit()

			return {'message': 'successful post'}
		except Exception as e:
			return {'error': str(e)}

	def get(self):
		result = manager.query(models.BucketList).all()
		res_json = []
		for bucket in result:
			current_bucket = {}
			current_bucket['id'] = bucket.buck_id
			current_bucket['name'] = bucket.name
			current_bucket['items'] = []
			current_bucket['date_created'] = str(bucket.date_created)
			current_bucket['date_modified'] = str(bucket.date_modified)
			current_bucket['created_by'] = bucket.created_by

			res_json.append(current_bucket)

		return ({'bucketlist': res_json})

api.add_resource(BucketList, '/bucketlist')

class Tokens(Resource):
	@auth.login_required
	def get(self):
		token = g.user.generate_auth_token()
		return jsonify({'token': token.decode('ascii')})

api.add_resource(Tokens, '/user/token')
if __name__ == '__main__':
	app.run(debug=True)
