from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, EmailField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms.widgets import HiddenInput

from app.models import Cashier


class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False
        # Does our user exist
        cashier = Cashier.query.filter_by(email=self.email.data).first()
        err_msg = 'Invalid Email Or Password'
        if not cashier:
            self.email.errors.append(err_msg)
            return False
        # Do the passwords match
        if not cashier.check_password(self.password.data):
            self.email.errors.append(err_msg)
            return False
        return True


class AddNewTableForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired()], render_kw={"placeholder": "Position here"})
    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=2, max=20, message="Capacity must be between 2 and 20")],
                            render_kw={"placeholder": "Capacity here"}
                            )


class AboutSettingForm(FlaskForm):
    paragraph1 = TextAreaField('Paragraph 1', render_kw={"placeholder": "Paragraph 1 here"})
    paragraph2 = TextAreaField('Paragraph 2', render_kw={"placeholder": "Paragraph 2 here"})
    paragraph3 = TextAreaField('Paragraph 3', render_kw={"placeholder": "Paragraph 3 here"})
    manager1 = StringField('Manager 1', render_kw={"placeholder": "Manager 1 here"})
    manager2 = StringField('Manager 2', render_kw={"placeholder": "Manager 2 here"})
    manager3 = StringField('Manager 3', render_kw={"placeholder": "Manager 3 here"})
    manager4 = StringField('Manager 4', render_kw={"placeholder": "Manager 4 here"})
    banner_url = URLField('Banner Url', validators=[DataRequired()], render_kw={"placeholder": "Banner Url here"})


class CashierProfile(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=150)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=150)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), NumberRange(min=4, max=100, message="Password must be between 4 and 100")]
    )

    def validate(self):
        check_validate = super(CashierProfile, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False

        # get cashier
        cashier = Cashier.query.get(self.id.data)
        if self.email.data != cashier.email:
            # check exist of email for uniqueness
            c = Cashier.query.filter_by(email=self.email.data).first()
            if c:
                self.form_errors.append("Duplicate Email Address!")
                return False
        if self.phone_number.data != cashier.phone_number:
            # check exist of email for uniqueness
            c = Cashier.query.filter_by(email=self.phone_number.data).first()
            if c:
                self.id.errors.append("Duplicate Phone Number!")
                return False
        # hash password
        cashier.set_password(self.password.data)

        return True
