import argparse
from app.models import Cashier
from app.utils.utils import Validator

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="createcashier", help="create a new cashier_panel")
    args = parser.parse_args()

    if args.createcashier == "createcashier":

        try:
            firstname = input("enter your first name: ")
            msg = "Your last name must be in alphabetical order and more than 3 characters"
            assert Validator.validate_fullname(firstname), msg

            lastname = input("enter your last name: ")
            msg = "Your last name must be in alphabetical order and more than 3 characters"
            assert Validator.validate_fullname(lastname), msg

            phone_number = input("enter your phone number: ")
            msg = "Your phone number must start with 09 or +989 and be 11 or 13 characters"
            assert Validator.validate_phone_number(phone_number), msg

            email = input("enter your email address: ")
            assert Validator.validate_email(email), "invalid email format !"

            password = input("Enter your password :")
            assert Validator.validate_email(
                email
            ), "password must be more than four characters !"

            new_cashier = Cashier(firstname, lastname, phone_number, email)
            new_cashier.set_password(password)
            new_cashier.create()
            print("new cashier created !")

        except Exception as e:
            print(e)
    else:
        print("Wrong argument !")
