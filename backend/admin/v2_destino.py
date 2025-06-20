from flask import Blueprint, request, jsonify
from conexion import get_connection

v2_destino_bp = Blueprint('v2_destino', __name__)

@v2_destino_bp.route('/api/v2_destino/destinos', methods=['GET'])
def obtener_destinos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT pais, ciudad FROM destino")
    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(datos)

@v2_destino_bp.route('/api/v2_destino/alojamientos', methods=['GET'])
def obtener_alojamientos():
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

@v2_destino_bp.route('/api/v2_destino/alojamientos', methods=['POST'])
def crear_alojamiento():
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
