from init import db, ma
from marshmallow.fields import Email, String
from marshmallow.validate import Length, Regexp, And

class User(db.Model):
    __tablename__ = 'users'

    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=True)

    reviews = db.relationship('Review', back_populates = 'user')

class UserSchema (ma.Schema):
    # Validation
    email = Email(required=True)

    username = String(required=True, validate=And(
        Length(min=6, error='username must be at least 6 characters')
        # Regexp('^A-Za-z0-9$', error='invalid character')
    ))

    password = String(required=True, validate=And(
        Length(min=6, error='password must be at least 6 characters')
        # Regexp('^A-Za-z0-9$', error='invalid character')
    ))

    class Meta():
        fields = ('user_id', 'username', 'email', 'password')


one_user = UserSchema()
many_users = UserSchema(many=True)
add_new_user = UserSchema(exclude=['user_id'])