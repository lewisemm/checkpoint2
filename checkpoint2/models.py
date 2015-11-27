import os
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BucketList(Base):
	__tablename__ = 'bucketlist'

	# def __init__(self, name, created_by):
	# 	self.name = name
	# 	self.created_by=created_by

	buck_id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	date_created = Column(DateTime, nullable=False, default=func.now())
	date_modified = Column(DateTime, nullable=False, default=func.now())
	created_by = Column(String(100), nullable=False, default='Unauthenticated')

class Item(Base):
	__tablename__ = 'item'
	
	item_id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	date_created = Column(DateTime, default=func.now())
	date_modified = Column(DateTime, default=func.now())
	done = Column(Boolean, default=False)
	bucket_id = Column(Integer, ForeignKey('bucketlist.buck_id'))
	bucketlist = relationship('BucketList')

if __name__ == '__main__':
	engine = create_engine('sqlite:///api.db', echo=True)
	Base.metadata.create_all(engine)
