from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, SubmitField


class RegistrationForm(FlaskForm):
    username = StringField(
        "foo_input", validators=[DataRequired(), Length(min=2, max=20)]
    )
    submit = SubmitField("Run")
