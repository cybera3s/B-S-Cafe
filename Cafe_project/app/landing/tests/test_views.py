from .conftest import *


def test_get_request_root_should_succeed(client):
    response = client.get("/")
    print(response)
    assert response.status_code == 200
