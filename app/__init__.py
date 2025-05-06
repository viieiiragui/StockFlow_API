from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.infraDB.config.connection import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    from app.routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.product_route import product_bp
    app.register_blueprint(product_bp)

    from app.routes.transaction_route import transaction_bp
    app.register_blueprint(transaction_bp)

    with app.app_context():
        from app.infraDB.models import products, users, transactions

    return app
