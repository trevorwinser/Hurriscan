
from flask import Blueprint, render_template, request

register_bp = Blueprint('register', __name__, template_folder="../templates", static_folder="../static")

@register_bp.route('/registration')
def registration():
    return render_template('registration.html')

@register_bp.route('/createAccount')
def createAcc():
    return render_template('accountCreation.html')

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