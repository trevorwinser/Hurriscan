from flask import Flask, render_template, jsonify, redirect, request
import os
import sqlite3
import calendar
from flask import jsonify
import json
import pandas as pd
import numpy as np

import sqlite_setup
from datetime import datetime

from twilio.rest import Client

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_setup.main()


app = Flask(__name__)

@app.route('/temperature-predictions', defaults={'month': None})
@app.route('/temperature-predictions/<int:month>')
def temperature_predictions(month):
    try:
        conn = sqlite3.connect('hurriscan.db')
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
  

@app.route('/login')
def login():
    return render_template('login/login.html')

@app.route('/registration')
def registration():
    return render_template('registration/registration.html')

@app.route('/createAccount')
def createAcc():
    return render_template('registration/accountCreation.html')

        
    try:
        sql = buildSQL()
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = [{'latitude': row[0], 'longitude': row[1], 'temp': row[2]} for row in rows]
        return jsonify(data), 200

    except sqlite3.Error as e:
        return jsonify({'error': f"Error {e} fetching filtered data from database"}), 500
    except Exception as e:
        return jsonify({'error': f"Error {e} fetching filtered data from database"}), 500
    finally:
        conn.close()
    
def buildSQL():
    sql = "SELECT latitude, longitude, temp FROM Data"
    month = request.args.get('month')
    year = request.args.get('year')
    min_temperature = request.args.get('minTemperature')
    max_temperature = request.args.get('maxTemperature')
    if(month and year):
        sql += " WHERE month = " + month + " AND year = " + year
    if(min_temperature and max_temperature):
        if(month and year):
            sql += " AND "
        else:
            sql += " WHERE "
        sql += "temp BETWEEN " + min_temperature + " AND " + max_temperature
    return sql



if __name__ == '__main__':
    app.run(debug=True)
