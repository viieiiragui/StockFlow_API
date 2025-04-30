from flask import Flask
from dotenv import load_dotenv
from config import Config
from infraBD.config.connection import db
from infraBD.models.products import Products
from infraBD.models.users import Users
from infraBD.models.transactions import Transactions

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return "API Stock works!"

    return app

# Executa o servidor
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
