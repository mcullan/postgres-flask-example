import datetime
import os

from flask import Flask
from models import Lost_Claimed, Subcategory

import sqlalchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = sqlalchemy.create_engine(DATABASE_URL)
session_gen = sessionmaker(bind=engine)
session = session_gen()

# a simple page that says hello
@app.route('/')
def index():
    lost_claimed = (session
        .query(
            Lost_Claimed.entry_time,
            Lost_Claimed.lost, 
            Lost_Claimed.claimed,
            )
        .order_by(sqlalchemy.desc(Lost_Claimed.entry_time))
        .limit(5))

    entry_time, lost, claimed = lost_claimed[0]

    time = entry_time.strftime('%Y-%m-%d %H:%M:%S')



    return time + ': ' + str((lost, claimed))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)