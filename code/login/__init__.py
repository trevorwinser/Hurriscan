from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'users.db'

def create_app():
    app = Flask(__name__, static_folder= "../static", template_folder= "../templates")
    app.config['SECRET_KEY'] = "hurriscanKey"
    import os

    # Absolute directory path of this __init__.py file
    basedir = os.path.abspath(os.path.dirname(__file__))

    DB_NAME = 'users.db'

    # Use the absolute path in SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_NAME)

    db.init_app(app)
    
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    from .models import User
    
    with app.app_context():
        db.create_all()
    
    return app


def create_database(app):
    if not path.exists('code/login/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    

