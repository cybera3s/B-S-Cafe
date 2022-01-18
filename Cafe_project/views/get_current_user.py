from flask import request
from models.models import Cashier
from database.manager import db


def get_current_user() -> Cashier:
    """
    return current Cashier object from database if exist in cookies
    """
    user_res = None

    if 'user' in request.cookies:
        user = request.cookies['user']
        user_res = db.read_by(Cashier, ('email', user))[0]

    return user_res
