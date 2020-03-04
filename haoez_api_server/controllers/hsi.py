import datetime
import json
import os
import sys
from haoez_api_server import db

import requests
from flask import abort, jsonify, request, send_from_directory, Blueprint, send_file
from sqlalchemy.sql import select
from haoez_api_server.models import keylist

hsi = Blueprint("hsi", __name__, url_prefix="/hsi")


@hsi.route("", methods=["GET"])
def hsi_list():

    try:

        res = keylist.keylist.query.all()
        print(type(res))
        print(type(jsonify([r.to_json() for r in res])))
        return jsonify([r.to_json() for r in res])

    except Exception as e:
        print(e, file=sys.stderr)
        return "<h1>Something is broken.</h1>"


@hsi.route("/post", methods=["POST"])
def hsi_file_post():

    try:
        time_now = datetime.datetime.now()
        time_now = time_now.strftime("%Y-%m-%d_%H_%M_%S")
        f = request.files["file"]

        camera_type = request.values["camera_type"]
        sample_name = request.values["sample_name"]
        res = f.filename
        filename_extension = res.split(".")
        if not filename_extension[1] == "npz":
            return abort(404)

        if not os.path.isdir("./data/"):
            os.mkdir("./data/")

        filename = (
            camera_type
            + "_"
            + sample_name
            + "_"
            + time_now
            + "."
            + filename_extension[1]
        )
        f.save("./data/" + filename)

        ins = keylist.keylist(
            Camera_name=camera_type,
            File_name=res,
            File_path=filename,
            Sample_name=sample_name,
        )
        db.session.add(ins)
        db.session.commit()
        db.session.close()
        return "file already upload"
    except Exception as e:
        print(e, file=sys.stderr)
        return e


@hsi.route("/<id>", methods=["GET"])
def hsi_file_get(id):
    conn = db.engine.connect()
    res = select([keylist.keylist]).where(keylist.keylist.Keylist_id == id)
    result = conn.execute(res).fetchone()
    if id == "-1":

        return str(result)
    # return str(result)
    elif result is None:

        return abort(404)

    else:

        root_dir = os.path.dirname(os.getcwd())
        path = os.path.join(root_dir, "haoez_api_server", "data", str(result[3]))

        return send_file(path, as_attachment=True)

