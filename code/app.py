from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import calendar
from flask import jsonify


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hurriscan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    

    
@app.route('/data-visualization')
def data_visualization():
    conn = sqlite3.connect('hurriscan.db')
    curs = conn.cursor()
    curs.execute("SELECT month, AVG(temp) FROM Data GROUP BY month")
    results = curs.fetchall()
    conn.close()
    months = [calendar.month_name[int(row[0])] for row in results]  # Converts month numbers to names
    temps = [row[1] for row in results]
    return jsonify(months=months, temperatures=temps)

@app.route('/map-filter')
def mapfilter():
    # Connect directly to the database
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT latitude, longitude, humidity FROM Data;")
        rows = cursor.fetchall()

        # Convert the retrieved data to JavaScript format
        js_data = "const el_nino_data = {\n"
        js_data += "    max: 100,\n"
        js_data += "    data: [\n"

        for row in rows:
            js_data += f"        {{latitude: '{row[0]}', longitude: '{row[1]}', humidity: '{row[2]}'}}"

            # Add comma if not the last row
            if row != rows[-1]:
                js_data += ",\n"
            else:
                js_data += "\n"

        js_data += "    ]\n};"

        with open(os.path.join(basedir, 'static', 'js/el_nino_data.js'), 'w') as js_file:
            js_file.write(js_data)

    except sqlite3.Error as e:
        print("Error executing SQL statement:", e)

    finally:
        # Close the database connection
        conn.close()

    return render_template('mapfilter-temp/mapfilter.html')
    
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

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
