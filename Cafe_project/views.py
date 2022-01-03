from flask import url_for, request, redirect


def index():
    if request.method == 'GET':
        return ' Index Page ! '


def menu():
    if request.method == 'GET':
        return ' Menu Page ! '


def order(table_id):
    if request.method == 'GET':
        return f'GET/Order Page !{table_id} '
    elif request.method == 'POST':
        return f'POST/Order Page !{table_id} '
    elif request.method == 'DELETE':
        return f'DELETE/Order Page !{table_id}'
