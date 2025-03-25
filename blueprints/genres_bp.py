from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from models.genre import Genre, many_genres, one_genre, add_new_genre
from init import db

genres_bp = Blueprint('genres', __name__)

# Read all - GET /genres
@genres_bp.route('/genres')
def get_all_genres():
    stmt = db.select(Genre).order_by(Genre.genre_name)
    genres = db.session.scalars(stmt)
    return many_genres.dump(genres)


# Read one - GET /genres/<int:genre_id>
@genres_bp.route('/genres/<int:genre_id>')
def get_one_genre(genre_id):
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)
    if genre:
        return one_genre.dump(genre)
    else:
        return {'error': f'Genre with id {genre_id} does not exist'}, 404
    

# Create - POST /genres
@genres_bp.route('/genres', methods=['POST'])
def create_new_genre():
    try:
        data = add_new_genre.load(request.json)
        new_genre = Genre(
            genre_name = data.get('genre_name'),
        )

        db.session.add(new_genre)
        db.session.commit()
        return one_genre.dump(new_genre)
    except IntegrityError:
        return {"error": "Genre name already in use"}, 409

# Update - PUSH /genres/<int:genre_id>
@genres_bp.route('/genres/<int:genre_id>', methods=['PUSH'])
def update_genre(genre_id):
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)
    if genre:
        data = add_new_genre.load(request.json)
        genre.genre_name = data.get('genre_name') or genre.genre_name
        db.session.commit()
        return one_genre.dump(genre), 200
    else:
        return {'error': f'Genre with id {genre_id} does not exist'}, 404


# Delete - DELETE /genres/<int:genre:id>
@genres_bp.route('/genres/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    stmt = db.select(Genre).filter_by(genre_id=genre_id)
    genre = db.session.scalar(stmt)
    if genre:
        db.session.delete(genre)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Genre with id {genre_id} does not exist'}, 404
