from flask import Flask, send_from_directory, request
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static/browser', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
