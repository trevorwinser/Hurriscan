from flask import Blueprint, render_template, request, redirect, url_for
import os
from . import user

navbar_bp = Blueprint('navbar', __name__, template_folder="../templates", static_folder="../static")

@navbar_bp.route('/navbar')
def navbar():
    if(user.currentUsername == ""):
        return redirect(url_for('auth.login'))
    else:
       return render_template('redirect_navbar.html')
