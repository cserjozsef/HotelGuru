from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Full Name", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    postalcode = IntegerField("Postal Code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])

    submit = SubmitField("Register")