from flask import url_for, redirect, make_response, request


def logout():
    """ log out"""
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('user')
    return resp
