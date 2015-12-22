import os
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from flask import current_app
# from flask.ext.login import UserMixin

from passlib.apps import custom_app_context as pwd_context

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

class BucketList(Base):
	__tablename__ = 'bucketlist'

	buck_id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	date_created = Column(DateTime, nullable=False, default=func.now())
	date_modified = Column(DateTime, nullable=False, default=func.now())
	created_by = Column(String(100), nullable=False, default='Unauthenticated')
	items = relationship("Item")

class Item(Base):
	__tablename__ = 'item'
	
	item_id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	date_created = Column(DateTime, nullable=False, default=func.now())
	date_modified = Column(DateTime, nullable=False, default=func.now())
	done = Column(Boolean, default=False)
	bucket_id = Column(Integer, ForeignKey('bucketlist.buck_id'))
	bucketlist = relationship('BucketList')

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), index=True, unique=True)
	password_hash = Column(String(128))
	is_active = Column(Boolean, default=False)

	def hash_password(self, password):
		"""
		Makes use of passlib to hash clear text passwords from the client for storage on the database.
		custom_app_context hashing algorithm is used.
		"""
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		"""
		Comapres a clear text password from the client with the hashed password in the database
		and returns True if the password is correct.
		"""
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=600):
		"""
		Generates a timed token to be associated with the client for authentication purposes during request sending.
		Default expiration time is 10 minutes (600 sec) unless client specifies otherwise.
		"""
		s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id':self.id})

	@staticmethod
	def verify_auth_token(token, manager):
		"""
		Retrieves an id from the token and queries the database against this id to identify the user for authentication purposes.
		"""
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None

		user = manager.query(User).get(data['id'])
		return user

def init_db(db_url=None):
	"""
	Used to initialize configurations and create the database during the initial run of the app or during 
	execution of tests.
	"""
	if db_url:
		engine = create_engine(db_url)
	else:
		engine = create_engine(os.environ.get('DATABASE_URL'))
	Base.metadata.create_all(engine)

if __name__ == '__main__':
	init_db()