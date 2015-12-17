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

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id':self.id})

	@staticmethod
	def verify_auth_token(token, manager):
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
	if db_url:
		engine = create_engine(db_url)
	else:
		engine = create_engine(os.environ.get('DATABASE_URL'))
	Base.metadata.create_all(engine)

if __name__ == '__main__':
	init_db()