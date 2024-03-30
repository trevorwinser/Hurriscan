from flask import Blueprint, render_template, request, jsonify
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sqlite3
import pandas as pd

predictions_bp = Blueprint('predictions_bp', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))



@predictions_bp.route('/temperature-predictions', defaults={'month': None})
@predictions_bp.route('/temperature-predictions/<int:month>')
def temperature_predictions(month):
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        df = pd.read_sql_query("SELECT month, AVG(temp) AS avg_temp, AVG(humidity) AS avg_humidity, AVG(air) AS avg_air FROM Data GROUP BY month", conn)
    except Exception as e:
        print(f"Error connecting to database or executing query: {e}")
        return jsonify(error="Database error"), 500
    finally:
        if conn:
            conn.close()
    if request.is_json or month is not None:
        if month and not df[df['month'] == month].empty:
            X = df[['month']]
            y = df[['avg_temp', 'avg_humidity', 'avg_air']]
            model = LinearRegression()
            model.fit(X, y)
            predicted_values = model.predict([[month]])
            return jsonify(month=month, temperature=predicted_values[0][0], humidity=predicted_values[0][1], air=predicted_values[0][2])
        else:
            return jsonify(error="No data available"), 404
    return render_template('temperature_predictions.html')

@predictions_bp.route('/predictions-dashboard')
def predictions_dashboard():
    return render_template('predictions-dashboard.html')