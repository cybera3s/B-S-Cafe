import click
from getpass import getpass
import pytest

from .models import Cashier
from .extensions import db
from .utils.utils import Validator


def register(app):
    @app.cli.command('create_new_cashier')
    def create_user():
        try:
            firstname = input("Enter Your First Name: ")
            msg = "Your last name must be in alphabetical order and more than 3 characters"
            assert Validator.validate_fullname(firstname), msg

            lastname = input("Enter Your Last Name: ")
            msg = "Your last name must be in alphabetical order and more than 3 characters"
            assert Validator.validate_fullname(lastname), msg

            phone_number = input("Enter Your Phone Number: ")
            msg = "Your phone number must start with 09 or +989 and be 11 or 13 characters"
            assert Validator.validate_phone_number(phone_number), msg

            email = input("Enter Your Email Address: ")
            assert Validator.validate_email(email), "invalid email format !"

            password = getpass('Enter Your Password :')
            assert Validator.validate_password(
                password
            ), "password must be more than four characters !"

            new_cashier = Cashier(first_name=firstname, last_name=lastname, phone_number=phone_number, email=email)
            new_cashier.set_password(password)
            new_cashier.create()
            print(f"New Cashier {email} Created!")
            print(f"You can Login at /admin/login")

        except Exception as e:
            print(e)

    @app.cli.command()
    def tests():
        """
            Run tests.
        """
        pytest.main(['--rootdir', 'app/tests'])
