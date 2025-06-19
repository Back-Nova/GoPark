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

