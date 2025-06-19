from flask import Blueprint, request, jsonify, send_from_directory
from conexion import get_connection
from werkzeug.security import check_password_hash
import psycopg2

auth_login = Blueprint('auth_login', __name__)


@auth_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return send_from_directory('static/login/browser', 'index.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        print(f"[LOGIN] Datos recibidos (POST): {data}")

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            print("[LOGIN] Campos incompletos")
            return jsonify({"success": False, "message": "Todos los campos son obligatorios."})

        conn = get_connection()
        if conn is None:
            print("[LOGIN] Error al conectar a la base de datos")
            return jsonify({"success": False, "message": "Error de conexión a la BD"})

        try:
            cursor = conn.cursor()

            sql = """
                SELECT id_usuario, nombre, apellido, email, contraseña, id_rol 
                FROM usuario 
                WHERE email = %s
            """
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()
            print(f"[LOGIN] Resultado de búsqueda de usuario: {usuario}")

            if usuario is None:
                print("[LOGIN] Email no encontrado en la base de datos")
                return jsonify({"success": False, "message": "Email no encontrado."})

            id_usuario, nombre, apellido, email_db, password_hash, id_rol = usuario

            if check_password_hash(password_hash, password):
                print(f"[LOGIN] Contraseña correcta. Usuario: {nombre} {apellido}, ID: {id_usuario}, Rol: {id_rol}")
    
                datos_usuario = {
                    "id_usuario": id_usuario,
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email_db
                }
                if id_rol == 5:
                    return jsonify({"success": True, "redirect": "/jefe_pag", "usuario": datos_usuario})
                elif id_rol == 6:
                    return jsonify({"success": True, "redirect": "/cliente", "usuario": datos_usuario})
                
                return jsonify({"success": True, "redirect": "/admin", "usuario": datos_usuario})
            else:
                print("[LOGIN] Contraseña incorrecta")
                return jsonify({"success": False, "message": "Contraseña incorrecta"})

        except psycopg2.Error as e:
            print(f"[LOGIN] Error al ejecutar consulta SQL: {e}")
            return jsonify({"success": False, "message": "Error al iniciar sesión"})

        finally:
            cursor.close()
            conn.close()
            print("[LOGIN] Conexión cerrada")