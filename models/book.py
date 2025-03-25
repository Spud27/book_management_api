from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import Email, String
from marshmallow.validate import Length, Regexp, And

class Book(db.Model):
    __tablename__ = 'books'

    # Primary Key
    book_id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False, unique=True)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(50), nullable=False)

    # Foreign Key
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    # back_populates connects the two ends (fields). its value is the field in the related model
    genre = db.relationship('Genre', back_populates = 'books')
    reviews = db.relationship('Review', back_populates = 'book')

class BookSchema (ma.Schema):
    # Validation

    title = String(required=True, validate=And(
        Length(min=6, error='bookname must be at least 6 characters')
        # Regexp('^A-Za-z0-9$', error='invalid character')
    ))

    genre = fields.Nested('GenreSchema')


    class Meta():
        fields = ('book_id', 'title', 'author', 'description', 'genre_id', 'genre')


one_book = BookSchema()
many_books = BookSchema(many=True)
add_new_book = BookSchema(exclude=['book_id'])