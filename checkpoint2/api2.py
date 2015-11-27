import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.json import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serial

import models

import ipdb

app = Flask(__name__)
api = Api(app)

engine = create_engine(os.environ['DATABASE_URL'])
session = sessionmaker()
session.configure(bind=engine)
manager = session()

# 
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

class BucketList(Resource):
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
		buckets = manager.query(models.BucketList).all()
		if buckets:
			return jsonify(json_list = manager.query(models.BucketList).all())
		else:
			return {'message': 'Nothing to see here'}

api.add_resource(BucketList, '/BucketList')

if __name__ == '__main__':
	app.run(debug=True)