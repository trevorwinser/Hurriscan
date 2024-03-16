from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__, template_folder="../templates", static_folder="../static")



@auth.route('/login', methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"

@auth.route('/sign-up', methods=["GET", "POST"])
def signUp():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if len(password) < 8:
            pass
        else:
            pass
    return render_template('registration.html')