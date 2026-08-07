import os

from flask import Flask
from .Database import db
from .behaviors import auth
from .behaviors.games import gamePage
from .behaviors import welcome


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'FlaskrBJSite.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path,exist_ok=True)

    db.init_app(app)

    #Add in the stuff for adding blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(gamePage.bp)
    app.register_blueprint(welcome.bp)
   


    return app
