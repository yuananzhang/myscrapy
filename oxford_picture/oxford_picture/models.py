
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary

import settings

def db_connect():
	"""
	Performs database connection using database settings from settings.py.
	Returns sqlalchemy engine instance
	"""
	return create_engine(URL(**settings.DATABASE), encoding="utf-8")

DeclarativeBase = declarative_base()

def create_oxford_picture_table(engine):
	""""""
	DeclarativeBase.metadata.create_all(engine)

class OxfordPicture(DeclarativeBase):
	"""Sqlalchemy deals model"""
	__tablename__ = "oxford_picture"

	id = Column(Integer, primary_key=True)
	word = Column('word', String)
	img_url = Column('img_url', String)
	imgref_url = Column('imgref_url', String)
	picture = Column('picture', LargeBinary)
