from wtforms import StringField, FloatField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange

class RateForm(FlaskForm):
    rating = FloatField(validators=[DataRequired(), NumberRange(min=0, max=10)], label="Your Rating Out of 10 e.g. 7.5")
    review = StringField(validators=[DataRequired()], label="Your Review")
    submit = SubmitField("Submit")
    
class SearchForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Search")
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Register")