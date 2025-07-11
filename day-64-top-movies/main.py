from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from edit_movie import EditMovieForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html", movies=db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars())

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        movie_id = request.form["id"]
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = float(request.form["rating"])
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    movie_id = request.args.get('id')
    movie_selected = db.get_or_404(Movie, movie_id)
    form=EditMovieForm()
    form.id.data = str(movie_selected.id)
    return render_template("edit.html", form=form)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
