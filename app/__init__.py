from flask import Flask
from .configs import database, migrations
from . import routes

def create_app():
    app = Flask(__name__)

    database.init_app(app)
    migrations.init_app(app)
    # initialize routes
    # routes.init_app(app)

    return app