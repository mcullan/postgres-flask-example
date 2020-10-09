#! /Users/admin/anaconda3/envs/postgres-flask-example/bin/python3

import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String

from mta_lost_found import query_lost_found_api

DATABASE_URL = os.environ.get('DATABASE_URL')

# This creates a base we can inherit from
Base = declarative_base()

class Lost_Claimed(Base):
    __tablename__ = "lost_claimed"
    
    # sqlalchemy uses these names as the column names
    entry_time = Column(DateTime(timezone=True), primary_key=True)
    lost = Column(Integer)
    claimed = Column(Integer)
    
class Subcategory(Base):
    __tablename__ = 'subcategories'
    
    entry_time = Column(DateTime(timezone=True), primary_key=True)
    subcategory = Column(String, primary_key=True)
    category = Column(String, primary_key=True)
    count = Column(Integer)
    
def query_and_push(DATABASE_URL):
    lost_found = query_lost_found_api()

    lost = lost_found['lost']
    claimed = lost_found['claimed']
    subcategories = lost_found['subcategories']
    now = lost_found['now']


    engine = sqlalchemy.create_engine(DATABASE_URL)
    session_gen = sessionmaker(bind=engine)
    session = session_gen()
    entries = []


    for subcategory in subcategories:
        subcategory_name, category_name, count = subcategory

        entries.append(Subcategory(entry_time=now, 
                                   subcategory=subcategory_name, 
                                   category=category_name, 
                                   count=count))

    lost_claimed = Lost_Claimed(entry_time=now,
                            lost=lost,
                            claimed=claimed)

    session.add_all(entries)
    session.add(lost_claimed)

    session.commit()

if __name__ == '__main__':
    print(DATABASE_URL)
    print(sqlalchemy.__version__)
    query_and_push(DATABASE_URL)