from flask import Flask, jsonify, request, send_from_directory
import sys
import requests

from haoez_api_server import __version__

app = Flask("haoez_api_server")
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})


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
    return send_from_directory('../data/', filename)


@app.route("/repository", methods=["POST"])
def repository():
    json = request.get_json()
    print(json, file=sys.stderr)
    url = "https://api.github.com/repositories"
    resp = requests.get(url)
    resp = resp.json()
    resp = resp[0 : json["num"]]
    return jsonify(resp)


if __name__ == "__main__":
    app.run()
