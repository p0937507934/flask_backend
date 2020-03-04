import os
import sys

import pytest


@pytest.fixture(scope="function")
def app():
    from haoez_api_server import app

    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client
