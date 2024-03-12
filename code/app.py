from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

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
    # Connect directly to the database
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    cur = conn.cursor()

    # Execute a query to fetch data from your table
    cur.execute('SELECT month, SUM(temp) as total_temp FROM Data GROUP BY month')
    data = cur.fetchall()  # Fetches all rows as a list of dicts

    # Close the connection
    conn.close()

    # Convert data to format suitable for visualization (e.g., lists of labels and values)
    months = [row['month'] for row in data]
    temps = [row['total_temp'] for row in data]

    # Pass this data to your template
    return render_template('data_visualization.html', months=months, temps=temps)

@app.route('/map-filter')
def mapfilter():
    # Connect to the SQLite database
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cursor = conn.cursor()

    try:
        # Execute SQL SELECT statement to retrieve latitude, longitude, and humidity
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

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
