import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user

import sqlite3
import csv
from . import user

predictions = Blueprint('predictions', __name__, template_folder="../templates", static_folder="../static")

@predictions.route("/predictions", methods = ["GET", "POST"])
def dashboard():
    return render_template('predictions-dashboard.html')