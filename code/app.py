from flask import Flask, render_template, jsonify, redirect, request
import os
import sqlite3
import calendar
from flask import jsonify
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import logging

import sqlite_setup
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from twilio.rest import Client

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_setup.main()


app = Flask(__name__)

@app.route('/temperature-predictions',)
def temperature_predictions_default():
    return render_template('temperature_predictions.html')

@app.route('/temperature-prediction-make')
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

#this is the graph in the predictions dashboard
@app.route('/temperature-predictions', defaults={'month': None})
@app.route('/temperature-predictions/<int:month>')
def temperature_predictions(month):
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
            return jsonify(error="No data available"), 404
    return render_template('temperature_predictions.html')

#this is the graph in the user-dashboard 
@app.route('/data-visualization')
def data_visualization():
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    curs = conn.cursor()
    curs.execute("SELECT month, AVG(temp) FROM Data GROUP BY month")
    results = curs.fetchall()
    conn.close()
    months = [calendar.month_name[int(row[0])] for row in results] 
    temperatures = [row[1] for row in results]
    return render_template('data_visualization.html',months=months, temperatures=temperatures)

#this is graph #2 where the user can pick a month and it also goes in the user dashboard
@app.route('/data-visualization/<int:year>/<int:month>')
def get_monthly_data(year, month):
    conn = sqlite3.connect('hurriscan.db')
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

@app.route('/')
def home():
    return 'Welcome to the Home Page'

@app.route('/login')
def login():
    return render_template('login/login.html')

@app.route('/registration')
def registration():
    return render_template('registration/registration.html')

@app.route('/createAccount')
def createAcc():
    return render_template('registration/accountCreation.html')

@app.route('/alerts', methods=['GET', 'POST'])
def alerts_page():
    if request.method == 'POST':
        phone = request.form.get('phone')
        email = request.form.get('email')
        east_coast = request.form.get('east-coast')
        west_coast = request.form.get('west-coast')

        if '@' not in email or len(phone) < 10:
            return "Invalid email or phone number"

        if east_coast and west_coast:
            zone = 'both'
        elif east_coast:
            zone = 'east'
        elif west_coast:
            zone = 'west'
        else:
            return "No zone selected"

        conn = sqlite3.connect('hurriscan.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE User
            SET phone = ?, email = ?, alerts_email = 1, alerts_phone = 1, zone = ?
            WHERE username = "User1";
        ''', (phone, email, zone))

        conn.commit()
        conn.close()

        return redirect('alerts_page')

    return render_template('alerts.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/admin-dashboard.html')

@app.route('/admin-nav-bar')
def admin_nav_bar():
    return render_template('admin/admin-nav-bar.html')

@app.route('/users')
def get_users():
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT * FROM User')
    rows = cur.fetchall()

    users = []
    for row in rows:
        user = {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'email': row[3],
            'phone': row[4],
            'zone': row[5],
            'alerts_email': row[6],
            'alerts_phone': row[7],
            'isAdmin': row[8]
        }
        users.append(user)

    conn.close()
    return jsonify(users)

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        cur = conn.cursor()
        cur.execute('DELETE FROM User WHERE id = ?', (user_id,))
        conn.commit()
        cur.execute("SELECT * FROM User;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        conn.close()
        return redirect('/admin') # Doesn't do anything, but needed to return something ¯\_(ツ)_/¯

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create-alert', methods=['POST'])
def create_alert():
    title = request.form['title']
    text = request.form['text']
    date = datetime.now().date()

    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cur = conn.cursor()
    cur.execute('INSERT INTO Alert (title, text, date) VALUES (?, ?, ?)', (title, text, date))
    conn.commit()
    cur.execute('SELECT * FROM Alert')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

    return redirect('/alerts') # Wrong path but will change later!

@app.route('/map-filter')
def mapfilter():
    return render_template('mapfilter-temp/mapfilter.html')

@app.route('/user-dashboard')
def user_dashboard():
    return render_template('user-dashboard.html')


@app.route('/map-filter-data')
def mapfilterData():         
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
        
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

def hurricane_risk(humidity, air_temp, temp):
    if humidity > 85 and air_temp > 26 and temp > 27:  
        return "High"
    elif humidity > 75 and air_temp > 24 and temp > 25:
        return "Medium"
    else:
        return "Low"
        
def send_alert(user, month, risk, kind):
    
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    if account_sid is None or auth_token is None:
        raise ValueError('TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set')
    
    if kind == 'email':
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        message = Mail(
            from_email="noah.stasuik@gmail.com",
            to_emails=user.get("email"),
            subject='Hurriscan Alert!',
            html_content='<strong>Warning!</strong> Hurricane Activity in your area!!')
        response = sg.send(message)
        return response.status_code
    elif kind == 'phone':
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+15005550006',
            body='Alert Hurricane Risk: ' + str(risk) + '\n' + 'Month: ' + str(month),
            to=user.get("phone")  
        )
        return message.sid
    else:
        return 0

@app.route('/predictions-dashboard/alerts', methods=['POST'])
def predictions_dashboard_alerts():
    north_america = request.form.get('north_america')
    south_america = request.form.get('south_america')
    print(north_america, south_america)
    if north_america and south_america:
        return "Both zones selected", 400
    elif north_america:
        zone = 'north'
    elif south_america:
        zone = 'south'
    else:
        return "No zone selected", 400
    month = 6
    risk = hurricane_risk(month, zone)
    
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        sql = "SELECT * FROM User WHERE alerts_email != 0"
        cur.execute(sql)
        user_rows = cur.fetchall()
        for user_row in user_rows:
            user = {
            'id': user_row[0],
            'username': user_row[1],
            'password': user_row[2],
            'email': user_row[3],
            'phone': user_row[4],
            'zone': user_row[5],
            'alerts_email': user_row[6],
            'alerts_phone': user_row[7],
            'isAdmin': user_row[8]
            }
            send_alert(user, month, risk, 'email')
        sql = "SELECT * FROM User WHERE alerts_phone != 0"
        cur.execute(sql)
        user_rows = cur.fetchall()
        for user_row in user_rows:
            user = {
            'id': user_row[0],
            'username': user_row[1],
            'password': user_row[2],
            'email': user_row[3],
            'phone': user_row[4],
            'zone': user_row[5],
            'alerts_email': user_row[6],
            'alerts_phone': user_row[7],
            'isAdmin': user_row[8]
            }
            send_alert(user, month, risk, 'phone')
        return "Alerts sent", 200  
    except sqlite3.Error as e:
        return f"Error {e} fetching user data from database", 500
    except Exception as e:
        return f"Error {e} fetching user data from database", 500
    finally:
        conn.close() 
@app.route('/predictions-dashboard')
def predictions_dashboard():
    return render_template('predictions-dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
