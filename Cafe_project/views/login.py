from flask import url_for, request, redirect, render_template, make_response, flash
from database.manager import db
from models import models


def login():
    """login view"""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user_info: models.Cashier = db.read_by(models.Cashier, ('email', email))

        # user does not exist
        if not user_info or user_info[0].password != password:
            flash('wrong email or password !', 'warning')
            return render_template('cashier/login.html')

        # user exists
        res = make_response("""
                            <h1>cookie is set<br>Hello {}</h1>
                            <button id='logout'>logout</button>
                            """.format(user_info[0].first_name))
        res.set_cookie('user', email)
        return res

    # Handle get request
    return render_template('cashier/login.html')
