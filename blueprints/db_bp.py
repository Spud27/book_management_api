from flask import Blueprint
from init import db
from models.user import User
from models.genre import Genre
from models.book import Book
from models.review import Review

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables created')

@db_bp.cli.command('seed')
def seed_tables():
    users = [
        User(
            username = 'bookie',
            email = 'bookie@gmail.com',
            password = '123456'
        ),
        User(
            username = 'bookface',
            email = 'bookface@spam.com',
            password = '654321'
        )
    ]
    genres = [
        Genre(
            genre_name = 'Horror'
        ),
        Genre(
            genre_name = 'Comedy'
        ),
        Genre(
            genre_name = 'Romance'
        ),
        Genre(
            genre_name = 'Fantasy'
        )
    ]

    db.session.add_all(genres)
    db.session.commit()

    books = [
        Book(
            title = 'Harry Potter 1',
            author = 'JK Rowling',
            genre_id = 1,
            description = 'Pretty good book'
        ),
        Book(
            title = 'Lord of The Rings',
            author = 'J.R.R Tolkien',
            genre_id = 3,
            description = 'Amazing book'
        )
    ]

    db.session.add_all(users)
    db.session.add_all(books)
    db.session.commit()

    reviews = [
        Review(
            rating = 5,
            feedback = 'it was too long',
            book_id = 1,
            user_id = 1
        ),
        Review(
            rating = 4,
            feedback = 'it was too short',
            book_id = 2,
            user_id = 2
        )
    ]

    db.session.add_all(reviews)
    db.session.commit()
    print('Tables Seeded')