from flask import Blueprint, render_template, request, url_for, redirect
import os
import sqlite3
import calendar
from . import user

data_visualization_bp = Blueprint('data_visualization', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))

@data_visualization_bp.route('/data-visualization')
def data_visualization():
    if(user.currentUsername == ""):
        return redirect(url_for('auth.login'))
    else:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        curs = conn.cursor()
        curs.execute("SELECT month, AVG(temp) FROM Data GROUP BY month")
        results = curs.fetchall()
        conn.close()
        months = [calendar.month_name[int(row[0])] for row in results]  # Convert month numbers to names
        temperatures = [row[1] for row in results]
        # Return the template with data included
        return render_template('data_visualization.html', months=months, temperatures=temperatures)

@data_visualization_bp.route('/data-visualization/<int:year>/<int:month>')
def get_monthly_data(year, month):
    if(user.currentUsername == ""):
        return redirect(url_for('auth.login'))
    else:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        curs = conn.cursor()
        curs.execute("SELECT AVG(humidity), AVG(air), AVG(temp), AVG(zon_winds), AVG(mer_winds) FROM Data WHERE year = ? AND month = ?", (year, month))
        data = curs.fetchone()
        conn.close()
        if data:
            labels = ['Humidity', 'Air', 'Temperature', 'Zon Winds', 'Mer Winds']
            values = [data[0], data[1], data[2], data[3], data[4]]
            return render_template('filter_visualization.html', year=year, month=month, labels=labels, values=values)
        else:
            return render_template('filter_visualization.html', error="No data found")
