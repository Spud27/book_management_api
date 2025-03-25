from flask import Flask
from init import ma, db
import os
from blueprints.db_bp import db_bp
from blueprints.users_bp import users_bp
from blueprints.genres_bp import genres_bp
from blueprints.books_bp import books_bp
from blueprints.reviews_bp import reviews_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)

    return app

