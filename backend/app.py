# Configuración de Flask
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from conexion import get_connection
from datetime import date
from auth.login import auth_login
from auth.register import auth_register
from auth.recuperar import recuperar_bp
from admin.recursos import recursos_bp
from admin.paquetes import paquetes_bp
from admin.v2_destino import v2_destino_bp
import mercadopago
app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_login)
app.register_blueprint(auth_register)
app.register_blueprint(recuperar_bp)
app.register_blueprint(recursos_bp)
app.register_blueprint(paquetes_bp)
app.register_blueprint(v2_destino_bp)

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

@app.route('/cliente')
def serve_cliente():
    return send_from_directory('static/cliente/browser', 'index.html')

@app.route('/jefe_pag')
def serve_jefe_pag():
    return send_from_directory('static/jefe_pag/browser', 'index.html')

@app.route('/pagina_destino')
def serve_destino():
    return send_from_directory('static/destino/browser', 'index.html')

@app.route('/documentos')
def serve_documentos():
    return send_from_directory('static/documentos/browser', 'index.html')



@app.route('/api/reservas', methods=['POST'])
def crear_reserva():
    from datetime import date
    data = request.get_json()

    id_paquete = data.get("id_paquete")
    id_usuario = data.get("id_usuario")
    cantidad_personas = data.get("cantidad_personas", 1)
    estado = data.get("estado", True)
    observaciones = data.get("observaciones", "")

    if not id_paquete or not id_usuario:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Obtener precio del paquete
        cur.execute("SELECT precio FROM paquete WHERE id_paquete = %s", (id_paquete,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Paquete no encontrado"}), 404
        precio = row[0]

        # Insertar reserva
        cur.execute("""
            INSERT INTO reserva (id_paquete, fecha_reserva, cantidad_personas, id_usuario, estado, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_reserva
        """, (id_paquete, date.today(), cantidad_personas, id_usuario, estado, observaciones))

        id_reserva = cur.fetchone()[0]
        conn.commit()

        return jsonify({"id_reserva": id_reserva, "precio_paquete": float(precio)}), 200

    except Exception as e:
        conn.rollback()
        print("Error al crear reserva:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cur.close()
        conn.close()
        
@app.route('/api/carrito', methods=['POST'])
def crear_carrito():
    from datetime import date
    data = request.get_json()

    reserva = data.get("reserva")
    precio_final = data.get("precio_final", 0)
    metodo_pago = data.get("metodo_pago", "Transferencia")
    estado_pago = data.get("estado_pago", "Pendiente")

    if not reserva:
        return jsonify({"error": "Falta el ID de reserva"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO carrito (reserva, fecha_carrito, precio_final, metodo_pago, estado_pago)
            VALUES (%s, %s, %s, %s, %s)
        """, (reserva, date.today(), precio_final, metodo_pago, estado_pago))
        conn.commit()
        return jsonify({"mensaje": "Carrito creado"}), 200

    except Exception as e:
        conn.rollback()
        print("Error al crear carrito:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cur.close()
        conn.close()


@app.route('/api/carrito/detalles', methods=['POST'])
def obtener_detalles_carrito():
    data = request.get_json()
    ids = data.get("ids", [])

    if not ids:
        return jsonify([])

    try:
        conn = get_connection()
        cur = conn.cursor()

        consulta = f'''
            SELECT
                p.id_paquete,
                p.nombre AS paquete_nombre,
                p.descripcion AS paquete_desc,
                p.precio,
                p.fecha_inicio,
                p.fecha_fin,

                v.aerolinea, v.aeropuerto_o, v.aeropuerto_d, v.fecha AS vuelo_fecha, v.duracion AS vuelo_duracion,
                vh.marca AS vehiculo_marca, vh.modelo AS vehiculo_modelo, vh.capacidad AS vehiculo_capacidad,
                a.nombre AS alojamiento_nombre, a.descripcion AS alojamiento_desc, a.tipo_alojamiento, a.capacidad AS alojamiento_capacidad,
                e.nombre AS excursion_nombre, e.descripcion AS excursion_desc, e.duracion AS excursion_duracion,

                d.pais AS destino_pais, d.ciudad AS destino_ciudad, d.region AS destino_region, d.descripcion AS destino_desc

            FROM paquete p
            LEFT JOIN vuelo v ON p.vuelo = v.id_vuelo
            LEFT JOIN vehiculo_alquiler vh ON p.vehiculo = vh.id_vehiculo
            LEFT JOIN alojamiento a ON p.alojamiento = a.id_alojamiento
            LEFT JOIN excursion e ON p.excursion = e.id_excursion
            LEFT JOIN destino d ON v.destino = d.id_destino

            WHERE p.id_paquete = ANY(%s)
        '''

        cur.execute(consulta, (ids,))
        columnas = [desc[0] for desc in cur.description]
        resultados = [dict(zip(columnas, fila)) for fila in cur.fetchall()]

        cur.close()
        conn.close()

        return jsonify(resultados)

    except Exception as e:
        print("Error en /api/carrito/detalles:", e)
        return jsonify({'error': 'Error al obtener datos del carrito'}), 500


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

# Configuración del SDK
sdk = mercadopago.SDK("APP_USR-4018927116411934-061904-77e75d5c947b1c3da7195bad29f0e838-2503073937")

@app.route('/crear_pago', methods=['POST'])
def crear_pago():
    data = request.get_json()
    monto = data.get("precio", 0)
    id_paquete = data.get("id_paquete")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Error al conectar a la base de datos"}), 500
    cursor = conn.cursor()

    # Consulta para obtener detalles del paquete
    cursor.execute("""
        SELECT p.nombre AS paquete_nombre,
               v.aerolinea, v.aeropuerto_o, v.aeropuerto_d,
               veh.marca AS vehiculo_marca, veh.modelo AS vehiculo_modelo,
               a.nombre AS alojamiento_nombre,
               e.nombre AS excursion_nombre
        FROM paquete p
        LEFT JOIN vuelo v ON p.vuelo = v.id_vuelo
        LEFT JOIN vehiculo_alquiler veh ON p.vehiculo = veh.id_vehiculo
        LEFT JOIN alojamiento a ON p.alojamiento = a.id_alojamiento
        LEFT JOIN excursion e ON p.excursion = e.id_excursion
        WHERE p.id_paquete = %s
    """, (id_paquete,))
    detalles = cursor.fetchone()
    conn.close()

    if not detalles:
        return jsonify({"error": "Paquete no encontrado"}), 404

    paquete_nombre, aerolinea, aeropuerto_o, aeropuerto_d, vehiculo_marca, vehiculo_modelo, alojamiento_nombre, excursion_nombre = detalles
    descripcion_item = (
        f"{paquete_nombre}. Vuelo: {aerolinea} ({aeropuerto_o} → {aeropuerto_d}), "
        f"Vehículo: {vehiculo_marca} {vehiculo_modelo}, Alojamiento: {alojamiento_nombre}, "
        f"Excursión: {excursion_nombre}"
    )

    # Crear la preferencia en MercadoPago
    preference_data = {
        "items": [
            {
                "title": paquete_nombre,
                "description": descripcion_item,
                "quantity": 1,
                "unit_price": float(monto),
                "currency_id": "ARS"
            }
        ],
        "back_urls": {
            "success": "https://www.google.com",
        },
        "auto_return": "approved"
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        print("Respuesta de MP:", preference_response)

        preference = preference_response.get("response", {})
        if "init_point" not in preference:
            return jsonify({"error": "No se pudo generar el link de pago", "detalle": preference}), 400

        return jsonify({"init_point": preference["init_point"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reportes", methods=["GET"])
def obtener_reportes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_reporte, id_usuario, tipo_reporte, fecha_generacion, contenido, parametros FROM reporte")
    registros = cur.fetchall()
    cur.close()
    conn.close()
    reportes = [
        {
            "id_reporte": r[0],
            "id_usuario": r[1],
            "tipo_reporte": r[2],
            "fecha_generacion": str(r[3]),
            "contenido": r[4],
            "parametros": r[5]
        } for r in registros
    ]
    return jsonify(reportes)

@app.route("/api/reservas", methods=["GET"])
def obtener_reservas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_reserva, id_paquete, fecha_reserva, cantidad_personas, id_usuario, estado, observaciones FROM reserva")
    registros = cur.fetchall()
    cur.close()
    conn.close()
    reservas = [
        {
            "id_reserva": r[0],
            "id_paquete": r[1],
            "fecha_reserva": str(r[2]),
            "cantidad_personas": r[3],
            "id_usuario": r[4],
            "estado": r[5],
            "observaciones": r[6]
        } for r in registros
    ]
    return jsonify(reservas)


# ------------------ ARRANCAR SERVIDOR -------------------
if __name__ == '__main__':
    print("Servidor Flask arrancando...")
    app.run(host='0.0.0.0', port=5000, debug=True)