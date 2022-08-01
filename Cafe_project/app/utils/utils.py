import re

from flask import current_app, Flask


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


def check_email_configuration(app: Flask) -> bool | Exception:
    """
        Take Flask application object and check email and Celery configuration
        if any of the configuration is not set raise a Exception
        else return True
    """
    email_config = ['MAIL_SERVER', 'MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_PORT', 'MAIL_USE_TLS', 'MAIL_USE_SSL',
                    'MAIL_DEFAULT_SENDER', 'CELERY_BROKER_URL', 'CELERY_RESULT_BACKEND']

    if all_set := not all([app.config[c] is not None for c in email_config]):
        not_set = list(filter(lambda config: app.config[config] is None, email_config))
        raise Exception(f"Some of the Email or Celery Config is Not Set : {', '.join(not_set)}")

    return all_set
