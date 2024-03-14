from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__, template_folder="../templates", static_folder="../static")



@auth.route('/login', methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"

@auth.route('/sign-Up', methods=["GET", "POST"])
def signUp():
    return "<h1>Sign Up</h1>"