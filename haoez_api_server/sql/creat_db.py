import table
import inspect
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database


engine = create_engine("mysql://hsipl:211@140.125.45.162/haoez_db")
metadata = MetaData()

if not database_exists(engine.url):
    create_database(engine.url)

all_tables = inspect.getmembers(table, inspect.isfunction)
tables = []
for t in all_tables:
    tables.append(getattr(table, t[0])(metadata))

metadata.create_all(engine)
