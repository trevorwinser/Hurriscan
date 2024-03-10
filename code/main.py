from flask import Flask
from admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)

@app.route('/')
def hello_world():
    return 'Hello World!', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)
