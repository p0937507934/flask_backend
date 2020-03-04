import pytest

def test_info(client):

    url = "/api"
    resp = client.get(url)
    assert resp.status_code == 200 or 308

def test_db(client):

    url="/api/db"
    resp=client.get(url)

    assert resp.status_code==200

