from .conftest import *
from flask import url_for


def test_get_request_index_should_succeed(client):
    url = url_for('landing.index')
    response = client.get(url)
    assert b"<title>Home</title>" in response.data
    assert response.status_code == 200


def test_post_request_index_should_fail(client):
    url = url_for('landing.index')
    response = client.post(url)
    assert response.status_code == 405