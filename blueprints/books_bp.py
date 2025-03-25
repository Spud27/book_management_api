from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from models.book import Book, many_books, one_book, add_new_book
from init import db

books_bp = Blueprint('books', __name__)

# Read all - GET /books
@books_bp.route('/books')
def get_all_books():
    stmt = db.select(Book).order_by(Book.title)
    books = db.session.scalars(stmt)
    return many_books.dump(books)


# Read one - GET /books/<int:book_id>
@books_bp.route('/books/<int:book_id>')
def get_one_book(book_id):
    stmt = db.select(Book).filter_by(book_id=book_id)
    book = db.session.scalar(stmt)
    if book:
        return one_book.dump(book)
    else:
        return {'error': f'Book with id {book_id} does not exist'}, 404
    

# Create - POST /books
@books_bp.route('/books', methods=['POST'])
def create_new_book():
    try:
        data = add_new_book.load(request.json)

        new_book = Book(
            title = data.get('title'),
            author = data.get('author'),
            description = data.get('description'),
            genre_id = data.get('genre_id')
        )

        db.session.add(new_book)
        db.session.commit()
        return one_book.dump(new_book)
    except IntegrityError:
        return {"error": "Book Title already in use"}, 409

# Update - PUT /books/<int:book_id>
@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    stmt = db.select(Book).filter_by(book_id=book_id)
    book = db.session.scalar(stmt)
    if book:
        data = add_new_book.load(request.json)
        book.title = data.get('title') or book.title
        book.author = data.get('author') or book.author
        book.description = data.get('description') or book.description
        book.genre_id = data.get('genre_id') or book.genre_id
        db.session.commit()
        return one_book.dump(book), 200
    else:
        return {'error': f'Book with id {book_id} does not exist'}, 404


# Delete - DELETE /books/<int:book:id>
@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    stmt = db.select(Book).filter_by(book_id=book_id)
    book = db.session.scalar(stmt)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Book with id {book_id} does not exist'}, 404
