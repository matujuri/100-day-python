from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
import csv
from datetime import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open = TimeField('Open', default=time(8, 0, 0), validators=[DataRequired()])
    close = TimeField('Close', default=time(17, 0, 0), validators=[DataRequired()])
    coffee = SelectField('Coffee', validators=[DataRequired()], choices=[('✘', 0), ('☕️', 1), ('☕️☕️', 2), ('☕️☕️☕️', 3), ('☕️☕️☕️☕️', 4), ('☕️☕️☕️☕️☕️', 5)]) # type: ignore
    wifi = SelectField('Wifi', validators=[DataRequired()], choices=[('✘', 0), ('💪', 1), ('💪💪', 2), ('💪💪💪', 3), ('💪💪💪💪', 4), ('💪💪💪💪💪', 5)]) # type: ignore
    power = SelectField('Power', validators=[DataRequired()], choices=[('✘', 0), ('🔌', 1), ('🔌🔌', 2), ('🔌🔌🔌', 3), ('🔌🔌🔌🔌', 4), ('🔌🔌🔌🔌🔌', 5)]) # type: ignore
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == 'POST' and form.validate_on_submit():
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
