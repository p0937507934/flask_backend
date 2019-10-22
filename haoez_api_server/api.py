from flask import Flask, jsonify

from haoez_api_server import __version__

app = Flask("haoez_api_server")


@app.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})
