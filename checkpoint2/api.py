import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.json import jsonify

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

import ipdb

import models

app = Flask(__name__)
api = Api(app)

engine = create_engine('sqlite:///api.db')
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


api.add_resource(BucketList, '/BucketList')

if __name__ == '__main__':
	app.run(debug=True)
