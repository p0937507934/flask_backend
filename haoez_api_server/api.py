import datetime
import json
import os
import sys

import requests
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy_utils import database_exists

from __init__ import __version__
from sql import table_v2 as table

app = Flask("haoez_api_server")
app.config["DEBUG"] = True

# DB setting
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://hsipl:211@140.125.45.162/haoez_db"
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})


@app.route("/db")
def test_db():
    try:
        database_exists(db.engine.url)
        return "<h1>It works.</h1>"
    except Exception as e:
        print(e, file=sys.stderr)
        return "<h1>Something is broken.</h1>"


@app.route("/hsi", methods=["GET"])
def hsi_list():
    try:
        t = table.keylist(db.metadata)
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


@app.route("/hsi", methods=["POST"])
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
            table.keylist(db.metadata)
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


@app.route("/hsi/<id>", methods=["GET"])
def hsi_file_get(id):
    t = table.keylist(db.metadata)
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


@app.route("/repository", methods=["POST"])
def repository():
    json = request.get_json()
    print(json, file=sys.stderr)
    url = "https://api.github.com/repositories"
    resp = requests.get(url)
    resp = resp.json()
    resp = resp[0 : json["num"]]
    return jsonify(resp)


@app.route("/demo", methods=["GET", "POST"])
def demo():
    try:
        w = request.files["white"]
        b = request.files["dark"]
        s = request.files["sample"]
        s_d = request.files["sample_dark"]

        import demo

        img_path = demo.coffee(w, b, s, s_d)
        return jsonify({"result": "ok!", "url": img_path})
    except Exception as e:
        print("Outer")
        print(e, file=sys.stderr)
        return jsonify({"result": "bad!", "msg": str(e)})


@app.route("/demo/ref", methods=["GET", "POST"])
def demo_ref():
    try:
        ref_hdr = request.files["ref_hdr"]
        ref_raw = request.files["ref_raw"]

        ref_hdr.save("./haoez_api_server/coffee_demo/data/" + ref_hdr.filename)
        ref_raw.save("./haoez_api_server/coffee_demo/data/" + ref_raw.filename)

        import demo

        img_path = demo.coffee(
            None,
            None,
            None,
            None,
            ref_raw_path="./haoez_api_server/coffee_demo/data/" + ref_raw.filename,
            ref_hdr_path="./haoez_api_server/coffee_demo/data/" + ref_hdr.filename,
        )
        return jsonify({"result": "ok!", "url": img_path})
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"result": "bad!", "msg": str(e)})


@app.route("/coffee_result", methods=["GET"])
def coffee_result():
    filename = request.args.get("filename")
    print(filename, file=sys.stderr)
    return send_from_directory("./coffee_demo/result/", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
