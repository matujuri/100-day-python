from wtforms import StringField, FloatField, IntegerField, SubmitField, HiddenField 
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class EditMovieForm(FlaskForm):
    rating = FloatField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")
    id = HiddenField("ID")