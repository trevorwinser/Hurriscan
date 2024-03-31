from flask import Blueprint, render_template, request, jsonify
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sqlite3
import pandas as pd

predictions_bp = Blueprint('predictions_bp', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))



@predictions_bp.route('/temperature-predictions',)
def temperature_predictions_default():
    return render_template('temperature_predictions.html')

@predictions_bp.route('/temperature-prediction-make')
def temperature_predictions():
    try:
        month = int(request.args.get('month')) if 'month' in request.args else None
        if month is None:
            return render_template('temperature_predictions.html')
        latitude = float(request.args.get('latitude'))if 'latitude' in request.args else None
        longitude = float(request.args.get('longitude'))if 'longitude' in request.args else None
        temperature, humidity, air = predict(month, latitude, longitude)
        return jsonify(temperature=temperature, humidity=humidity, air=air)
    except Exception as e:
        return f"Error {e} fetching predictions from database", 500

def predict(month:int, latitude:float, longitude:float):
    try:
        conn = sqlite3.connect('hurriscan.db')
        query = "SELECT month, AVG(temp) AS avg_temp, AVG(humidity) AS avg_humidity, AVG(air) AS avg_air FROM Data GROUP BY month"
        if latitude is not None and longitude is not None:
            latitude_min = latitude -10
            latitude_max = latitude +10
            longitude_min = longitude -10
            longitude_max = longitude +10
            query = f"SELECT month, AVG(temp) AS avg_temp, AVG(humidity) AS avg_humidity, AVG(air) AS avg_air FROM Data WHERE latitude BETWEEN {latitude_min} AND {latitude_max} AND longitude BETWEEN {longitude_min} AND {longitude_max} GROUP BY month"
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error connecting to database or executing query: {e}")
        raise e
    finally:
        if conn:
            conn.close()
    try:
        if month is not None:
            if not df[df['month'] == int(month)].empty:
                X = df[['month']]
                y = df[['avg_temp', 'avg_humidity', 'avg_air']]
                model = LinearRegression()
                model.fit(X, y)
                predicted_values = model.predict([[month]])
                temperature = predicted_values[0][0]
                humidity = predicted_values[0][1]
                air = predicted_values[0][2]
                return temperature, humidity, air
            else:
                raise Exception(f"No data available for month {month} {df[['month']]}")
        else:
            return None, None, None
    except Exception as e:
        print(f"Error predicting: {e}")
        raise e