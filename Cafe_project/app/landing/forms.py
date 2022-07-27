from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, EmailField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length
from app.models import Cashier


class ContactUsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)],
                             render_kw={"placeholder": "First Name here"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)],
                            render_kw={"placeholder": "Last Name here"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email Address here"})
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(max=400)],
                             render_kw={"placeholder": "Feedback here"})
