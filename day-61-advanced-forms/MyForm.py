from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class MyForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(),Email(message="Invalid email address")])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')