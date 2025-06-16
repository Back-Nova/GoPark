# Configuración de Flask
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from conexion import get_connection
from werkzeug.security import generate_password_hash
import psycopg2
from datetime import datetime


app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_pagina_prin():
    return send_from_directory('static/pagina-prin/browser', 'index.html')

@app.route('/login')
def serve_login():
    print("Geniooooo")
    return send_from_directory('static/login/browser', 'index.html')

# SERVIR TU HTML DE REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print("Estas en el registro (GET)")
        return send_from_directory('static/register/browser', 'index.html')
    
    elif request.method == 'POST':
        data = request.get_json()

        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol')

        if not all([nombre, apellido, email, password, rol]):
            return jsonify({"success": False, "message": "Todos los campos son obligatorios."})

        try:
            rol = int(rol)
        except ValueError:
            return jsonify({"success": False, "message": "Rol inválido."})

        # Hasheamos la contraseña
        password_hash = generate_password_hash(password)

        conn = get_connection()
        if conn is None:
            print("No se pudo conectar a la base de datos")
            return jsonify({"success": False, "message": "Error de conexión a la BD"})

        try:
            cursor = conn.cursor()

            # Insertamos el usuario
            sql_usuario = """
                INSERT INTO usuario (nombre, apellido, email, contraseña, id_rol)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_usuario;
            """
            valores_usuario = (nombre, apellido, email, password_hash, rol)
            cursor.execute(sql_usuario, valores_usuario)
            id_usuario = cursor.fetchone()[0]  # Obtenemos el id insertado

            # Insertamos la sesión inicial COMPLETA
            sql_sesion = """
                INSERT INTO sesion_usuario (fecha_sesion, ip_address, sesion_activa, id_usuario)
                VALUES (%s, %s, %s, %s)
            """
            fecha_sesion = datetime.now()  # Fecha actual
            ip_address = "0.0.0.0"  # Por ahora fijo, se puede obtener la IP real si querés
            sesion_activa = True

            valores_sesion = (fecha_sesion, ip_address, sesion_activa, id_usuario)
            cursor.execute(sql_sesion, valores_sesion)

            conn.commit()

            return jsonify({"success": True, "message": "Usuario registrado correctamente"})
        
        except psycopg2.Error as e:
            print("Error al insertar en la base de datos:", e)
            return jsonify({"success": False, "message": "Error al registrar"})
        
        finally:
            cursor.close()
            conn.close()

@app.route('/recuperar_contra')
def serve_recuperar_contra():
    print("Geniooooo")
    return send_from_directory('static/recuperar_contra/browser', 'index.html')

if __name__ == '__main__':
    print("Servidor Flask arrancando...")
    app.run(debug=True, port=4200)


# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS

# from conexion import get_connection
# import os

# app = Flask(__name__, static_folder='static/browser', static_url_path='')
# CORS(app)

# # Ruta principal (por si entran al home)
# @app.route('/')
# def serve_index():
#     print("Acceso a / (index)")
#     return send_from_directory(app.static_folder, 'index.html')

# # Ruta GET /login para servir el index.html (angular maneja luego el frontend)
# @app.route('/login')
# def serve_login():
#     print("Se accedió a la ruta /login (GET)")
#     return send_from_directory(app.static_folder, 'index.html')

# # Ruta POST /login para procesar el login
# @app.route('/login', methods=['POST'])
# def process_login():
#     print("Se recibió un POST en /login")
#     try:
#         data = request.json
#         if data is None:
#             print("No se recibió JSON en la petición")
#             return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400

#         email = data.get('email')
#         password = data.get('password')
#         print(f"Intentando login con email: {email}")

#         conn = get_connection()
#         if conn is None:
#             print("Error: No se pudo conectar a la base de datos")
#             return jsonify({'success': False, 'message': 'No se pudo conectar a la base de datos'}), 500
        
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT id_usuario, nombre, apellido FROM usuario
#             WHERE email = %s AND "contraseña" = %s
#         """, (email, password))

#         user = cursor.fetchone()
#         conn.close()

#         if user:
#             print(f"Login exitoso para usuario ID: {user[0]}")
#             return jsonify({'success': True, 'message': 'Login exitoso', 'user': {
#                 'id': user[0],
#                 'nombre': user[1],
#                 'apellido': user[2]
#             }})
#         else:
#             print("Usuario o contraseña incorrectos")
#             return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

#     except Exception as e:
#         print("Error general en login:", e)
#         return jsonify({'success': False, 'message': 'Error en el servidor'}), 500


# # Ruta GET /register (sirve el index.html para el frontend)
# @app.route('/register', methods=['GET'])
# def serve_register():
#     print("Se accedió a la ruta /register (GET)")
#     return send_from_directory(app.static_folder, 'register.html')

# # Ruta POST /register para registrar usuario
# @app.route('/register', methods=['POST'])
# def process_register():
#     print("Se recibió un POST en /register")
#     try:
#         data = request.json
#         if data is None:
#             print("No se recibió JSON en la petición")
#             return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400

#         nombre = data.get('nombre')
#         apellido = data.get('apellido')
#         email = data.get('email')
#         password = data.get('password')
#         rol = 2  # por defecto, le ponemos rol 2 (después podemos mejorar esto)

#         print(f"Intentando registrar usuario: {email}")

#         conn = get_connection()
#         if conn is None:
#             print("Error: No se pudo conectar a la base de datos")
#             return jsonify({'success': False, 'message': 'No se pudo conectar a la base de datos'}), 500
        
#         cursor = conn.cursor()

#         # Primero verificamos si el email ya existe
#         cursor.execute("""
#             SELECT id_usuario FROM usuario WHERE email = %s
#         """, (email,))
#         existing_user = cursor.fetchone()

#         if existing_user:
#             print("El email ya está registrado.")
#             return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409

#         # Insertar nuevo usuario
#         cursor.execute("""
#             INSERT INTO usuario (nombre, apellido, email, rol, "contraseña")
#             VALUES (%s, %s, %s, %s, %s)
#         """, (nombre, apellido, email, rol, password))

#         conn.commit()
#         conn.close()

#         print("Usuario registrado correctamente")
#         return jsonify({'success': True, 'message': 'Usuario registrado correctamente'})

#     except Exception as e:
#         print("Error general en registro:", e)
#         return jsonify({'success': False, 'message': 'Error en el servidor'}), 500




# if __name__ == '__main__':
#     print("Servidor Flask arrancando...")
#     app.run(debug=True, port=4200)
