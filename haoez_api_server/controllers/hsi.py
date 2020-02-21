import datetime
import json
import os
import sys
from haoez_api_server import db
import requests
from flask import abort, jsonify, request, send_from_directory, Blueprint
from sqlalchemy.sql import select
from haoez_api_server.models import keylist

hsi = Blueprint("hsi", __name__, url_prefix="/hsi")


@hsi.route("", methods=["GET"])
def hsi_list():
    try:
        t = keylist.keylist(db.metadata)
        res = db.session.query(t).all()
        return jsonify(
            {
                "desc": json.loads(str(t.c).replace("keylist.", "").replace("'", '"')),
                "result": res,
            }
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return "<h1>Something is broken.</h1>"


@hsi.route("", methods=["POST"])
def hsi_file_post():

    try:
        time_now = datetime.datetime.now()
        time_now = time_now.strftime("%Y-%m-%d_%H_%M_%S")
        f = request.files["file"]
        camera_type = request.values["camera_type"]
        sample_name = request.values["sample_name"]
        res = f.filename
        if not os.path.isdir("./data/"):
            os.mkdir("./data/")

        filename = camera_type + "_" + sample_name + "_" + time_now
        f.save("./data/" + filename)

        ins = (
            keylist.keylist(db.metadata)
            .insert()
            .values(
                Camera_name=camera_type,
                File_name=res,
                File_path=filename,
                Sample_name=sample_name,
            )
        )
        conn = db.engine.connect()
        conn.execute(ins)
        return "ok"
    except Exception as e:
        print(e, file=sys.stderr)
        return e


@hsi.route("/<id>", methods=["GET"])
def hsi_file_get(id):
    t = keylist.keylist(db.metadata)
    res = select([t.c.File_path]).where(t.c.Keylist_id == id)
    conn = db.engine.connect()
    res = conn.execute(res).fetchone()

    if res is None:
        return abort(404)
    else:
        root_dir = os.path.dirname(os.getcwd())
        return send_from_directory(
            os.path.join(root_dir, "haoez_api_server", "data"), res[0]
        )
