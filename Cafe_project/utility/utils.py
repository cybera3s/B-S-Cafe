import re


class Validator:

    @staticmethod
    def validate_fullname(name):
        pattern = r'^[a-zA-Z]{3,}$'
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
        pattern = r'.{4,}'
        if re.match(pattern, passwd):
            return True
        else:
            return False
