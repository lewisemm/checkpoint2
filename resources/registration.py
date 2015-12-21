from flask_restful import Resource, reqparse
from api import init_session

class Registration(Resource):
	def post(self):
		manager = api.init_session()

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