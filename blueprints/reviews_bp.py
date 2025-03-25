from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from models.review import Review, many_reviews, one_review, add_new_review
from init import db

reviews_bp = Blueprint('reviews', __name__)

# Read all - GET /reviews
@reviews_bp.route('/reviews')
def get_all_reviews():
    stmt = db.select(Review).order_by(Review.rating)
    reviews = db.session.scalars(stmt)
    return many_reviews.dump(reviews)


# Read one - GET /reviews/<int:review_id>
@reviews_bp.route('/reviews/<int:review_id>')
def get_one_review(review_id):
    stmt = db.select(Review).filter_by(review_id=review_id)
    review = db.session.scalar(stmt)
    if review:
        return one_review.dump(review)
    else:
        return {'error': f'Review with id {review_id} does not exist'}, 404
    

# Create - POST /reviews
@reviews_bp.route('/reviews', methods=['POST'])
def create_new_review():
        data = add_new_review.load(request.json)

        new_review = Review(
            rating = data.get('rating'),
            feedback = data.get('feedback'),
            user_id = data.get('user_id'),
            book_id = data.get('book_id')
        )

        db.session.add(new_review)
        db.session.commit()
        return one_review.dump(new_review)


# Update - PUT /reviews/<int:review_id>
@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    stmt = db.select(Review).filter_by(review_id=review_id)
    review = db.session.scalar(stmt)
    if review:
        data = add_new_review.load(request.json)
        review.rating = data.get('rating') or review.rating
        review.feedback = data.get('feedback') or review.feedback
        review.user_id = data.get('user_id') or review.user_id
        review.book_id = data.get('book_id') or review.book_id
        db.session.commit()
        return one_review.dump(review), 200
    else:
        return {'error': f'Review with id {review_id} does not exist'}, 404


# Delete - DELETE /reviews/<int:review:id>
@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    stmt = db.select(Review).filter_by(review_id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Review with id {review_id} does not exist'}, 404
