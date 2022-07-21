from .conftest import *
from flask import url_for


def test_get_request_index_should_succeed(client):
    url = url_for('landing.index')
    response = client.get(url)
    assert b"<title>Home</title>" in response.data
    assert response.status_code == 200
