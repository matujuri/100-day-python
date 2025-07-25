from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
import requests
from forms import RateForm, SearchForm, LoginForm, RegisterForm
import os
from dotenv import load_dotenv
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash

load_dotenv()
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'movies.db')}"
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE DB
class Base(DeclarativeBase):
    """
    SQLAlchemyの宣言的ベースクラス。
    このクラスを継承することで、モデルクラスがデータベーステーブルにマッピングされます。
    """
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    """
    映画情報を保存するデータベースモデル。
    各カラムは映画のタイトル、公開年、説明、評価、ランキング、レビュー、画像URLを管理します。
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    review: Mapped[str] = mapped_column(String, nullable=False, default="")
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), default=0)
    user: Mapped["User"] = relationship(back_populates="movies")
    
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    movies = relationship("Movie", back_populates="user")

def update_ranking():
    """
    データベース内の映画のランキングを更新します。
    映画を評価の高い順に並べ替え、1位から順にランキングを割り当てます。
    """
    movies = db.session.execute(db.select(Movie).where(Movie.user_id == current_user.id).order_by(Movie.rating.desc())).scalars()
    for i, movie in enumerate(movies):
        movie.ranking = i + 1
    db.session.commit()
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("movies"))
    else:
        movie = Movie()
        movie.title = "CODA"
        movie.year = 2021
        movie.description = "As a CODA (Child of Deaf Adults), Ruby is the only hearing person in her deaf family. When the family's fishing business is threatened, Ruby finds herself torn between pursuing her love of music and her fear of abandoning her parents."
        movie.img_url = "https://image.tmdb.org/t/p/w500/BzVjmm8l23rPsijLiNLUzuQtyd.jpg"
        return render_template("index.html", movie=movie, login_form=LoginForm(), register_form=RegisterForm(), search_form=SearchForm())

@app.route("/register", methods=["POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data or "", method="pbkdf2:sha256", salt_length=8),
            name=form.name.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("movies"))
    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data or ""):
            login_user(user)
            return redirect(url_for("movies"))
        else:
            flash("メールアドレスまたはパスワードが正しくありません")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/movies")
@login_required
def movies():
    """
    ホームページを表示します。
    データベースから映画をランキング順に取得し、テンプレートに渡して表示します。
    """
    movies = db.session.execute(db.select(Movie).where(Movie.user_id == current_user.id).order_by(Movie.ranking.desc())).scalars().all()
    return render_template("movies.html", movies=movies, search_form=SearchForm())

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    """
    映画の評価とレビューを更新するページを表示・処理します。
    GETリクエストでは、選択された映画の現在の評価とレビューをフォームに表示します。
    POSTリクエストでは、フォームから送信されたデータで映画の評価とレビューを更新し、
    ランキングを再計算してホームページにリダイレクトします。
    """
    movie_id = request.args.get('id')
    movie_to_update = db.get_or_404(Movie, movie_id)
    form = RateForm()
    if request.method == "POST" and form.validate_on_submit():
        movie_to_update.rating = float(request.form["rating"])
        movie_to_update.review = request.form["review"]
        db.session.commit()
        update_ranking()
        return redirect(url_for("movies"))
    movie_title = movie_to_update.title
    form.rating.data = movie_to_update.rating
    form.review.data = movie_to_update.review
    return render_template("rate.html", form=form, title=movie_title)

@app.route("/delete")
@login_required
def delete():
    """
    映画をデータベースから削除します。
    指定されたIDの映画を削除し、ランキングを再計算してホームページにリダイレクトします。
    """
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    update_ranking()
    return redirect(url_for("movies"))

def _filter_saved_movies(search_results, saved_movies):
        saved_titles = {movie.title for movie in saved_movies}
        return [item for item in search_results if item["title"] not in saved_titles]

@app.route("/search", methods=["POST"])
def search():
    """
    映画を検索し、検索結果を表示します。
    POSTリクエストでは、フォームから送信されたタイトルでThe Movie Database APIを検索し、
    結果を人気度でソートし、既に保存されている映画を除外して表示します。
    GETリクエストでは、検索フォームを表示します。
    """
    form = SearchForm()
    if form.validate_on_submit():
        title = request.form["title"]
        headers = {
            "Authorization": f"Bearer {TMDB_API_TOKEN}"
        }
        body = {
            "query": title
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", headers=headers, params=body)
        response.raise_for_status()
        data = response.json()["results"]
        
        if current_user.is_authenticated:
            saved_movies = db.session.execute(db.select(Movie).where(Movie.user_id == current_user.id).order_by(Movie.ranking.desc())).scalars()
            filtered_data = _filter_saved_movies(data, saved_movies)
        else:
            filtered_data = data
        
        popularity_sorted_data=sorted(filtered_data, key=lambda x: x["popularity"] if x.get("popularity") else 0, reverse=True)[:10]
        release_date_sorted_data = sorted(popularity_sorted_data, key=lambda x: x["release_date"])
        return render_template("select.html", options=release_date_sorted_data, keyword=title)
    return redirect(url_for("home"))

@app.route("/", methods=["POST"])
def create_card():
    selected_data = json.loads(request.form.get("selected") or "{}")
    movie = Movie()
    movie.title = selected_data.get("title")
    movie.year = int(selected_data.get("release_date", "").split("-")[0]) if selected_data.get("release_date") else 0
    movie.description = selected_data.get("overview")
    movie.img_url = f"https://image.tmdb.org/t/p/w500{selected_data.get('poster_path')}" if selected_data.get('poster_path') else ""
    if current_user.is_authenticated:
        movie.user_id = current_user.id
        db.session.add(movie)
        db.session.commit()
        update_ranking()
        return redirect(url_for("rate", id=movie.id))
    else:
        return render_template("index.html", movie=movie, login_form=LoginForm(), register_form=RegisterForm(), search_form=SearchForm())

if __name__ == '__main__':
    app.run(debug=True)
