from flask import Blueprint, request, jsonify
from conexion import get_connection

paquetes_bp = Blueprint('paquetes', __name__)

@paquetes_bp.route("/api/paquetes_cliente", methods=["GET"])
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

@paquetes_bp.route("/api/paquetes", methods=["POST"])
def crear_paquete():
    data = request.get_json()

    def convertir_a_null(valor):
        return valor if valor not in [None, "", "null"] else None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO paquete (
                nombre, descripcion, precio, cupos_totales, fecha_inicio, fecha_fin,
                tipo, disponible, cupos_disponibles, vuelo, vehiculo, alojamiento, excursion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("nombre"), data.get("descripcion"), data.get("precio"),
            data.get("cupos_totales"), data.get("fecha_inicio"), data.get("fecha_fin"),
            data.get("tipo"), data.get("disponible"), data.get("cupos_disponibles"),
            convertir_a_null(data.get("vuelo")),
            convertir_a_null(data.get("vehiculo")),
            convertir_a_null(data.get("alojamiento")),
            convertir_a_null(data.get("excursion"))
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Paquete creado exitosamente"}), 201
    except Exception as e:
        print("Error al crear paquete:", e)
        return jsonify({"message": "Error al crear el paquete", "error": str(e)}), 500

@paquetes_bp.route("/api/paquetes", methods=["GET"])
def obtener_paquetes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_paquete, nombre, descripcion, precio, cupos_disponibles,
               cupos_totales, fecha_inicio, fecha_fin, tipo
        FROM paquete
    """)
    paquetes = cursor.fetchall()
    cursor.close()
    conn.close()

    resultado = [
        {"id": p[0], "nombre": p[1], "descripcion": p[2], "precio": float(p[3]),
         "cupos_disponibles": p[4], "cupos_totales": p[5], "fecha_inicio": p[6],
         "fecha_fin": p[7], "tipo": p[8]}
        for p in paquetes
    ]
    return jsonify(resultado)

@paquetes_bp.route("/api/paquetes/<int:id>", methods=["DELETE"])
def eliminar_paquete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paquete WHERE id_paquete = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Paquete eliminado correctamente"}), 200
