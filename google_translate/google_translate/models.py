# -*- coding: utf-8 -*-

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker

REMOTE_DATABASE = {'drivername': 'postgres',
                   'host': '182.92.220.225',
                   'port': '5432',
                   'username': 'admin',
                   'password': '314159',
                   'database': 'acenglish'}

def db_connect_remote():
    return create_engine(URL(**REMOTE_DATABASE), encoding="utf-8")

DeclarativeBase = declarative_base()

class RemoteTranslate(DeclarativeBase):
    __tablename__ = "translate"

    id = Column(Integer, primary_key=True)
    hash = Column('hash', String)
    english = Column('english', String)
    chinese = Column('chinese', String)

class RemoteDb(object):
    engine = db_connect_remote()
    def __init__(self):
        self.Session = sessionmaker(bind=self.engine)

    def query(self):
        return self.Session().query(RemoteTranslate).filter(RemoteTranslate.chinese==None).yield_per(100).enable_eagerloads(False)

    def update(self, obj):
        session = self.Session()
        try:
            session.query(RemoteTranslate).filter(RemoteTranslate.hash==obj.hash).update({RemoteTranslate.chinese:obj.chinese})
            session.commit()
        except Exception as e:
            print e
            session.rollback()
        finally:
            session.close()
