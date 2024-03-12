from flask import Flask, render_template
from flask import Blueprint, request
import sqlite3

app = Flask(__name__)
dataset_bp = Blueprint('dataset', __name__)

@dataset_bp.route('/data_flask/dataset', methods=['GET'])
def display_dataset():
    # Connect to the database
    conn = sqlite3.connect('/../hurriscan.db')
    cursor = conn.cursor()

    # Fetch the data from the database
    cursor.execute('SELECT * FROM Data LIMIT 20')  # Modify this query as per your database structure
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the HTML template and pass the data to it
    return render_template('/../front-end/nav-bar/admin-dashboard/dataset.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
