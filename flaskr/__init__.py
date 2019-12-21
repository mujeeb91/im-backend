from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model has to be imported after initializing db variable
from .model import User, insert_seed_data
from .auth import auth as auth_blueprint
from .message import message as message_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # blueprints for routes in our app
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(message_blueprint)

    with app.app_context():
        db.create_all()
        insert_seed_data()

    return app
