from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
import csv
from datetime import time

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', default="https://goo.gl/maps/ALR8iBiNN6tVfuAA8", validators=[DataRequired(), URL()])
    open = TimeField('Open', default=time(8, 0, 0), validators=[DataRequired()])
    close = TimeField('Close', default=time(17, 0, 0), validators=[DataRequired()])
    coffee = SelectField('Coffee', validators=[DataRequired()], choices=[(str(i), i * '☕️') for i in range(6)])
    wifi = SelectField('Wifi', validators=[DataRequired()], choices=[(str(i), i * '💪') for i in range(6)])
    power = SelectField('Power', validators=[DataRequired()], choices=[(str(i), i * '🔌') for i in range(6)])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('day-62-coffee-and-wifi/cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data}, {form.location.data}, {form.open.data.strftime('%H:%M') if form.open.data else ''}, {form.close.data.strftime('%H:%M') if form.close.data else ''}, {form.coffee.data}, {form.wifi.data}, {form.power.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('day-62-coffee-and-wifi/cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
