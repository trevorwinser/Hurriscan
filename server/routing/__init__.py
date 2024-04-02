from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

import sqlite_setup
sqlite_setup.main()
def create_app():
    app = Flask(__name__, static_folder= "../static", template_folder= "../templates")
    app.config['SECRET_KEY'] = "hurriscanKey"
    import os

    # Absolute directory path of this __init__.py file
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Use the absolute path in SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hurriscan.db')


    
    #import blueprints here
    from .views import views
    from .auth import auth
    from .admin import admin_bp
    from .mapFilter import mapfilter_bp
    from .data_visualization import data_visualization_bp
    from .alerts import alerts_bp
    from .user_dashboard import user_dashboard
    from .register import register_bp
    from .navbar import navbar_bp
    from .predictions import predictions_bp
    
    #register blueprints here
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(mapfilter_bp, url_prefix='/')
    app.register_blueprint(data_visualization_bp, url_prefix='/')
    app.register_blueprint(alerts_bp, url_prefix = '/')
    app.register_blueprint(user_dashboard, url_prefix='/')
    app.register_blueprint(register_bp, url_prefix='/')
    app.register_blueprint(navbar_bp, url_prefix='/')
    app.register_blueprint(predictions_bp, url_prefix='/')
    
    
    
    
    
        
        
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))  #swap out with call from database or from auth.py
    
    return app


# def create_database(app):
#     if not path.exists('server/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
    

