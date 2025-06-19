from flask import Blueprint, request, jsonify, send_from_directory
from conexion import get_connection

recursos_bp = Blueprint('recursos', __name__)

# --------- DESTINOS ---------

@recursos_bp.route('/api/destinos', methods=['GET'])
def obtener_destinos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_destino, pais, ciudad FROM destino ORDER BY pais, ciudad")
        destinos = cursor.fetchall()
        lista = [{"id_destino": d[0], "pais": d[1], "ciudad": d[2]} for d in destinos]
        return jsonify(lista)
    except Exception as e:
        print("Error obteniendo destinos:", e)
        return jsonify([]), 500
    finally:
        cursor.close()
        conn.close()

@recursos_bp.route('/api/destinos', methods=['POST'])
def crear_destino():
    data = request.json
    pais = data.get('pais')
    ciudad = data.get('ciudad')
    region = data.get('region')
    descripcion = data.get('descripcion')

    if not pais or not ciudad or not region or not descripcion:
        return jsonify({'error': 'Faltan campos'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO destino (pais, ciudad, region, descripcion)
        VALUES (%s, %s, %s, %s)
    """, (pais, ciudad, region, descripcion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Destino creado correctamente'}), 201

@recursos_bp.route('/api/destinos/<int:id>', methods=['PUT'])
def actualizar_destino(id):
    data = request.json
    pais = data.get('pais')
    ciudad = data.get('ciudad')
    region = data.get('region')
    descripcion = data.get('descripcion')

    if not pais or not ciudad or not region or not descripcion:
        return jsonify({'error': 'Faltan campos'}), 400

    conn = get_connection()
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

@recursos_bp.route('/api/destinos/<int:id>', methods=['DELETE'])
def eliminar_destino(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM destino WHERE id_destino = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Destino eliminado correctamente'}), 200

# --------- ALOJAMIENTOS ---------

@recursos_bp.route('/recursos')
def serve_recursos():
    return send_from_directory('static/recursos/browser', 'index.html')

@recursos_bp.route('/api/alojamientos', methods=['GET'])
def get_alojamientos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alojamiento")
    columnas = [desc[0] for desc in cursor.description]
    alojamientos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(alojamientos)

@recursos_bp.route('/api/alojamientos', methods=['POST'])
def agregar_alojamiento():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alojamiento (nombre, descripcion, tipo_alojamiento, capacidad, precio, destino)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['nombre'], data['descripcion'], data['tipo_alojamiento'],
          data['capacidad'], data['precio'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Alojamiento agregado'}), 201

@recursos_bp.route('/api/alojamientos/<int:id_alojamiento>', methods=['DELETE'])
def eliminar_alojamiento(id_alojamiento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alojamiento WHERE id_alojamiento = %s", (id_alojamiento,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Alojamiento eliminado'}), 200

# --------- VEHÍCULOS ---------

@recursos_bp.route('/api/vehiculos', methods=['GET'])
def get_vehiculos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo_alquiler")
    columnas = [desc[0] for desc in cursor.description]
    vehiculos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(vehiculos)

@recursos_bp.route('/api/vehiculos', methods=['POST'])
def crear_vehiculo():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehiculo_alquiler (marca, modelo, capacidad, destino)
        VALUES (%s, %s, %s, %s)
    """, (data['marca'], data['modelo'], data['capacidad'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vehículo agregado'}), 201

@recursos_bp.route('/api/vehiculos/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehiculo_alquiler WHERE id_vehiculo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vehículo eliminado'}), 200

# =================== VUELOS ===================

@recursos_bp.route('/api/vuelos', methods=['GET'])
def get_vuelos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vuelo")
    columnas = [desc[0] for desc in cursor.description]
    vuelos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(vuelos)

@recursos_bp.route('/api/vuelos', methods=['POST'])
def crear_vuelo():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vuelo (aerolinea, aeropuerto_o, aeropuerto_d, fecha, duracion, precio, destino)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data['aerolinea'], data['aeropuerto_o'], data['aeropuerto_d'],
          data['fecha'], data['duracion'], data['precio'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vuelo agregado correctamente'}), 201

@recursos_bp.route('/api/vuelos/<int:id>', methods=['DELETE'])
def eliminar_vuelo(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vuelo WHERE id_vuelo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Vuelo eliminado'}), 200

# =================== EXCURSIONES ===================

@recursos_bp.route('/api/excursiones', methods=['GET'])
def obtener_excursiones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id_excursion, e.nombre, e.descripcion, e.duracion,
               e.precio_adulto, e.precio_nino, e.participantes,
               d.pais, d.ciudad
        FROM excursion e
        JOIN destino d ON e.destino = d.id_destino
    """)
    excursiones = cursor.fetchall()
    cursor.close()
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

@recursos_bp.route('/api/excursiones', methods=['POST'])
def crear_excursion():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO excursion (nombre, descripcion, duracion, precio_adulto,
                               precio_nino, participantes, destino)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data['nombre'], data['descripcion'], data['duracion'],
          data['precio_adulto'], data['precio_nino'],
          data['participantes'], data['destino']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Excursión creada con éxito'})

@recursos_bp.route('/api/excursiones/<int:id_excursion>', methods=['DELETE'])
def eliminar_excursion(id_excursion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM excursion WHERE id_excursion = %s", (id_excursion,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Excursión eliminada'})