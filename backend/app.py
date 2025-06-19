# Configuración de Flask
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from conexion import get_connection

from auth.login import auth_login
from auth.register import auth_register
from auth.recuperar import recuperar_bp
from admin.recursos import recursos_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_login)
app.register_blueprint(auth_register)
app.register_blueprint(recuperar_bp)
app.register_blueprint(recursos_bp)

# ----------- PAGINAS  SOLO CON LAS RUTAS ---------------
@app.route('/')
def serve_pagina_prin():
    return send_from_directory('static/pagina-prin/browser', 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory('static/admin/browser', 'index.html')

@app.route('/api/admin/paquetes')
def obtener_paquetes_admin():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_paquete, nombre, descripcion, precio, cupos_totales, cupos_disponibles,
               fecha_inicio, fecha_fin, tipo, disponible, vuelo, vehiculo, alojamiento, excursion
        FROM paquete
    """)
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(datos)


@app.route('/api/admin/usuarios')
def obtener_jefes_venta():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_usuario, nombre, apellido, email FROM usuario WHERE id_rol = 5
    """)
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(datos)

# Eliminar paquete
@app.route('/api/admin/paquetes/<int:id_paquete>', methods=['DELETE'])
def eliminar_paquete_admin(id_paquete):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Conexión fallida"}), 500
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM paquete WHERE id_paquete = %s", (id_paquete,))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Eliminar usuario (solo jefes de venta)
@app.route('/api/admin/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario_admin(id_usuario):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Conexión fallida"}), 500
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE id_usuario = %s AND id_rol = 5", (id_usuario,))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/admin/paquetes/<int:id>', methods=['PUT'])
def editar_paquete_admin(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE paquete
        SET nombre = %s, descripcion = %s, precio = %s, cupos_totales = %s,
            cupos_disponibles = %s, fecha_inicio = %s, fecha_fin = %s, tipo = %s,
            disponible = %s, vuelo = %s, vehiculo = %s, alojamiento = %s, excursion = %s
        WHERE id_paquete = %s
    """, (
        data['nombre'], data['descripcion'], data['precio'], data['cupos_totales'],
        data['cupos_disponibles'], data['fecha_inicio'], data['fecha_fin'], data['tipo'],
        data['disponible'], data['vuelo'], data['vehiculo'], data['alojamiento'],
        data['excursion'], id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/admin/usuarios/<int:id>', methods=['PUT'])
def editar_usuario_admin(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuario
        SET nombre = %s, apellido = %s, email = %s
        WHERE id_usuario = %s AND id_rol = 5
    """, (
        data['nombre'], data['apellido'], data['email'], id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})




# Obtener todos los destinos (para el select)
@app.route('/api/v2_destino/destinos', methods=['GET'])
def V2_obtener_destinos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT pais,ciudad FROM destino")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(datos)

# Obtener todos los alojamientos
@app.route('/api/v2_destino/alojamientos', methods=['GET'])
def V2_obtener_alojamientos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_alojamiento, nombre, descripcion, tipo_alojamiento, capacidad, precio, destino 
        FROM alojamiento
    """)
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(datos)

# Crear nuevo alojamiento
@app.route('/api/v2_destino/alojamientos', methods=['POST'])
def Vcrear_alojamiento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alojamiento (nombre, descripcion, tipo_alojamiento, capacidad, precio, destino)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['nombre'], data['descripcion'], data['tipo_alojamiento'],
        data['capacidad'], data['precio'], data['destino']
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})


@app.route('/cliente')
def serve_cliente():
    return send_from_directory('static/cliente/browser', 'index.html')

@app.route('/jefe_pag')
def serve_jefe_pag():
    return send_from_directory('static/jefe_pag/browser', 'index.html')

@app.route('/pagina_destino')
def serve_destino():
    return send_from_directory('static/destino/browser', 'index.html')

#--- Paquetes de rutas ---
@app.route('/api/paquetes_cliente', methods=['GET'])
def obtener_paquetes_cliente():
    conn = get_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_paquete, nombre, descripcion, precio, 
                   cupos_totales, cupos_disponibles, 
                   fecha_inicio, fecha_fin, tipo, disponible,
                   vuelo, vehiculo, alojamiento, excursion
            FROM paquete;
        """)
        rows = cur.fetchall()
        columnas = [desc[0] for desc in cur.description]
        paquetes = [dict(zip(columnas, row)) for row in rows]

        cur.close()
        conn.close()
        return jsonify(paquetes)
    except Exception as e:
        print("Error al obtener paquetes:", e)
        return jsonify({'error': 'Error en la consulta'}), 500








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



# ------------------ ARRANCAR SERVIDOR -------------------
if __name__ == '__main__':
    print("Servidor Flask arrancando...")
    app.run(debug=True, port=5000)

