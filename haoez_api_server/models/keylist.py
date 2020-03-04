from haoez_api_server import db
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, create_engine
from sqlalchemy_utils import database_exists, create_database


class keylist(db.Model):
    Keylist_id = db.Column(Integer, primary_key=True, nullable=False)
    Camera_name = db.Column(VARCHAR(20), nullable=False)
    File_name = db.Column(VARCHAR(50), nullable=False)
    File_path = db.Column(VARCHAR(50), nullable=False)
    Sample_name = db.Column(VARCHAR(50), nullable=False)
    Sample_time = db.Column(TIMESTAMP(), nullable=False)
    __table_args__ = {'extend_existing': True}


    def to_json(self):
        if hasattr(self, '__table__'):
            return {i.name: getattr(self, i.name) for i in self.__table__.columns}
        raise AssertionError('<%r> does not have attribute for __table__' % self)


if __name__ == "__main__":
    if not database_exists(db.get_engine().url):
        create_database(db.get_engine().url)

    db.create_all()
    