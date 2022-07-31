from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, EmailField, PasswordField, FloatField, \
    SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms.validators import ValidationError

from app.models import Cashier, Category


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
            self.form_errors.append(err_msg)
            return False
        # Do the passwords match
        if not cashier.check_password(self.password.data):
            self.form_errors.append(err_msg)
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
        validators=[DataRequired(), Length(min=4, max=100, message="Password must be between 4 and 100")]
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

        return True


class MenuItemForm(FlaskForm):
    DISCOUNTS = [(0, "Choose Your Discount...")]
    CATEGORIES = [(0, "Choose Your Category...")]
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)], )

    serving_time_period = StringField('Serving Time', validators=[DataRequired(), Length(min=3)],
                                      description=' e.g: Always, Morning...', )

    estimated_cooking_time = IntegerField('Estimated Cooking Time', validators=[DataRequired(), NumberRange(min=1)],
                                          description='in Minutes', )

    discount = SelectField('Discount', choices=DISCOUNTS, coerce=int, description="(Optional)")
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()], coerce=int)
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
        , FileSize(max_size=5 * 1000 * 1000)])
    submit = SubmitField("Add Item")

    def validate(self):
        check_validate = super(MenuItemForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False

        if self.category.data == 0:
            self.category.errors.append('Please Select a Category')
            return False

        if self.discount.data == 0:
            self.discount.data = None

        return True


class AddCategoryForm(FlaskForm):
    ROOTS = [(0, "Choose Your Category Root...")]
    DISCOUNTS = [(0, "Choose Your Discount...")]
    id = IntegerField(widget=HiddenInput())
    category_name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    category_root = SelectField('Root', choices=ROOTS, coerce=int)
    discount_id = SelectField('Discount', choices=DISCOUNTS, coerce=int)
    is_root = BooleanField('Is Root?', default=False)

    def validate(self):
        check_validate = super(AddCategoryForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False

        if self.category_root.data == 0:
            self.category_root.data = None

        if self.discount_id.data == 0:
            self.discount_id.data = None

        return True