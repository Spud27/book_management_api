from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String
from marshmallow.validate import Length, Regexp, And

class Genre(db.Model):
    __tablename__ = 'genres'

    # Primary Key
    genre_id = db.Column(db.Integer, primary_key=True)

    genre_name = db.Column(db.String(200), nullable=False, unique=True)

    books = db.relationship('Book', back_populates='genre')


class GenreSchema (ma.Schema):
    # stop recursion occuring
    books = fields.Nested('BookSchema', many=True, exclude=['genre', 'genre_id'])

    # Validation
    genre_name = String(required=True, validate=And(
        Length(min=6, error='genre name must be at least 6 characters')
        # Regexp('^A-Za-z0-9$', error='invalid character')
    ))

    class Meta():
        fields = ('genre_id', 'genre_name')


one_genre = GenreSchema()
many_genres = GenreSchema(many=True)
add_new_genre = GenreSchema(exclude=['genre_id'])