from flask import Blueprint, request, jsonify, send_from_directory
from conexion import get_connection
from werkzeug.security import generate_password_hash
from datetime import datetime
import psycopg2

auth_register = Blueprint('auth_register', __name__)

@auth_register.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
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

        password_hash = generate_password_hash(password)

        conn = get_connection()
        if conn is None:
            return jsonify({"success": False, "message": "Error de conexión a la BD"})

        try:
            cursor = conn.cursor()

            sql_usuario = """
                INSERT INTO usuario (nombre, apellido, email, contraseña, id_rol)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_usuario;
            """
            valores_usuario = (nombre, apellido, email, password_hash, rol)
            cursor.execute(sql_usuario, valores_usuario)
            id_usuario = cursor.fetchone()[0]

            sql_sesion = """
                INSERT INTO sesion_usuario (fecha_sesion, ip_address, sesion_activa, id_usuario)
                VALUES (%s, %s, %s, %s)
            """
            fecha_sesion = datetime.now()
            ip_address = "0.0.0.0"
            sesion_activa = True

            valores_sesion = (fecha_sesion, ip_address, sesion_activa, id_usuario)
            cursor.execute(sql_sesion, valores_sesion)

            conn.commit()

            return jsonify({"success": True, "message": "Usuario registrado correctamente"})
        
        except psycopg2.Error as e:
            return jsonify({"success": False, "message": "Error al registrar"})
        
        finally:
            cursor.close()
            conn.close()