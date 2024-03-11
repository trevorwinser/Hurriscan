from flask import Flask
from flask_cors import CORS

from admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)
CORS(app, origins="*", expose_headers="*", allow_headers="*")


@app.route('/')
def hello_world():
    return 'Hello World!', 200


if __name__ == "__main__":
    port = 7070
    app.run(host="0.0.0.0", port=port)
