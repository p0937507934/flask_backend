import os

from flask import Flask

__version__ = "0.0.1.dev0"

app = Flask("haoez_api_server")
app.config["DEBUG"] = True


from haoez_api_server.controllers.base import base

app.register_blueprint(base)

from haoez_api_server.controllers.classify import classify

app.register_blueprint(classify)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
