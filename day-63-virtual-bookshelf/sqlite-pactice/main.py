from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # # create a new book
    # book1 = Book()
    # book1.title = "Harry Potter"
    # book1.author = "J. K. Rowling"
    # book1.rating = 9.3
    # db.session.add(book1)
    
    # # create another book
    # book2 = Book()
    # book2.title = "The Great Gatsby"
    # book2.author = "F. Scott Fitzgerald"
    # book2.rating = 8.5
    # db.session.add(book2)
    # db.session.commit()
    
    # read all books
    books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    for book in books:
        print(book.title, book.author, book.rating)
    
    # # read a book by id
    # book = db.get_or_404(Book, 1)
    # print(book.title)

    # # update a book
    # book = db.get_or_404(Book, 1)
    # book.rating = 10.0
    # db.session.commit()
    
    # # delete a book
    # book = db.get_or_404(Book, 1)
    # db.session.delete(book)
    # db.session.commit()
    
    
    
    
    