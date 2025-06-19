from flask import Blueprint, request, jsonify, send_from_directory
from conexion import get_connection
from correo_utils import enviar_correo
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets, hashlib

recuperar_bp = Blueprint('recuperar', __name__)

@recuperar_bp.route('/api/recuperar_contra', methods=['POST'])
def recuperar_contra():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email requerido'}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
    usuario = cur.fetchone()

    if usuario:
        id_usuario = usuario[0]
        print(f"📧 Usuario encontrado: {email} (id: {id_usuario})")

        # Generar código y su hash
        codigo = secrets.token_urlsafe(6)
        codigo_hash = hashlib.sha256(codigo.encode()).hexdigest()
        expiracion = datetime.now() + timedelta(minutes=10)

        # Guardar en la base
        cur.execute("""
            INSERT INTO recuperacion_cuenta (codigo, codigo_hash, expiracion, usuario)
            VALUES (%s, %s, %s, %s)
        """, (codigo, codigo_hash, expiracion, id_usuario))

        conn.commit()
        cur.close()
        conn.close()

        enviar_correo(email, codigo)
        print(f"✅ Código enviado: {codigo}")
        return jsonify({'message': 'Correo enviado con éxito'}), 200
    else:
        print(f"❌ Email no registrado: {email}")
        cur.close()
        conn.close()
        return jsonify({'message': 'El email no está registrado'}), 404


@recuperar_bp.route('/api/verificar_codigo', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    email = data.get('email')
    codigo = data.get('codigo')

    if not email or not codigo:
        return jsonify({"message": "Faltan datos."}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Verificar ID del usuario
    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
    user = cur.fetchone()
    if not user:
        print(f"❌ Usuario no encontrado para: {email}")
        return jsonify({"message": "Usuario no encontrado."}), 404

    id_usuario = user[0]
    codigo_hash = hashlib.sha256(codigo.encode()).hexdigest()

    cur.execute("""
        SELECT id_restablecer, expiracion FROM recuperacion_cuenta
        WHERE usuario = %s AND codigo = %s
        ORDER BY id_restablecer DESC LIMIT 1
    """, (id_usuario, codigo))
    resultado = cur.fetchone()

    if resultado:
        id_recuperacion, expiracion = resultado
        if datetime.now() > expiracion:
            print("⚠️ Código expirado.")
            return jsonify({"message": "El código ha expirado."}), 403
        print(f"✅ Código válido para usuario {email}")
        return jsonify({"message": "Código válido."}), 200
    else:
        print("❌ Código inválido.")
        return jsonify({"message": "Código incorrecto."}), 401

@recuperar_bp.route('/api/restablecer_contra', methods=['POST'])
def restablecer_contra():
    data = request.get_json()
    email = data.get('email')
    nueva_contra = data.get('nueva_contra')

    if not email or not nueva_contra:
        return jsonify({"message": "Faltan datos."}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
    user = cur.fetchone()
    if not user:
        print(f"❌ Usuario no encontrado para: {email}")
        return jsonify({"message": "Usuario no encontrado."}), 404

    id_usuario = user[0]
    hash_nueva = generate_password_hash(nueva_contra)

    cur.execute("UPDATE usuario SET contraseña = %s WHERE id_usuario = %s", (hash_nueva, id_usuario))
    conn.commit()

    cur.close()
    conn.close()
    print(f"🔐 Contraseña actualizada para {email}")
    return jsonify({"message": "Contraseña restablecida correctamente."}), 200

@recuperar_bp.route('/recuperar_contra')
def serve_recuperar_contra():
    return send_from_directory('static/recuperar_contra/browser', 'index.html')