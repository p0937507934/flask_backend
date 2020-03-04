import pytest
import io
from werkzeug.wrappers import Response


def test_hsi_list(client):
    url = "/hsi"
    resp = client.get(url)

    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_hsi_post(client):
    url = "/hsi/post"

    data = dict(
        file=(io.BytesIO(b"Fortesting"), "test.txt"),
        camera_type="test",
        sample_name="test",
    )

    resp = client.post(url, content_type="multipart/form-data", data=data)

    assert resp.status_code == 404


def test_hsi_get(client):
    url = "/hsi/-1"
    resp = client.get(url)
    assert resp.data == b"None"

