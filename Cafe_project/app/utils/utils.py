import re

from flask import current_app


class Validator:
    @staticmethod
    def validate_fullname(name):
        pattern = r"^[a-zA-Z]{3,}$"
        if re.match(pattern, name):
            return True
        else:
            return False

    @staticmethod
    def validate_phone_number(phone):
        pattern = r"^(09|\+989)\d{9}$"
        if re.match(pattern, phone):
            return True
        else:
            return False

    @staticmethod
    def validate_email(email):
        pattern = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        if re.match(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def validate_password(passwd):
        pattern = r".{4,}"
        if re.match(pattern, passwd):
            return True
        else:
            return False


def allowed_file(filename: str) -> bool:
    """
        check if provided file name matches to allowed extension
        return true of false according condition
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
