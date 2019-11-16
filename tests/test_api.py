def test_info(client):

    url = "/"
    resp = client.get(url)

    assert resp.status_code == 200


def test_upload(client):
    import io

    url = "/upload"
    data = dict(myfile=(io.BytesIO(b"123456"), "./test.txt"))
    resp = client.post(url, content_type="multipart/form-data", data=data)

    assert resp.status_code == 200
    assert resp.data == b"ok!"
