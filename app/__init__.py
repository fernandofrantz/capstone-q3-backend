from flask import Flask
from .configs import database, migrations, jwt
from app import routes

def create_app():
    app = Flask(__name__)

    database.init_app(app)
    migrations.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app