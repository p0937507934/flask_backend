import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")


@pytest.fixture(scope="function")
def app():
    from haoez_api_server.api import app

    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client
