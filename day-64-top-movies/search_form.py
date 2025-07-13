from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Search")