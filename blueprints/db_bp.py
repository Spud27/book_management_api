from flask import Blueprint
from init import db

from models.user import User

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

    db.session.add_all(users)
    db.session.commit()
    print('Tables Seeded')