from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

db = SQLAlchemy()

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    
    def __init__(self, id, title, author, rating):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()
    
    book = Book(
        id=1,
        title="Harry Potter",
        author="J. K. Rowling",
        rating=9.3
    )
    db.session.add(book)
    db.session.commit()