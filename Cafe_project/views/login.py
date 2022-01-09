from flask import url_for, request, redirect, render_template
from database.manager import db
from models import models

def login():
    return render_template('cashier/login.html')