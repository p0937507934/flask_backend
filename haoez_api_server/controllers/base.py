import sys

from flask import Blueprint, jsonify
# from sqlalchemy_utils import database_exists

base = Blueprint("base", __name__, url_prefix="/api")
# from haoez_api_server import db, __version__
from haoez_api_server import __version__

@base.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})


@base.route("/db")
def test_db():
    try:
        # TODO
        # database_exists(db.engine.url)
        # return "<h1>It works.</h1>"
        raise Exception('SQL didn\'t deploy!')
    except Exception as e:
        print(e, file=sys.stderr)
        return "<h1>Something is broken.</h1>", 404
