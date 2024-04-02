from flask import Blueprint, render_template, request
import os
import sqlite3
import calendar

user_dashboard = Blueprint('user_dashboard', __name__, template_folder="../templates", static_folder="../static")



@user_dashboard.route('/user_dashboard')
def dashboard():
    return render_template('user_dashboard.html')