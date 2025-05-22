from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField("Email Address*", validators=[DataRequired()])
    password = PasswordField("Password*", validators=[DataRequired(), Length(6)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")