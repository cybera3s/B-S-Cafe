from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField
from wtforms.validators import DataRequired, NumberRange


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
