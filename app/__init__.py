from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.infraBD.config.connection import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from app.infraBD.models import products, users, transactions

    return app
