import json
import os
import sys

from flask import Blueprint, jsonify, request, send_from_directory

coffee = Blueprint("coffee", __name__, url_prefix="/coffee")


@coffee.route("/classify", methods=["POST"])
def demo():
    try:
        w = request.files["white"]
        b = request.files["dark"]
        s = request.files["sample"]
        s_d = request.files["sample_dark"]

        from haoez_api_server import demo
        import time
        print("Start classify")
        sTime = time.time()
        img_path = demo.coffee(w, b, s, s_d)
        print(time.time() - sTime, file=sys.stderr)
        return jsonify({"result": "ok!", "url": img_path})
    except Exception as e:
        print("Outer")
        print(e, file=sys.stderr)
        return jsonify({"result": "bad!", "msg": str(e)})


@coffee.route("/classify/ref", methods=["POST"])
def demo_ref():
    try:
        ref_hdr = request.files["ref_hdr"]
        ref_raw = request.files["ref_raw"]

        ref_hdr.save("./haoez_api_server/coffee_demo/data/" + ref_hdr.filename)
        ref_raw.save("./haoez_api_server/coffee_demo/data/" + ref_raw.filename)

        from haoez_api_server import demo

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


@coffee.route("/result", methods=["GET"])
def coffee_result():
    filename = request.args.get("filename")
    print(filename, file=sys.stderr)
    return send_from_directory("./coffee_demo/result/", filename)
