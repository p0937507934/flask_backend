from haoez_api_server import db
from haoez_api_server.models import keylist
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


engine = create_engine("mysql+pymysql://hsipl:211@140.125.45.162/haoez_db")
if not database_exists(engine.url):
    create_database(engine.url)

db.create_all()
