def test_info(client):

    url = "/"
    resp = client.get(url)

    assert resp.status_code == 200
