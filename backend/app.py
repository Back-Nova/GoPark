# Configuración de Flask
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from conexion import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from datetime import datetime,timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import hashlib
app = Flask(__name__)
CORS(app)

# ----------- FRONTEND STATIC ---------------
@app.route('/')
def serve_pagina_prin():
    return send_from_directory('static/pagina-prin/browser', 'index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'GET':
        print("[LOGIN] Acceso a la página de login (GET)")
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
                if id_rol == 5:
                    return jsonify({"success": True, "redirect": "/jefe_pag"})
                elif id_rol == 6:
                    return jsonify({"success": True, "redirect": "/admin"})
                return jsonify({"success": True, "redirect": "/admin"})
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

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/api/recuperar_contra', methods=['POST'])
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


def enviar_correo(destinatario, codigo):
    remitente = 'gopark3139@gmail.com'
    contraseña = 'pcyqcrzhqimssxlu'
    asunto = 'Recuperación de contraseña - GoPark'
    mensaje = (
        f"Hola!\n\n"
        f"Tu código de recuperación es:\n\n"
        f"{codigo}\n\n"
        f"Este código expirará en 10 minutos.\n\n"
        f"Equipo GoPark 🚗"
    )

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        print("📤 Correo enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar el correo:", e)

        
@app.route('/api/verificar_codigo', methods=['POST'])
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
    
    
@app.route('/api/restablecer_contra', methods=['POST'])
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


@app.route('/recuperar_contra')
def serve_recuperar_contra():
    return send_from_directory('static/recuperar_contra/browser', 'index.html')




@app.route('/jefe_pag')
def serve_jefe_pag():
    return send_from_directory('static/jefe_pag/browser', 'index.html')



#--- Paquetes de rutas ---

@app.route("/api/paquetes", methods=["POST"])
def crear_paquete():
    print("==> Recibí una petición POST para crear paquete")
    data = request.get_json()
    print("Datos recibidos:", data)

    # Función para convertir valores vacíos a None
    def convertir_a_null(valor):
        return valor if valor not in [None, "", "null"] else None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Recolectar campos
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        precio = data.get("precio")
        cupos_totales = data.get("cupos_totales")
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")
        tipo = data.get("tipo")
        disponible = data.get("disponible")
        cupos_disponibles = data.get("cupos_disponibles")

        # Campos opcionales que podrían ser NULL
        vuelo = convertir_a_null(data.get("vuelo"))
        vehiculo = convertir_a_null(data.get("vehiculo"))
        alojamiento = convertir_a_null(data.get("alojamiento"))
        excursion = convertir_a_null(data.get("excursion"))

        # Insertar el paquete en la base de datos
        cursor.execute("""
            INSERT INTO paquete (
                nombre, descripcion, precio, cupos_totales, fecha_inicio, fecha_fin,
                tipo, disponible, cupos_disponibles, vuelo, vehiculo, alojamiento, excursion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nombre, descripcion, precio, cupos_totales, fecha_inicio, fecha_fin,
            tipo, disponible, cupos_disponibles,
            vuelo, vehiculo, alojamiento, excursion
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Paquete creado exitosamente")
        return jsonify({"message": "Paquete creado exitosamente"}), 201

    except Exception as e:
        print("Error al insertar paquete en la BD:", e)
        return jsonify({"message": "Error al crear el paquete", "error": str(e)}), 500
    
@app.route('/api/paquetes', methods=['GET'])
def obtener_paquetes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_paquete, nombre, descripcion, precio, cupos_disponibles, cupos_totales, fecha_inicio, fecha_fin, tipo FROM paquete")
    paquetes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    resultado = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": float(p[3]), "cupos_disponibles": p[4], "cupos_totales": p[5], "fecha_inicio": p[6], "fecha_fin": p[7], "tipo": p[8]}
        for p in paquetes
    ]
    return jsonify(resultado)

@app.route('/api/paquetes/<int:id>', methods=['DELETE'])
def eliminar_paquete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM paquete WHERE id_paquete = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Paquete eliminado correctamente"}), 200
#--- FIN DE PAQUETES ---

# -------- DESTINO --------

@app.route('/pagina_destino')
def serve_destino():
    return send_from_directory('static/destino/browser', 'index.html')

# GET - Listar destinos
@app.route('/api/destinos', methods=['GET'])
def obtener_destinos():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destino")
    columnas = [desc[0] for desc in cursor.description]
    destino = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(destino)


# POST - Crear destino
@app.route('/api/destinos', methods=['POST'])
def crear_destino():
    data = request.json
    pais = data.get('pais')
    ciudad = data.get('ciudad')
    region = data.get('region')
    descripcion = data.get('descripcion')

    if not pais or not ciudad or not region or not descripcion:
        return jsonify({'error': 'Faltan campos'}), 400

    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO destino (pais, ciudad, region, descripcion)
        VALUES (%s, %s, %s, %s)
    """, (pais, ciudad, region, descripcion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Destino creado correctamente'}), 201



# PUT - Actualizar destino
@app.route('/api/destinos/<int:id>', methods=['PUT'])
def actualizar_destino(id):
    data = request.json
    pais = data.get('pais')
    ciudad = data.get('ciudad')
    region = data.get('region')
    descripcion = data.get('descripcion')

    if not pais or not ciudad or not region or not descripcion:
        return jsonify({'error': 'Faltan campos'}), 400

    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE destino
        SET pais = %s, ciudad = %s, region = %s, descripcion = %s
        WHERE id_destino = %s
    """, (pais, ciudad, region, descripcion, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Destino actualizado correctamente'}), 200

# DELETE - Eliminar destino
@app.route('/api/destinos/<int:id>', methods=['DELETE'])
def eliminar_destino(id):
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM destino WHERE id_destino = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Destino eliminado correctamente'}), 200
# -------- FIN --------


# -------- RECURSOS --------

@app.route('/recursos')
def serve_recursos():
    return send_from_directory('static/recursos/browser', 'index.html')

@app.route('/api/alojamientos', methods=['GET'])
def get_alojamientos():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alojamiento")
    columnas = [desc[0] for desc in cursor.description]
    alojamientos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(alojamientos)

# Agregar alojamiento
@app.route('/api/alojamientos', methods=['POST'])
def agregar_alojamiento():
    data = request.json
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO alojamiento (nombre, descripcion, tipo_alojamiento, capacidad, precio, destino)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['nombre'], data['descripcion'], data['tipo_alojamiento'], data['capacidad'], data['precio'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Alojamiento agregado'}), 201

# Eliminar alojamiento
@app.route('/api/alojamientos/<int:id_alojamiento>', methods=['DELETE'])
def eliminar_alojamiento(id_alojamiento):
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM alojamiento WHERE id_alojamiento = %s", (id_alojamiento,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Alojamiento eliminado'}), 200



# Obtener vehículos
@app.route('/api/vehiculos', methods=['GET'])
def get_vehiculos():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo_alquiler")
    columnas = [desc[0] for desc in cursor.description]
    vehiculos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(vehiculos)

# Crear vehículo
@app.route('/api/vehiculos', methods=['POST'])
def crear_vehiculo():
    data = request.json
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehiculo_alquiler (marca, modelo, capacidad, destino)
        VALUES (%s, %s, %s, %s)
    """, (data['marca'], data['modelo'], data['capacidad'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vehículo agregado'}), 201

# Eliminar vehículo
@app.route('/api/vehiculos/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehiculo_alquiler WHERE id_vehiculo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vehículo eliminado'}), 200


# Obtener todos los vuelos
@app.route('/api/vuelos', methods=['GET'])
def get_vuelos():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Conexión fallida'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vuelo")
    columnas = [desc[0] for desc in cursor.description]
    vuelos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(vuelos)

# Crear un nuevo vuelo
@app.route('/api/vuelos', methods=['POST'])
def crear_vuelo():
    data = request.json
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Conexión fallida'}), 500

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vuelo (aerolinea, aeropuerto_o, aeropuerto_d, fecha, duracion, precio, destino)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['aerolinea'],
        data['aeropuerto_o'],
        data['aeropuerto_d'],
        data['fecha'],
        data['duracion'],
        data['precio'],
        data['destino']
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vuelo agregado correctamente'}), 201

# Eliminar vuelo
@app.route('/api/vuelos/<int:id>', methods=['DELETE'])
def eliminar_vuelo(id):
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Conexión fallida'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM vuelo WHERE id_vuelo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vuelo eliminado'}), 200


@app.route('/api/excursiones', methods=['GET'])
def obtener_excursiones():
    conn = get_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id_excursion, e.nombre, e.descripcion, e.duracion,
                   e.precio_adulto, e.precio_nino, e.participantes,
                   d.pais, d.ciudad
            FROM excursion e
            JOIN destino d ON e.destino = d.id_destino
        """)
        excursiones = cursor.fetchall()
        conn.close()

        resultado = []
        for e in excursiones:
            resultado.append({
                'id_excursion': e[0],
                'nombre': e[1],
                'descripcion': e[2],
                'duracion': e[3],
                'precio_adulto': float(e[4]),
                'precio_nino': float(e[5]),
                'participantes': e[6],
                'destino': f"{e[7]} - {e[8]}"
            })

        return jsonify(resultado)
    except Exception as e:
        print("❌ Error al obtener excursiones:", e)
        return jsonify({'error': 'Error al obtener excursiones'}), 500


@app.route('/api/excursiones', methods=['POST'])
def crear_excursion():
    data = request.json
    conn = get_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO excursion (nombre, descripcion, duracion, precio_adulto,
                                   precio_nino, participantes, destino)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre'], data['descripcion'], data['duracion'],
            data['precio_adulto'], data['precio_nino'],
            data['participantes'], data['destino']
        ))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Excursión creada con éxito'})
    except Exception as e:
        print("❌ Error al crear excursión:", e)
        return jsonify({'error': 'Error al crear excursión'}), 500


@app.route('/api/excursiones/<int:id_excursion>', methods=['DELETE'])
def eliminar_excursion(id_excursion):
    conn = get_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM excursion WHERE id_excursion = %s", (id_excursion,))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Excursión eliminada'})
    except Exception as e:
        print("❌ Error al eliminar excursión:", e)
        return jsonify({'error': 'Error al eliminar excursión'}), 500



# ------------------ FIN -------------------

@app.route('/admin')
def serve_admin():
    return send_from_directory('static/admin/browser', 'index.html')




# ------------------ ARRANCAR SERVIDOR -------------------
if __name__ == '__main__':
    print("Servidor Flask arrancando...")
    app.run(debug=True, port=5000)
