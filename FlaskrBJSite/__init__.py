import os

from flask import Flas, Flask
from .Database import db
# from behaviors.auth import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path,exist_ok=True)

    db.init_app(app)

    #Add in the stuff for adding blueprints

    app.add_url_rule('/',endpoint='index') #this may need to change/update depending on which page we want to be the base page.


    return app