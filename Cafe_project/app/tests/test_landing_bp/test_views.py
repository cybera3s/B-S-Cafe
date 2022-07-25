from .conftest import *
from flask import url_for


def test_(client, app):
    with app.test_request_context():
        res = client.get('/')
        print(res)


# def test_get_request_index_should_succeed(client):
#     url = url_for('landing.index')
#     response = client.get(url)
#     assert b"<title>Home</title>" in response.data
#     assert response.status_code == 200

#
# def test_post_request_index_should_fail(client):
#     url = url_for('landing.index')
#     response = client.post(url)
#     assert response.status_code == 405
#
#
# def test_get_request_index_should_have_table_context(client, captured_templates):
#     url = url_for('landing.index')
#     response = client.get(url)
#
#     template, context = captured_templates[0]
#
#     assert 'tables' in context
#     assert template.name == "landing/index.html"
