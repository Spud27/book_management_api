from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import Email, String
from marshmallow.validate import Length, Regexp, And

class Review(db.Model):
    __tablename__ = 'reviews'

    # Primary Key
    review_id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500))

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    # back_populates connects the two ends (fields). its value is the field in the related model
    user = db.relationship('User', back_populates = 'reviews')
    book = db.relationship('Book', back_populates = 'reviews')

class ReviewSchema (ma.Schema):
    # Validation

    title = String(required=True, validate=And(
        Length(min=6, error='reviewname must be at least 6 characters')
        # Regexp('^A-Za-z0-9$', error='invalid character')
    ))

    genre = fields.Nested('GenreSchema')


    class Meta():
        fields = ('review_id', 'title', 'author', 'description', 'genre_id', 'genre')


one_review = ReviewSchema()
many_reviews = ReviewSchema(many=True)
add_new_review = ReviewSchema(exclude=['review_id'])