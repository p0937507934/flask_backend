from flask import Flask, jsonify, request
import sys

from haoez_api_server import __version__

app = Flask("haoez_api_server")
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})


@app.route("/upload", methods=["post"])
def upload():
    try:
        #--debug--
        #檢查當下沒有data路徑 就用OS新建
        import os
        if not os.path.isdir("./data/"):
            os.mkdir("./data/")
        #--debug--
        f = request.files["myfile"]
        f.save("./data/" + f.filename)
        return "ok!"
    except Exception as e:
        print(e, file=sys.stderr)
        return e


if __name__ == "__main__":
    app.run()
