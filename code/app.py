from flask import Flask, render_template, jsonify, redirect, request
import os
import sqlite3
import sqlite_setup
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_setup.main()
app = Flask(__name__)

@app.route('/data-visualization')
def data_visualization():
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT month, SUM(temp) as total_temp FROM Data GROUP BY month')
    data = cur.fetchall()

    conn.close()

    months = [row['month'] for row in data]
    temps = [row['total_temp'] for row in data]

    return render_template('data_visualization.html', months=months, temps=temps)

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

        return redirect(url_for('alerts_page'))

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
            'alerts_email': row[5],
            'alerts_phone': row[6],
            'isAdmin': row[7]
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

@app.route('/initial-data')
def initial_data():
    try:
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude, humidity FROM Data;")

        data = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return jsonify(data), 200

    except sqlite3.Error as e:
        return f"Error {e} fetching initial data from database", 500

@app.route('/map-filter')
def mapfilter():
    return render_template('mapfilter-temp/mapfilter.html')

@app.route('/map-filter-data')
def mapfilterData():
    month = request.args.get('month')
    year = request.args.get('year')
    
    if month and year:
        # Convert month and year to integers
        month = int(month)
        year = int(year)
        
        # If month and year are provided, fetch filtered data from the database
        conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT latitude, longitude, humidity FROM Data WHERE month = ? AND year = ?;", (month, year))
            rows = cursor.fetchall()

        except sqlite3.Error as e:
            return f"Error {e} fetching filtered data from database", 500
        finally:
            conn.close()

        # Serialize the data to JSON format
        data = [{'latitude': row[0], 'longitude': row[1], 'humidity': row[2]} for row in rows]

        # Render the mapfilter.html template and pass the JSON data as a context variable
        return data, 200
    else:
        # If month and year are not provided, simply render the mapfilter.html template
        return initial_data()

@app.route('/temperature-filter')
def temperature_filter():
    # Handle temperature range filter
    min_temperature = request.args.get('minTemperature')
    max_temperature = request.args.get('maxTemperature')

    if min_temperature is not None and max_temperature is not None:
        # Apply temperature range filter
        connection = sqlite3.connect((os.path.join(basedir, 'hurriscan.db'))) 
        cursor = connection.cursor()
        cursor.execute("SELECT latitude, longitude, humidity FROM Data WHERE temperature BETWEEN ? AND ?", (min_temperature, max_temperature))
        filtered_data = cursor.fetchall()
        connection.close()
    else:
        # No filters applied, return all data
        connection = sqlite3.connect((os.path.join(basedir, 'hurriscan.db'))) 
        cursor = connection.cursor()
        cursor.execute("SELECT latitude, longitude, humidity FROM Data")
        filtered_data = cursor.fetchall()
        connection.close()

    return jsonify(filtered_data)


    return jsonify(filtered_data)
if __name__ == '__main__':
    app.run(debug=True)

