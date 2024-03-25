from flask import Blueprint, redirect, url_for, render_template
from flask_login import  login_required,  current_user
from . import user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if(user.currentUsername == ""):
        redirect(url_for('auth.login'))
    
    
    return render_template('user-dashboard.html')