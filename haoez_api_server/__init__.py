from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = "0.0.1.dev0"

app = Flask("haoez_api_server")
app.config["DEBUG"] = True
# DB setting
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://hsipl:211@140.125.45.162/haoez_db"
db = SQLAlchemy(app)

from haoez_api_server.controllers.base import base
app.register_blueprint(base)

from haoez_api_server.controllers.hsi import hsi
app.register_blueprint(hsi)

from haoez_api_server.controllers.coffee import coffee
app.register_blueprint(coffee)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
