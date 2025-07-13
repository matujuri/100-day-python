from wtforms import StringField, FloatField, SubmitField, HiddenField 
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange

class EditMovieForm(FlaskForm):
    rating = FloatField(validators=[DataRequired(), NumberRange(min=0, max=10)], label="Your Rating Out of 10 e.g. 7.5")
    review = StringField(validators=[DataRequired()], label="Your Review")
    submit = SubmitField("Submit")
    id = HiddenField("ID")