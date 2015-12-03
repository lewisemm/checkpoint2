import os

from flask import Flask, render_template, Markup, request, redirect, url_for, flash
from flask_restful import Resource, Api, reqparse
from flask.json import jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user

from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, MetaData, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

import ipdb

import models

app = Flask(__name__)
api = Api(app)
app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])

auth = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)


engine = create_engine(os.environ['DATABASE_URL'])
session = sessionmaker()
session.configure(bind=engine)
manager = session()

@login_manager.user_loader
def load_user(user_id):
	return manager.query(models.User).filter_by(id=user_id).first()

@auth.verify_password
def verify_password(username_or_token, password):

	user = models.User.verify_auth_token(username_or_token)
	ipdb.set_trace()

	if not user:
		user = manager.query(models.User).filter_by(username = username_or_token).first()

		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

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
	@login_required
	def post(self):
		try:
			json_data = request.get_json()
			for bucketlist in json_data:
				name = bucketlist['name']
				created_by = current_user.username
				bucket = models.BucketList(name=name, created_by=created_by)
				manager.add(bucket)
				manager.commit()
			

			return {'message': 'successful post'}
		except Exception as e:
			return {'error': str(e)}

	@auth.login_required
	def get(self, limit=20):

		result = manager.query(models.BucketList).order_by(desc(models.BucketList.date_created)).limit(limit)
		
		res_json = []
		for bucket in result:
			current_bucket = {}
			current_items = {}
			current_bucket['id'] = bucket.buck_id
			current_bucket['name'] = bucket.name

			item_in_bucket = manager.query(models.Item).filter(models.Item.bucket_id==bucket.buck_id).order_by(desc(models.Item.date_created)).all()
			current_bucket['items'] = []

			for item in item_in_bucket:
				current_items['id'] = item.item_id
				current_items['name'] = item.name
				current_items['date_created'] = str(item.date_created)
				current_items['date_modified'] = str(item.date_modified)
				current_items['done'] = item.done

			if current_items:
				current_bucket['items'].append(current_items)
				
			current_bucket['date_created'] = str(bucket.date_created)
			current_bucket['date_modified'] = str(bucket.date_modified)
			current_bucket['created_by'] = bucket.created_by

			res_json.append(current_bucket)

		return jsonify({'bucketlists': res_json})

api.add_resource(BucketList, '/bucketlists/')


class BucketListID(Resource):
	@login_required
	def put(self, id):
		try:
			json_data = request.get_json()

			bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
			
			if bucketlist:
				bucketlist.name = json_data['name']
				bucketlist.date_modified = func.now()
			
				manager.add(bucketlist)
				manager.commit()

				return {'message': 'Bucketlist updated successfully'}
			else:
				return {'message': 'That bucket list id doesnt exist'}

		except Exception as e:
			return {'error': str(e)}

	@login_required
	def get(self, id):
		result = manager.query(models.BucketList).filter_by(buck_id=id).first()
		
		if result:
			current_bucket = {}
			current_bucket['id'] = result.buck_id
			current_bucket['name'] = result.name
			current_bucket['items'] = []
			current_bucket['date_created'] = str(result.date_created)
			current_bucket['date_modified'] = str(result.date_modified)
			current_bucket['created_by'] = result.created_by
	
			return ({'bucketlist': current_bucket})
		else:
			return ({'bucketlist': 'Bucket of id ' + str(id) + ' doesnt exist'})
	
	@login_required
	def delete(self, id):
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()
		manager.delete(bucketlist)
		manager.commit()

		return {'message': 'bucketlist of id ' + str(id) + ' has been deleted'}

api.add_resource(BucketListID, '/bucketlists/<int:id>')


class BucketListItems(Resource):
	@login_required
	def post(self, id):

		# check if bucketlist exists
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()

		if bucketlist:
			json_data = request.get_json()
			name = json_data['name']
			item = models.Item(name=name, bucket_id=bucketlist.buck_id)
			manager.add(item)
			manager.commit()

			return ({'message': 'Item added to bucketlist id ' + str(id)})
		else:
			return ({'bucketlist': 'Bucket of id ' + str(id) + ' doesnt exist'})

api.add_resource(BucketListItems, '/bucketlists/<int:id>/items/')


class BucketListItemsID(Resource):
	@login_required
	def put(self, id, item_id):

		# check if bucketlist exists
		bucketlist = manager.query(models.BucketList).filter_by(buck_id=id).first()

		if bucketlist:

			json_data = request.get_json()

			item = manager.query(models.Item).filter_by(item_id=item_id).first()
			item.name = json_data['name']
			item.date_modified = func.now()
			item.done = json_data['done']

			manager.add(item)
			manager.commit()

			return ({'bucketlist': 'Item of id ' + str(item_id) + 'from bucket of id ' + str(id) + ' has been updated'})
		else:
			return ({'bucketlist': 'Bucket of id ' + str(id) + ' doesnt exist'})


	@login_required
	def delete(self, id, item_id):
		pass

api.add_resource(BucketListItemsID, '/bucketlists/<int:id>/items/<int:item_id>')

@app.route('/login/token', methods=['GET'])
def tokenize():
	token = current_user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})


@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html', error=None)

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', error=None)
	
	elif request.method == 'POST':

		username = request.form.get('username')
		password = request.form.get('password')

		user = manager.query(models.User).filter_by(username=username).first()

		if not user:
			return render_template('login.html', error='That username does not exist!')
		elif user.verify_password(password):

			if user.verify_password(password):
				login_user(user)
				return redirect(url_for('tokenize'))
			else:
				return render_template('login.html', error='Invalid password!')
		
@app.route('/auth/logout', methods=['GET'])
@login_required
def logout():

	if request.method == 'GET':
	    logout_user()
	return render_template('logout.html')
    
if __name__ == '__main__':
	app.run(debug=True)
