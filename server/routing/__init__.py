from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'hurriscan.db'

def create_app():
    app = Flask(__name__, static_folder= "../static", template_folder= "../templates")
    app.config['SECRET_KEY'] = "hurriscanKey"
    import os

    # Absolute directory path of this __init__.py file
    basedir = os.path.abspath(os.path.dirname(__file__))

    DB_NAME = 'hurriscan.db'

    # Use the absolute path in SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_NAME)

    db.init_app(app)
    
    #import blueprints here
    from .views import views
    from .auth import auth
    
    #register blueprints here
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    
    
    
    
    with app.app_context():
        db.create_all()
        
        
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))  #swap out with call from database or from auth.py
    
    return app


def create_database(app):
    if not path.exists('server/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    

