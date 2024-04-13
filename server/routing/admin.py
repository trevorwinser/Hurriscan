from flask import Blueprint, render_template, jsonify, redirect, request,url_for
import os
import sqlite3
from datetime import datetime
from routing import user

admin_bp = Blueprint('admin', __name__, template_folder="../templates", static_folder="../static")

basedir = os.path.abspath(os.path.dirname(__file__))

@admin_bp.route('/admin')
def admin_dashboard():
    
    if(user.currentUsername != ""):
        if(user.isAdmin == True):
            return render_template('admin_dashboard.html')
        else:
            return redirect(url_for('views.home'))
        
    else:
        return redirect(url_for('auth.login'))
    

@admin_bp.route('/redirect-navbar')
def admin_nav_bar():
    
    if(user.currentUsername != ""):
        if(user.isAdmin == True):
            return render_template('redirect_navbar.html', username = user.currentUsername)
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

@admin_bp.route('/users')
def get_users():
    if(user.currentUsername != ""):
        if(user.isAdmin == True):
             
            conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute('SELECT id, username, alerts_email, alerts_phone, isAdmin FROM User')
            rows = cur.fetchall()

            users = []
            for row in rows:
                user1 = {
                    'id': row[0],
                    'username': row[1],
                    'alerts_email': row[2],
                    'alerts_phone': row[3],
                    'isAdmin': row[4]
                }
                users.append(user1)

            conn.close()
            return jsonify(users)
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))

            
    


@admin_bp.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    if(user.currentUsername != ""):
        if(user.isAdmin == True):
            try:
                conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
                cur = conn.cursor()
                cur.execute('DELETE FROM User WHERE id = ?', (user_id,))
                conn.commit()
                
                conn.close()
                return redirect('/admin')

            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))
    
@admin_bp.route('/create-alert', methods=['POST'])
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

    return redirect('/admin')
    
    
