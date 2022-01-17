from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Order, Receipt, MenuItems, Status


def cashier_list_menu():
    pass