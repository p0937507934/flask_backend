from flask import Flask, jsonify

from haoez_api_server import __version__

app = Flask("haoez_api_server")
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def info():
    return jsonify({"version": __version__})


if __name__ == "__main__":
    app.run()
