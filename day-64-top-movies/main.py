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
from add_movie import AddMovieForm
import os
from dotenv import load_dotenv

load_dotenv()
themoviedbAPITOKEN = os.getenv("themoviedbAPITOKEN")

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
    form = EditMovieForm()
    if request.method == "POST" and form.validate_on_submit():
        movie_id = request.form["id"]
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = float(request.form["rating"])
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    movie_id = request.args.get('id')
    movie_selected = db.get_or_404(Movie, movie_id)
    form.id.data = str(movie_selected.id)
    movie_title = movie_selected.title
    return render_template("edit.html", form=form, title=movie_title)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if request.method == "POST" and form.validate_on_submit():
        title = request.form["title"]
        headers = {
            "Authorization": f"Bearer {themoviedbAPITOKEN}"
        }
        body = {
            "query": title
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", headers=headers, params=body)
        response.raise_for_status()
        data = response.json()["results"]
        popularity_sorted_data=sorted(data, key=lambda x: x["popularity"], reverse=True)[:10]
        release_date_sorted_data = sorted(popularity_sorted_data, key=lambda x: x["release_date"])
        return render_template("select.html", options=release_date_sorted_data)
    return render_template("add.html", form=form)

@app.route("/add/<title>")
def add_movie(title):
    movie = Movie()
    movie.title = title or "No title"
    movie.year = int(request.args.get("year") or 0)
    movie.description = request.args.get("description") or "No description"
    movie.img_url = request.args.get("img_url") or "No image"
    movie.rating = 0.0
    movie.ranking = 0
    movie.review = ""
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for("edit", id=movie.id))

if __name__ == '__main__':
    app.run(debug=True)
