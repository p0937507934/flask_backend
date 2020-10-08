import pytest
import io
import numpy as np


def test_classify_raw(client):

    test_methods = ["peanut", "coffee", "test"]
    expect_status = [200, 200, 400]
    assert len(test_methods) == len(expect_status)

    for idx in range(len(test_methods)):

        url = "/classify/" + test_methods[idx]

        data = dict(
            white=(open("./tests/data/WHITE.RAW", "rb"), "WHITE.RAW"),
            dark=(open("./tests/data/RDARK.RAW", "rb"), "RDARK.RAW"),
            sample=(open("./tests/data/HPCCD.RAW", "rb"), "HPCCD.RAW"),
            sample_dark=(open("./tests/data/SDARK.RAW", "rb"), "SDARK.RAW"),
        )

        resp = client.post(url, content_type="multipart/form-data", data=data)
        assert resp.status_code == expect_status[idx]

        resp = resp.get_json()
        assert isinstance(resp, dict)


def test_classify_ref(client):

    test_methods = ["peanut", "test"]
    expect_status = [200, 400]
    assert len(test_methods) == len(expect_status)

    for idx in range(len(test_methods)):

        url = "/classify/" + test_methods[idx] + "/ref"

        data = dict(
            ref_raw=(open("./tests/data/1_RT_New.raw", "rb"), "1_RT_New.raw"),
            ref_hdr=(open("./tests/data/1_RT_New.hdr", "rb"), "1_RT_New.hdr"),
        )

        resp = client.post(url, content_type="multipart/form-data", data=data)
        assert resp.status_code == expect_status[idx]

        resp = resp.get_json()
        assert isinstance(resp, dict)


def test_classify_result(client):

    url = "/classify/result?filename="
    verify_result = [
        "HPCCD.RAW.png",
        "HPCCD.RAW_classes.png",
        "1_RT_New.raw_classes.png",
        "test",
    ]
    expect_status = [200, 200, 200, 404]
    assert len(verify_result)==len(expect_status)

    for idx in range(len(verify_result)):
        print("get:", verify_result[idx])
        resp = client.get(url + verify_result[idx])
        assert resp.status_code == expect_status[idx]
