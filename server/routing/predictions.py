from flask import render_template, jsonify, request, Blueprint
import os
import sqlite3
from flask import jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

predictions_bp = Blueprint('predictions_bp', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))

@predictions_bp.route('/temperature-prediction-make')
def temperature_predictions_make():
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

def predict(month:int, latitude:float, longitude:float):
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
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

def hurricane_risk(humidity, air_temp, temp):
    if humidity > 85 and air_temp > 26 and temp > 27:  
        return "High"
    elif humidity > 75 and air_temp > 24 and temp > 25:
        return "Medium"
    else:
        return "Low"

@predictions_bp.route('/predictions-dashboard/send-text-alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    humidity = data['humidity']
    temperature = data['temperature']
    airPressure = data['airPressure']
    risk = data['risk']

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    body = f"Humidity: {humidity}, Temperature: {temperature}, Air Pressure: {airPressure}, Risk: {risk}"

    conn = sqlite3.connect('routing/hurriscan.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User;")
    users = cursor.fetchall()

    for user in users:
        phone = user[6]
        email = user[5]
        message = client.messages.create(
            from_='+19163024424', 
            body=body,
            to=phone
        )

        message = Mail(
            from_email='noah.stasuik@gmail.com',
            to_emails=email,
            subject='Hurriscan Alert!',
            html_content=body)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    conn.close()

    return jsonify(message="Alert sent"), 200 

@predictions_bp.route('/predictions-dashboard')
def predictions_dashboard():
    return render_template('predictions_dashboard.html')