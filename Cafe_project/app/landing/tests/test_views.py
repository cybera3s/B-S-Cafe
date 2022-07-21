from .conftest import *


def test_get_request_root_should_succeed(client):
    response = client.get("/")
    assert "<title>Home</title>" in response.get_data(as_text=True)
    assert response.status_code == 200
