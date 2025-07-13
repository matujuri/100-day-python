from wtforms import StringField, FloatField, IntegerField, SubmitField, HiddenField 
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class EditMovieForm(FlaskForm):
    rating = FloatField(validators=[DataRequired()], label="Your Rating Out of 10 e.g. 7.5")
    review = StringField(validators=[DataRequired()], label="Your Review")
    submit = SubmitField("Submit")
    id = HiddenField("ID")