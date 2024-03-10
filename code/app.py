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
    cur.execute('SELECT month, SUM(temp) as total_temp FROM new_table GROUP BY month')
    data = cur.fetchall()  # Fetches all rows as a list of dicts

    # Close the connection
    conn.close()

    # Convert data to format suitable for visualization (e.g., lists of labels and values)
    months = [row['month'] for row in data]
    temps = [row['total_temp'] for row in data]

    # Pass this data to your template
    return render_template('data_visualization.html', months=months, temps=temps)

@app.route('/')
def home():
    return 'Welcome to the Home Page'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
