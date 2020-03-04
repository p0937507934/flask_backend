# def test_info(client):

#     url = "/api"
#     resp = client.get(url)

#     assert resp.status_code == 200


def test_file_post(client):
    import io

    url = "/file"
    data = dict(myfile=(io.BytesIO(b"123456"), "./test.txt"))
    resp = client.post(url, content_type="multipart/form-data", data=data)

    assert resp.status_code == 200
    assert resp.data == b"ok!"


def test_file_get(client):

    url = "/file"
    data = dict(filename="test.txt")
    resp = client.get(url, query_string=data)

    assert resp.status_code == 200
    assert resp.data == b"123456"


def test_repository(client):
    import json

    url = "/repository"
    data = json.dumps(dict(num=1))
    resp = client.post(url, content_type="application/json", data=data)

    assert resp.status_code == 200
    resp = resp.get_json()
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert isinstance(resp[0], dict)
