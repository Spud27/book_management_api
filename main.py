from flask import Flask
from init import ma, db
import os
from blueprints.db_bp import db_bp
from blueprints.users_bp import users_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)

    return app

