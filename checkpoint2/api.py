import os

from flask import Flask, render_template, Markup, request, redirect, url_for, flash
from flask_restful import Resource, Api, reqparse
from flask.json import jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

import ipdb

import models
from forms import LoginForm

app = Flask(__name__)
api = Api(app)
app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)


engine = create_engine('sqlite:///api.db')
session = sessionmaker()
session.configure(bind=engine)
manager = session()

@login_manager.user_loader
def load_user(user_id):
	return manager.query(models.User).filter_by(id=user_id).first()

#@auth.verify_password
def verify_password(username_or_token, password):

	user = models.User.verify_auth_token(username_or_token)

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
			username = request.form['username']
			password = request.form['password']
			if username is None or password is None:
				return render_template('registration.html', error='Username and/or password missing!')
			if manager.query(models.User).filter_by(username = username).first() is not None:
				return render_template('registration.html', error='User already exists!')

			user = models.User(username=username)
			user.hash_password(password)
			manager.add(user)
			manager.commit()

			return render_template('registration.html', error='User successfully registered!')
		except Exception as e:
			return render_template('registration.html', error=e)

class BucketList(Resource):
	@login_required
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

	@login_required
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

@app.route('/login/token', methods=['GET'])
@login_required
def tokenize():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})


@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', error=None)
	
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = manager.query(models.User).filter_by(username=username).first()
		if not user:
			return render_template('login.html', error='That username does not exist!')
		elif user.verify_password(password):
			login_user(user)
			flash('Logged in successfully.')

        	return redirect(url_for('index'))
    	return render_template('login.html', error='Neither GET nor POST')
		
			
@app.route("/logout")
@login_required
def logout():
    logout_user()
   	return render_template('logout.html', error='None')

    
if __name__ == '__main__':
	app.run(debug=True)
