from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from models.user import User, many_users, one_user, add_new_user
from init import db

users_bp = Blueprint('users', __name__)

# Read all - GET /users
@users_bp.route('/users')
def get_all_users():
    # Create the SQL statement
    stmt = db.select(User).order_by(User.username)
    # Execute the SQL statement
    users = db.session.scalars(stmt)
    # pass in the list of users to .dump() to serialise it
    return many_users.dump(users)


# Read one - GET /users/<int:user_id>
@users_bp.route('/users/<int:user_id>')
def get_one_user(user_id):
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return one_user.dump(user)
    else:
        return {'error': f'User with id {user_id} does not exist'}, 404
    

# Create - POST /users
@users_bp.route('/users', methods=['POST'])
def create_new_user():
    # some exception handling
    try:

        data = add_new_user.load(request.json)

        # Check if username already exists in the database
        existing_user_username = User.query.filter_by(username=data.get('username')).first()
        if existing_user_username:
            return {"error": "Username already in use"}, 409
        # Check if email already exists in the database
        existing_user_email = User.query.filter_by(email=data.get('email')).first()
        if existing_user_email:
            return {"error": "Email address already in use"}, 409
        # Check if password already exists in the database
        existing_user_password = User.query.filter_by(password=data.get('password')).first()
        if existing_user_password:
            return {"error": "Password already in use"}, 409

        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = data.get('password')
        )

        db.session.add(new_user)
        db.session.commit()
        return one_user.dump(new_user)
    except IntegrityError:
        return {"error": "Username, Email or Password already in use"}, 409

# Update - PUT /users/<int:user_id>
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    if user:
        data = add_new_user.load(request.json)
        user.username = data.get('username') or user.username
        user.email = data.get('email') or user.email
        user.password = data.get('password') or user.password
        db.session.commit()
        return one_user.dump(user), 200
    else:
        return {'error': f'User with id {user_id} does not exist'}, 404


# Delete - DELETE /users/<int:user:id>
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'User with id {user_id} does not exist'}, 404
