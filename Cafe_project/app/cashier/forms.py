from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class AddNewTableForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired()], render_kw={"placeholder": "Position here"})
    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=2, max=20, message="Capacity must be between 2 and 20")],
                            render_kw={"placeholder": "Capacity here"}
                            )
