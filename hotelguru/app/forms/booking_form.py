from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length


class BookingForm(FlaskForm):
    check_in = DateField("From: ", validators=[DataRequired()], format="%Y-%m-%d")
    check_out = DateField("To: ", validators=[DataRequired()], format="%Y-%m-%d")
    comment = TextAreaField("Comment: ")

    submit = SubmitField("Submit")