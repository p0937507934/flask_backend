import sys

import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

from __init__ import __version__

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


@app.route("/db/<table_name>")
def db_table(table_name):
    try:

        from sql import table
        import json

        t = getattr(table, table_name)(db.metadata)
        res = db.session.query(t).all()
        return jsonify(
            {
                "desc": json.loads(
                    str(t.c).replace(table_name + ".", "").replace("'", '"')
                ),
                "result": res,
            }
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return "<h1>Something is broken.</h1>"


@app.route("/file", methods=["POST"])
def file_post():
    try:
        # --debug--
        # 檢查當下沒有data路徑 就用OS新建
        import os

        if not os.path.isdir("./data/"):
            os.mkdir("./data/")
        # --debug--
        f = request.files["myfile"]
        f.save("./data/" + f.filename)
        return "ok!"
    except Exception as e:
        print(e, file=sys.stderr)
        return e


@app.route("/file", methods=["GET"])
def file_get():
    filename = request.args.get("filename")
    print(filename, file=sys.stderr)
    return send_from_directory("../data/", filename)


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
        # img_name = ""
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
