from flask import Blueprint, render_template

navbar_bp = Blueprint('navbar', __name__, template_folder="../templates", static_folder="../static")

@navbar_bp.route('/navbar')
def navbar():
    return render_template('redirect_navbar.html')