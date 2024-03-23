from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__, template_folder="../templates", static_folder="../static")

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully Logged In!', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try Again.', category="error")
        else:
            flash('Email does not exist.', category="error")
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET", "POST"])
def signUp():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = request.form.get('dob')
        
        if dob:  # Ensure 'dob' is not None or empty
            dateOfBirth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists.', category="error")
        elif len(password1) < 8:
            flash('Password must be greater than 7 characters', category='error')
        
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        else:
            flash('Account Created!', category="sucess")
            new_user = User(email=email, first_name=firstName, last_name=lastName, date_of_birth = dateOfBirth, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
            
    return render_template('registration.html')