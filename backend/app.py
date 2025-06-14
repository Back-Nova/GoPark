from flask import Flask, send_from_directory, request, jsonify
import os


# Inicializamos la app
app = Flask(__name__, static_folder='static')

# 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    full_path = os.path.join(app.static_folder, 'browser', path)

    if path != "" and os.path.exists(full_path):
        return send_from_directory(os.path.join(app.static_folder, 'browser'), path)
    else:
        return send_from_directory(os.path.join(app.static_folder, 'browser'), 'index.html')


if __name__ == '__main__':
    app.run(debug=True)