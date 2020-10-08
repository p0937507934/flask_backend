import json
import os
import sys

from flask import Blueprint, jsonify, request, send_from_directory

classify = Blueprint("classify", __name__, url_prefix="/classify")

# 檢查放光譜資料的資料夾
tmp_path = "./haoez_api_server/classify_temp"
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path + "/data")
    os.makedirs(tmp_path + "/result")


@classify.route("/<hsi_type>", methods=["POST"])
def post_classify(hsi_type):
    try:
        w = request.files["white"]
        b = request.files["dark"]
        s = request.files["sample"]
        s_d = request.files["sample_dark"]

        from haoez_api_server import methods
        import time

        print("Start classify")
        sTime = time.time()
        img_path = getattr(methods, str(hsi_type))(w, b, s, s_d)
        print(time.time() - sTime, file=sys.stderr)
        return jsonify({"result": "ok!", "url": img_path})
    except Exception as e:
        print("Outer")
        print(e, file=sys.stderr)
        return jsonify({"result": "bad!", "msg": str(e)}), 400


@classify.route("/<hsi_type>/ref", methods=["POST"])
def post_classify_ref(hsi_type):
    try:
        ref_hdr = request.files["ref_hdr"]
        ref_raw = request.files["ref_raw"]

        ref_hdr.save("./haoez_api_server/classify_temp/data/" + ref_hdr.filename)
        ref_raw.save("./haoez_api_server/classify_temp/data/" + ref_raw.filename)

        from haoez_api_server import methods

        img_path = getattr(methods, str(hsi_type))(
            None,
            None,
            None,
            None,
            ref_raw_path="./haoez_api_server/classify_temp/data/" + ref_raw.filename,
            ref_hdr_path="./haoez_api_server/classify_temp/data/" + ref_hdr.filename,
        )
        return jsonify({"result": "ok!", "url": img_path})
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({"result": "bad!", "msg": str(e)}), 400


@classify.route("/result", methods=["GET"])
def get_result():
    filename = request.args.get("filename")
    print(filename, file=sys.stderr)
    return send_from_directory("./classify_temp/result/", filename)
