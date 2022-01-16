from flask import render_template, request


def test():
    if request.method == "GET":
        return render_template("cashier/baseCashier.html")