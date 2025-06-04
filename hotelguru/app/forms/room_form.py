from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class RoomForm(FlaskForm):
    type = StringField("Type", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])

    submit = SubmitField("Submit")