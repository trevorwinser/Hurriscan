from flask import Blueprint, redirect, url_for, render_template
from flask_login import  login_required,  current_user
from . import user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    
    if(user.currentUsername == ""):
        return redirect(url_for('auth.login'))
    else:
        return render_template('nav_bar.html', username=user.currentUsername)